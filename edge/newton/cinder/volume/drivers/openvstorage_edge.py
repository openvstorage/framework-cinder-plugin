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

sudo mkdir -p /opt/OpenvStorage/
sudo git clone https://github.com/openvstorage/framework-cinder-plugin.git /opt/OpenvStorage/
cd /opt/OpenvStorage/
sudo git checkout ovs-23-cinder-cleanup
sudo find . -type d -exec touch {}/__init__.py \;
cd /opt/
sudo chown -R ovs-support:ovs-support OpenvStorage/
"""
import sys
import random
import os, ctypes, errno
from ctypes import cdll, CDLL

from oslo_config import cfg
from oslo_log import log as logging
import six

from cinder import exception
from cinder import utils
from cinder.image import image_utils
from cinder.volume import driver

# Open vStorage imports

OVS_DIR = "/opt/OpenvStorage"
sys.path.append(OVS_DIR)

from ci.api_lib.helpers.api import OVSClient
from ci.api_lib.helpers.vdisk import VDiskHelper
from ci.api_lib.helpers.storagedriver import StoragedriverHelper
from ci.api_lib.helpers.storagerouter import StoragerouterHelper
from ci.api_lib.setup.vdisk import VDiskSetup

LOG = logging.getLogger(__name__)
OPTS = [cfg.StrOpt('management_ips',
                   default='10.100.199.191',
                   help='IP addresses of a Open vStorage master nodes'),
        cfg.StrOpt('vpool_guid',
                   default='7968a798-a0ab-4f6a-8f3d-32f785215307',
                   help='Name of the used vPool'),
        cfg.StrOpt('username',
                   default='admin',
                   help='Username of user used to access Open vStorage'),
        cfg.StrOpt('password',
                   default='admin',
                   help='Password of user used to access Open vStorage'),
        cfg.StrOpt('port',
                   default='443',
                   help='Port to reach Open vStorage API')]

CONF = cfg.CONF
CONF.register_opts(OPTS)


class OpenvStorageEdgeVolumeDriver(driver.VolumeDriver):
    """Open vStorage Edge Volume Driver plugin for Cinder."""

    VERSION = '0.0.1'
    SNAPSHOT_CREATE_TIMEOUT = 120
    VOLUME_PREFIX = "volume-"

    def __init__(self, *args, **kwargs):
        """
        Initialize Open vStorage cinder plugin

        Options come from CONF
        """
        super(OpenvStorageEdgeVolumeDriver, self).__init__(*args, **kwargs)
        self.configuration.append_config_values(OPTS)
        self.volume_backend_name = kwargs['host'].split('@')[1]
        LOG.debug('libovsvolumedriver.init {0} {1} {2} {3} {4}'.format(CONF.management_ips, CONF.vpool_guid,
                                                                       CONF.username, CONF.password, CONF.port))
        cdll.LoadLibrary('libovsvolumedriver.so')
        self.libovsvolumedriver = CDLL('libovsvolumedriver.so', use_errno=True)

    def _get_volume_location(self, volume_name, storage_ip=None):
        """
        Return volume location for edge client

        :param volume_name: name of a volume without .raw, .vmdk
        :type volume_name: str
        :param storage_ip: request a volume location on a specific storage_ip
        :type storage_ip: str
        :return: volume location
        :rtype: str
        """
        storagedriver = self._get_storagedriver_information(storage_ip=storage_ip)
        volume_location = 'openvstorage+{0}:{1}:{2}/{3}'.format(storagedriver['cluster_node_config']
                                                                ['network_server_uri'].split(':')[0],
                                                                storagedriver['storage_ip'],
                                                                storagedriver['ports']['edge'],
                                                                volume_name)
        LOG.debug('libovsvolumedriver.generating.volume.location {0}'.format(volume_location))
        return volume_location

    def _get_storagedriver_information(self, storage_ip=None):
        """
        Returns a storagedriver its information
        Currently a random storagedriver is chosen from the vpool if storage_ip is None,
        in the future this can be strategically chosen

        :return: storagedriver information
        :rtype: dict
        """
        api = self._setup_ovs_client()
        data = StoragedriverHelper.get_storagedrivers_by_vpoolguid(vpool_guid=CONF.vpool_guid, api=api)

        # if a specific storagedriver is requested, provide this one. else provide a random one
        if storage_ip:
            storagedriver = [sd for sd in data if sd['storage_ip'] == storage_ip][0]
        else:
            storagedriver = random.choice(data)
        LOG.debug('libovsvolumedriver.get_storagedriver_information {0}'.format(storagedriver))
        return storagedriver

    @staticmethod
    def _get_management_ip():
        """
        Returns a available ip address to contact Open vStorage
        Currently a random ip is given. In the future this could be HA tested

        :return: management ip
        :rtype: str
        """

        return CONF.management_ips

    def _setup_ovs_client(self):
        """
        Sets up a OVSClient to contact the Open vStorage API

        :return: api client
        :return: ci.api_lib.helpers.api.OVSClient
        """

        return OVSClient(ip=self._get_management_ip(),
                         username=CONF.username,
                         password=CONF.password)

    @staticmethod
    def _run_qemu_img(command, *params):
        """
        Executes qemu-img command wrapper.
        """
        cmd = ['env', 'LC_ALL=C', 'LANG=C', 'qemu-img', command] + list(params)
        output = utils.execute(*cmd)
        LOG.debug('Run: {0} Output: {1}'.format(cmd, output))
        return output

    def check_for_setup_error(self):
        """
        Check for setup errors
        """

        pass

    def do_setup(self, context):
        """
        Any initialization the volume driver does while starting.
        """
        pass

    def _setup_ovsvolumedriver(self):
        """
        Sets up the ovsvolumedriver

        :return: libovsvolumedriver
        :rtype: libovsvolumedriver
        """

        ctx_attr = self.libovsvolumedriver.ovs_ctx_attr_new()

        # fetch first time setup information
        storagedriver = self._get_storagedriver_information()
        edge_protocol = storagedriver['cluster_node_config']['network_server_uri'].split(':')[0]

        self.libovsvolumedriver.ovs_ctx_attr_set_transport(ctx_attr, edge_protocol, storagedriver['storage_ip'],
                                                           int(storagedriver['ports']['edge']))
        LOG.debug('libovsvolumedriver.do_setup {0} {1} {2} {3}'.format(ctx_attr, edge_protocol,
                                                                       storagedriver['storage_ip'],
                                                                       storagedriver['ports']['edge']))
        return self.libovsvolumedriver, self.libovsvolumedriver.ovs_ctx_new(ctx_attr)

    # Volume operations
    def initialize_connection(self, volume, connector):
        """Allow connection to connector and return connection info."""
        _ = connector
        return {'driver_volume_type': 'openvstorage_edge',
                'volume_backend_name': self.volume_backend_name,
                'data': {'device_path': volume.provider_location}}

    def create_volume(self, volume):
        """
        Creates a volume.
        Called by "cinder create ..." or "nova volume-create ..."

        :param volume: volume reference (sqlalchemy Model)
        :return: volume location
        :rtype: dict
        """
        volume_name = self.VOLUME_PREFIX + str(volume.id)
        location = self._get_volume_location(volume_name)
        out = self._run_qemu_img('create', location, '{0}G'.format(volume.size))
        LOG.debug('libovsvolumedriver.ovs_create_volume: {0} {1} {2}'.format(volume.id, volume.size, out))

        if out == -1:
           raise OSError(errno.errorcode[ctypes.get_errno()])

        volume['provider_location'] = location
        return {'provider_location': volume['provider_location']}

    def delete_volume(self, volume):
        """
        Deletes a logical volume.
        Called by "cinder delete ... "

        :param volume: volume reference (sqlalchemy Model)
        """
        volume_name = self.VOLUME_PREFIX + str(volume.id)
        libovsvolumedriver, ctx = self._setup_ovsvolumedriver()
        out = libovsvolumedriver.ovs_remove_volume(ctx, volume_name)
        LOG.debug('libovsvolumedriver.ovs_remove_volume: {0} {1} > {2}'.format(ctx, volume, out))
        if out == -1:
            errno = ctypes.get_errno()
            raise OSError(errno.errorcode[errno])

    def create_snapshot(self, snapshot):
        """Creates a snapshot."""

        location = self._get_volume_location(snapshot['volume_name'])
        out = self._run_qemu_img('snapshot', location, '-c', snapshot['name'])
        LOG.debug('libovsvolumedriver.ovs_snapshot_create: {0} {1} {2}'.format(str(snapshot['volume_name']),
                                                                               str(snapshot['name']), out))
        if out == -1:
            errno = ctypes.get_errno()
            raise OSError(errno.errorcode[errno])

    def delete_snapshot(self, snapshot):
        """Deletes a snapshot."""

        location = self._get_volume_location(snapshot['volume_name'])
        out = self._run_qemu_img('snapshot', location, '-d', snapshot['name'])
        LOG.debug('libovsvolumedriver.ovs_snapshot_remove: {0} {1} {2}'.format(str(snapshot['volume_name']),
                                                                               str(snapshot['name']), out))

        if out == -1:
            errno = ctypes.get_errno()
            raise OSError(errno.errorcode[errno])

    def create_cloned_volume(self, volume, src_vref):
        """
        Creates a clone of the specified volume.

        :param volume: new volume object
        :param src_vref: source volume object
        """
        source_volume_name = self.VOLUME_PREFIX + str(src_vref.id)
        new_volume_name = self.VOLUME_PREFIX + str(volume.id)
        LOG.debug('libovsvolumedriver.ovs_clone new={0} source={1}'.format(volume.id, src_vref.id))

        api = self._setup_ovs_client()
        # pick a random storagerouter to deploy the new clone on
        storagerouter_ip = random.choice([sr for sr in StoragerouterHelper.get_storagerouters(api=api).values()
                                          if CONF.vpool_guid in sr['vpools_guids']])
        VDiskSetup.create_clone(vdisk_name=source_volume_name, new_vdisk_name=new_volume_name,
                                storagerouter_ip=storagerouter_ip, api=api, vpool_guid=CONF.vpool_guid)

    def copy_image_to_volume(self, context, volume, image_service, image_id):
        """
        Copy image to volume
        Called on "nova volume-create --image-id ..."
        or "cinder create --image-id"
        Downloads image from glance server into volume

        :param context: Context object
        :param volume: volume reference (sqlalchemy Model)
        :param image_service: image service reference
        :param image_id: id of the image
        """
        volume_name = self.VOLUME_PREFIX + str(volume.id)
        location = self._get_volume_location(volume_name=volume_name)
        image_path = os.path.join('/tmp', image_id)
        if not os.path.exists(image_path):
            image_utils.fetch_to_raw(context, image_service, image_id, image_path, '1M', size=volume['size'])
        self._run_qemu_img('convert', '-n', '-O', 'raw', image_path, location)
        LOG.debug('libovsvolumedriver.ovs_copy_image_to_volume {0} {1}'.format(volume.id, image_id))

    def extend_volume(self, volume, size_gb):
        """Extend volume to new size size_gb."""
        if size_gb < volume.size:
            raise RuntimeError('Cannot shrink volume: {0} > {1}'.format(volume.size, size_gb))

        volume_name = self.VOLUME_PREFIX + str(volume.id)
        location = self._get_volume_location(volume_name)
        out = self._run_qemu_img('resize', location, '{0}G'.format(size_gb))

        LOG.debug('libovsvolumedriver.ovs_truncate_volume: {0} {1} {2} < {3}'.format(volume.id, volume.size, size_gb,
                                                                                     out))

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
