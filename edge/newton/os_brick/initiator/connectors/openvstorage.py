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

from oslo_log import log as logging
from oslo_utils import fileutils

from os_brick.initiator import initiator_connector

LOG = logging.getLogger(__name__)
DEVICE_SCAN_ATTEMPTS_DEFAULT = 3


class OpenvStorageEdgeConnector(initiator_connector.InitiatorConnector):
    def __init__(self, root_helper, driver=None, execute=None,
                 device_scan_attempts=DEVICE_SCAN_ATTEMPTS_DEFAULT,
                 *args, **kwargs):
        super(OpenvStorageEdgeConnector, self).__init__(root_helper, execute=execute,
                                                       *args, **kwargs)

    @staticmethod
    def get_connector_properties(root_helper, *args, **kwargs):
        """The generic connector properties."""
        return {}

    def check_valid_device(self, path, run_as_root=True):
        """Test to see if the device path is a real device.
        :param path: The file system path for the device.
        :type path: str
        :param run_as_root: run the tests as root user?
        :type run_as_root: bool
        :returns: bool
        """
        LOG.debug('OVSEdgeConnector check_valid_device {0}'.format(path))

    def connect_volume(self, connection_properties):
        """Connect to a volume.
        The connection_properties describes the information needed by
        the specific protocol to use to make the connection.
        The connection_properties is a dictionary that describes the target
        volume.  It varies slightly by protocol type (iscsi, fibre_channel),
        but the structure is usually the same.
        :param connection_properties: The dictionary that describes all
                                      of the target volume attributes.
        :type connection_properties: dict
        :returns: dict
        """
        LOG.debug('OVSEdgeConnector connect_volume {0}'.format(connection_properties))
        device_info = {'type': 'openvstorage_edge',
                       'path': connection_properties['device_path']}

        return device_info

    def disconnect_volume(self, connection_properties, device_info):
        """Disconnect a volume from the local host.
        The connection_properties are the same as from connect_volume.
        The device_info is returned from connect_volume.
        :param connection_properties: The dictionary that describes all
                                      of the target volume attributes.
        :type connection_properties: dict
        :param device_info: historical difference, but same as connection_props
        :type device_info: dict
        """
        LOG.debug('OVSEdgeConnector disconnect_volume {0} {1}'.format(connection_properties, device_info))

    def get_volume_paths(self, connection_properties):
        """Return the list of existing paths for a volume.
        The job of this method is to find out what paths in
        the system are associated with a volume as described
        by the connection_properties.
        :param connection_properties: The dictionary that describes all
                                      of the target volume attributes.
        :type connection_properties: dict
        """
        LOG.debug('OVSEdgeConnector get_volume_paths {0}'.format(connection_properties))
        path = connection_properties['device_path']
        return [path]

    def get_search_path(self):
        """Return the directory where a Connector looks for volumes.
        Some Connectors need the information in the
        connection_properties to determine the search path.
        """
        LOG.debug('OVSEdgeConnector get_search_path > returning None')
        return None

    def extend_volume(self, connection_properties):
        """Update the attached volume's size.
        This method will attempt to update the local hosts's
        volume after the volume has been extended on the remote
        system.  The new volume size in bytes will be returned.
        If there is a failure to update, then None will be returned.
        :param connection_properties: The volume connection properties.
        :returns: new size of the volume.
        """
        LOG.debug('OVSEdgeConnector extend_volume {0}'.format(connection_properties))

    def get_all_available_volumes(self, connection_properties=None):
        """Return all volumes that exist in the search directory.
        At connect_volume time, a Connector looks in a specific
        directory to discover a volume's paths showing up.
        This method's job is to return all paths in the directory
        that connect_volume uses to find a volume.
        This method is used in coordination with get_volume_paths()
        to verify that volumes have gone away after disconnect_volume
        has been called.
        :param connection_properties: The dictionary that describes all
                                      of the target volume attributes.
        :type connection_properties: dict
        """
        LOG.debug('OVSEdgeConnector get_all_available_volumes {0}'.format(connection_properties))
        return []
