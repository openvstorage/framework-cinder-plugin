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

import ConfigParser
import random
import sys

from os_brick.initiator import connector

from oslo_log import log as logging

from nova import utils
from nova.virt.libvirt.volume.volume import LibvirtVolumeDriver
from nova.virt.libvirt import config as vconfig
from nova.virt.libvirt import utils as libvirt_utils

# Open vStorage imports

OVS_DIR = "/opt/OpenvStorage"
sys.path.append(OVS_DIR)

from ci.api_lib.helpers.api import OVSClient
from ci.api_lib.helpers.vpool import VPoolHelper
from ci.api_lib.helpers.vdisk import VDiskHelper

LOG = logging.getLogger(__name__)

# Parse nova config yourself instead of using oslo
NOVA_CFG_LOC = "/etc/nova/nova.conf"
NOVA_CFG = ConfigParser.ConfigParser()
NOVA_CFG.read(NOVA_CFG_LOC)


class LibvirtOpenvStorageEdgeVolumeDriver(LibvirtVolumeDriver):
    """
    Class for volumes backed by OpenvStorage Edge
    """

    VOLUME_PREFIX = "volume-"
    LIBVIRT_MODULE = "openvstorage"

    def __init__(self, connection):
        super(LibvirtOpenvStorageEdgeVolumeDriver, self).__init__(connection)
        self.connector = connector.InitiatorConnector.factory('OPENVSTORAGE_EDGE', utils.get_root_helper())
        LOG.debug("libovsvolumedriver.init")

    @staticmethod
    def _get_management_ip(section_name):
        """
        Returns a available ip address to contact Open vStorage MASTER NODE
        Currently a random ip is given. In the future this could be HA tested

        :param section_name: name of the section you want to fetch the management IP from
        :type section_name: str
        :return: management ip
        :rtype: str
        """

        return random.choice(NOVA_CFG.get(section_name, 'management_ips').split(','))

    def _setup_ovs_client(self, section_name):
        """
        Sets up a OVSClient to contact the Open vStorage API

        :param section_name: name of the section you want to fetch the management IP from
        :type section_name: str
        :return: api client
        :return: ci.api_lib.helpers.api.OVSClient
        """

        return OVSClient(ip=self._get_management_ip(section_name=section_name),
                         username=NOVA_CFG.get(section_name, 'username'),
                         password=NOVA_CFG.get(section_name, 'password'))

    def _get_volume_location(self, volume_name, vpool_name, api):
        """
        Return volume location for edge client

        :param volume_name: name of a volume without .raw, .vmdk
        :type volume_name: str
        :param vpool_name: name of a existing vpool
        :type vpool_name: str
        :
        :return: volume location
        :rtype: str
        """

        vpool_guid = VPoolHelper.get_vpool_by_name(vpool_name=vpool_name, api=api)['guid']
        protocol, uri, port = VDiskHelper.get_vdisk_location_by_name(vdisk_name=volume_name, vpool_guid=vpool_guid,
                                                                     api=api)['cluster_node_config']['network_server_uri'].split(':')
        return "{0}+{1}:{2}:{3}/{4}".format(self.LIBVIRT_MODULE, protocol, uri.replace('/', ''), port, volume_name)

    def get_config(self, connection_info, disk_info):
        """
        Returns xml for libvirt.
        """
        conf = vconfig.LibvirtConfigOpenvStorageEdgeGuestDisk()
        conf.driver_name = libvirt_utils.pick_disk_driver_name(self.connection._host.get_version(),
                                                               self.is_block_dev)
        LOG.debug("libovsvolumedriver.libvirt.get_config {0} {1}".format(connection_info, disk_info))

        # u'device_path': u'openvstorage+tcp:10.130.11.202:26203/volimage3'
        if connection_info['data']['device_path'] is not None:
            device_path = connection_info['data']['device_path']
        else:
            # this is probably a cloned volume with no device path
            vpool_name = connection_info['volume_backend_name']
            volume_name = self.VOLUME_PREFIX + connection_info['serial']
            api = self._setup_ovs_client(section_name=vpool_name)
            # query volume details in Open vStorage
            device_path = self._get_volume_location(volume_name=volume_name, vpool_name=vpool_name, api=api)

        ovs_proto, host, port_volume = device_path.split(':')
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
        LOG.debug("Detacched volume {0}".format(connection_info['data']))
