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
- uses qemu-img calls (requires libovsvolumedriver, qemu, libvirt-bin packages from openvstorage repo)
- uses https api where needed
"""

from oslo_config import cfg
from oslo_log import log as logging
import six

from cinder import exception
from cinder import utils
from cinder.i18n import _, _LE
from cinder.image import image_utils
from cinder.volume import driver


LOG = logging.getLogger(__name__)
OPTS = [cfg.StrOpt('storage_ip',
                   default = '',
                   help = 'IP address of first storage node'),
        cfg.StrOpt('edge_port',
                   default = '26203',
                   help = 'PORT of the edge server'),
        cfg.StrOpt('edge_protocol',
                   default = 'tcp',
                   help = 'Protocol to use - edge client')]

CONF = cfg.CONF
CONF.register_opts(OPTS)

class OpenvStorageEdgeVolumeDriver(driver.VolumeDriver):
    """Open vStorage Edge Volume Driver plugin for Cinder."""
    VERSION = '0.0.1'

    def __init__(self, *args, **kwargs):
        """Init: args, kwargs pass through;

        Options come from CONF
        """
        super(OpenvStorageEdgeVolumeDriver, self).__init__(*args, **kwargs)
        LOG.debug('INIT %s %s %s %s %s', CONF.storage_ip, CONF.edge_port, CONF.edge_protocol, args, kwargs)
        self.configuration.append_config_values(OPTS)
        self.volume_backend_name = kwargs['host'].split('@')[1]

    def _get_volume_location(self, volume_name):
        return 'openvstorage+{0}:{1}:{2}/{3}'.format(self.configuration.edge_protocol,
                                                     self.configuration.storage_ip,
                                                     self.configuration.edge_port,
                                                     volume_name)

    def _run_qemu_img(self, command, volume_name, *params):
        """Executes qemu-img command wrapper."""
        location = self._get_volume_location(volume_name)
        cmd = ['env', 'LC_ALL=C', 'LANG=C', 'qemu-img', command, location] + list(params)
        return utils.execute(*cmd)


    def check_for_setup_error(self):
        pass

    # Volume operations
    def initialize_connection(self, volume, connector):
        """Allow connection to connector and return connection info.

        Volume is a .raw file on a virtual filesystem.
        No specific action required, connection is allowed based
        on POSIX permissions
        """

        return {'driver_volume_type': 'openvstorage_edge',
                'data': {'device_path': volume.provider_location}}

    def create_volume(self, volume):
        """Creates a volume.

        Called on "cinder create ..." or "nova volume-create ..."
        :param volume: volume reference (sqlalchemy Model)
        """
        self._run_qemu_img('create', volume.display_name, '{0}G'.format(volume.size))

        location = self._get_volume_location(volume.display_name)
        volume['provider_location'] = location

        return {'provider_location': volume['provider_location']}

    def delete_volume(self, volume):
        """Deletes a logical volume.

        Called on "cinder delete ... "
        :param volume: volume reference (sqlalchemy Model)
        """
        location = self._get_volume_location(volume.display_name)
        

    def get_volume_stats(self, refresh=False):
        """Get volumedriver stats

        Refresh not implemented
        """
        data = {}
        data['volume_backend_name'] = self.volume_backend_name
        data['vendor_name'] = 'Open vStorage'
        data['driver_version'] = self.VERSION
        data['storage_protocol'] = 'openvstorage_edge'
        data['total_capacity_gb'] = 'unknown'
        data['free_capacity_gb'] = 'unknown'
        data['reserved_percentage'] = 0
        data['QoS_support'] = False
        return data


