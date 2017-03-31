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
OpenStack Nova driver - interface to Open vStorage Edge for qemu
- requires qemu, libvirt-bin packages from openvstorage repo
- see also config_PATCH
"""

from os_brick.initiator import connector

from oslo_log import log as logging

from nova import utils
from nova.virt.libvirt.volume.volume import LibvirtVolumeDriver
from nova.virt.libvirt import config as vconfig
from nova.virt.libvirt import utils as libvirt_utils

LOG = logging.getLogger(__name__)


class LibvirtOpenvStorageEdgeVolumeDriver(LibvirtVolumeDriver):
    """
    Class for volumes backed by OpenvStorage Edge
    """

    VOLUME_PREFIX = "volume-"
    LIBVIRT_MODULE = "openvstorage"

    def __init__(self, connection):
        super(LibvirtOpenvStorageEdgeVolumeDriver, self).__init__(connection)
        LOG.debug("libovsvolumedriver.init")

    def get_config(self, connection_info, disk_info):
        """
        Returns xml for libvirt.
        """
        conf = vconfig.LibvirtConfigOpenvStorageEdgeGuestDisk()
        conf.driver_name = libvirt_utils.pick_disk_driver_name(self.connection._host.get_version(),
                                                               self.is_block_dev)
        LOG.debug("libovsvolumedriver.libvirt.get_config {0} {1}".format(connection_info, disk_info))

        # u'device_path': u'openvstorage+tcp:10.130.11.202:26203/volimage3'
        ovs_proto, host, port_volume = connection_info['data']['device_path'].split(':')
        port, name = port_volume.split('/')  # 26203/volimage3
        _, transport = ovs_proto.split('+')  # openvstorage+tcp

        conf.source_name = name
        conf.source_host_name = host
        conf.source_host_port = port
        conf.source_host_transport = transport

        conf.target_dev = disk_info['dev']
        conf.target_bus = disk_info['bus']
        conf.serial = connection_info.get('serial')

        return conf

    def connect_volume(self, connection_info, disk_info):
        """Attach the volume to instance_name."""
        LOG.debug("Attached volume {0}".format(connection_info['data']['device_path']))

    def disconnect_volume(self, connection_info, disk_dev):
        """Detach the volume from instance_name."""
        LOG.debug("Detached volume {0}".format(connection_info['data']))
