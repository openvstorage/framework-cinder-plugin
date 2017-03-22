# Copyright 2016 iNuron NV
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
OpenStack Cinder driver - interface to Open vStorage Edge

- uses qemu-img calls (requires qemu & libvirt-bin packages from openvstorage.com repo)
"""
import os, ctypes, errno
from ctypes import cdll, CDLL

from oslo_config import cfg
from oslo_log import log as logging
import six

from cinder import exception
from cinder import utils
from cinder.image import image_utils
from cinder.volume import driver


LOG = logging.getLogger(__name__)
OPTS = [cfg.StrOpt('storage_ip',
                   default='',
                   help='IP address of first storage node'),
        cfg.StrOpt('edge_port',
                   default='26203',
                   help='PORT of the edge server'),
        cfg.StrOpt('edge_protocol',
                   default='tcp',
                   help='Protocol to use - edge client')]

CONF = cfg.CONF
CONF.register_opts(OPTS)


class OpenvStorageEdgeVolumeDriver(driver.VolumeDriver):
    """Open vStorage Edge Volume Driver plugin for Cinder."""

    VERSION = '0.0.1'

    # https://github.com/openvstorage/volumedriver/blob/dev/docs/libovsvolumedriver.txt#L263
    SNAPSHOT_CREATE_TIMEOUT = 120

    def __init__(self, *args, **kwargs):
        """Init: args, kwargs pass through;

        Options come from CONF
        """
        super(OpenvStorageEdgeVolumeDriver, self).__init__(*args, **kwargs)
        LOG.debug('INIT %s %s %s %s %s', CONF.storage_ip, CONF.edge_port, CONF.edge_protocol, args, kwargs)
        self.configuration.append_config_values(OPTS)
        self.volume_backend_name = kwargs['host'].split('@')[1]

    def _get_volume_location(self, volume_name):
        """Return volume location."""
        return 'openvstorage+{0}:{1}:{2}/{3}'.format(self.configuration.edge_protocol,
                                                     self.configuration.storage_ip,
                                                     self.configuration.edge_port,
                                                     volume_name)

    def _run_qemu_img(self, command, *params):
        """Executes qemu-img command wrapper."""
        cmd = ['env', 'LC_ALL=C', 'LANG=C', 'qemu-img', command] + list(params)
        output = utils.execute(*cmd)
        LOG.debug('Run: {0} Output: {1}'.format(cmd, output))
        return output

    def check_for_setup_error(self):
        """Check for setup errors"""
        pass

    def do_setup(self, context):
        """Any initialization the volume driver does while starting."""
        cdll.LoadLibrary('libovsvolumedriver.so')
        libovsvolumedriver = CDLL('libovsvolumedriver.so', use_errno=True)
        ctx_attr = libovsvolumedriver.ovs_ctx_attr_new()
        libovsvolumedriver.ovs_ctx_attr_set_transport(ctx_attr,
                                                      self.configuration.edge_protocol,
                                                      self.configuration.storage_ip,
                                                      int(self.configuration.edge_port))
        self.ctx = libovsvolumedriver.ovs_ctx_new(ctx_attr)
        LOG.debug('libovsvolumedriver do_setup: {0} {1} {2} {3} > {4}'.format(ctx_attr,
                                                                              self.configuration.edge_protocol,
                                                                              self.configuration.storage_ip,
                                                                              self.configuration.edge_port, self.ctx))
        self.libovsvolumedriver = libovsvolumedriver

    # Volume operations
    def initialize_connection(self, volume, connector):
        """Allow connection to connector and return connection info."""
        _ = connector
        return {'driver_volume_type': 'openvstorage_edge',
                'volume_backend_name': self.volume_backend_name,
                'data': {'device_path': volume.provider_location}}

    def create_volume(self, volume):
        """Creates a volume.

        Called on "cinder create ..." or "nova volume-create ..."
        :param volume: volume reference (sqlalchemy Model)
        """
        volume_name = "volume-" + str(volume.id)
        location = self._get_volume_location(volume_name)
        out = self._run_qemu_img('create', location, '{0}G'.format(volume.size))
        LOG.debug('libovsvolumedriver.ovs_create_volume: {0} {1} {2} > {3}'.format(self.ctx, volume, volume.size, out))
        if out == -1:
           raise OSError(errno.errorcode[ctypes.get_errno()])

        volume['provider_location'] = location
        return {'provider_location': volume['provider_location']}

    def delete_volume(self, volume):
        """Deletes a logical volume.

        Called on "cinder delete ... "
        :param volume: volume reference (sqlalchemy Model)
        """
        volume_name = "volume-" + str(volume.id)
        out = self.libovsvolumedriver.ovs_remove_volume(self.ctx, volume_name)
        LOG.debug('libovsvolumedriver.ovs_remove_volume: {0} {1} > {2}'.format(self.ctx, volume, out))
        if out == -1:
            errno = ctypes.get_errno()
            raise OSError(errno.errorcode[errno])

    def create_snapshot(self, snapshot):
        """Creates a snapshot."""

        out = self.libovsvolumedriver.ovs_snapshot_create(self.ctx,
                                                          str(snapshot['volume_name']),
                                                          str(snapshot['name']),
                                                          OpenvStorageEdgeVolumeDriver.SNAPSHOT_CREATE_TIMEOUT)
        LOG.debug('libovsvolumedriver.ovs_snapshot_create: {0} {1} {2} {3}'.format(self.ctx,
                                                                                   str(snapshot['volume_name']),
                                                                                   str(snapshot['name']), out))
        if out == -1:
            errno = ctypes.get_errno()
            raise OSError(errno.errorcode[errno])

    def delete_snapshot(self, snapshot):
        """Deletes a snapshot."""

        out = self.libovsvolumedriver.ovs_snapshot_remove(self.ctx,
                                                          str(snapshot['volume_name']),
                                                          str(snapshot['name']))
        LOG.debug('libovsvolumedriver.ovs_snapshot_remove: {0} {1} {2}'.format(self.ctx, str(snapshot), out))

        if out == -1:
            errno = ctypes.get_errno()
            raise OSError(errno.errorcode[errno])

    def copy_image_to_volume(self, context, volume, image_service, image_id):
        """Copy image to volume

        Called on "nova volume-create --image-id ..."
        or "cinder create --image-id"
        Downloads image from glance server into volume
        :param context: Context object
        :param volume: volume reference (sqlalchemy Model)
        :param image_service: image service reference
        :param image_id: id of the image
        """
        volume_name = "volume-" + str(volume.id)
        location = self._get_volume_location(volume_name)
        image_path = os.path.join('/tmp', image_id)
        if not os.path.exists(image_path):
            image_utils.fetch_to_raw(context,
                                     image_service,
                                     image_id,
                                     image_path,
                                     '1M',
                                     size=volume['size'])
        self._run_qemu_img('convert', '-n', '-O', 'raw', image_path, location)

    def extend_volume(self, volume, size_gb):
        """Extend volume to new size size_gb."""
        if size_gb < volume.size:
            raise RuntimeError('Cannot shrink volume.')
        volume_name = "volume-" + str(volume.id)
        out = self.libovsvolumedriver.ovs_truncate_volume(self.ctx, str(volume_name), int(volume.size*1024**3))
        LOG.debug('libovsvolumedriver.ovs_truncate_volume: {0} {1} {2} > {3}'.format(self.ctx, volume_name,
                                                                                     volume.size, out))

        if out == -1:
            raise OSError(errno.errorcode[ctypes.get_errno()])

    def attach_volume(self, context, volume, instance_uuid, host_name,
                      mountpoint):
        """Callback for volume attached to instance or host."""
        pass

    def detach_volume(self, context, volume, attachment=None):
        """Callback for volume detached."""
        pass

    def get_volume_stats(self, refresh=False):
        """Get volumedriver stats

        Refresh not implemented
        """
        _ = refresh
        return {'volume_backend_name': self.volume_backend_name,
                'vendor_name': 'Open vStorage',
                'driver_version': self.VERSION,
                'storage_protocol': 'openvstorage_edge',
                'total_capacity_gb': 'unknown',
                'free_capacity_gb': 'unknown',
                'reserved_percentage': 0,
                'QoS_support': False}

    def create_export(self, context, volume, connector=None):
        """Exports the volume."""
        pass

    def remove_export(self, context, volume):
        """Removes an export for a volume."""
        pass

    def ensure_export(self, context, volume):
        """Synchronously recreates an export for a volume."""
        pass

    def terminate_connection(self, volume, connector, force):
        """Disallow connection from connector"""
        pass
