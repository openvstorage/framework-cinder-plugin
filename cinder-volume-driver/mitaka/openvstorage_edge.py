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
- uses libovsvolumedriver calls where needed
"""
import os
import re
import time
from cinder.image import image_utils
from cinder.volume import driver
from oslo_config import cfg
from oslo_log import log as logging
from subprocess import PIPE, Popen
from volumedriver.storagerouter.storagerouterclient import ClusterContact, StorageRouterClient

logger = logging.getLogger(__name__)
options = [cfg.StrOpt(name='storage_ip',
                      help='IP address of a storage node on which the vPool is extended'),
           cfg.StrOpt(name='vpool_guid',
                      help='The GUID of the vPool being used'),
           cfg.StrOpt(name='edge_protocol',
                      default='tcp',
                      help='Protocol to use - edge client'),
           cfg.PortOpt(name='edge_port',
                       help='Port of the edge server'),
           cfg.PortOpt(name='xml_rpc_port',
                       help='XML RPC port used by the StorageDriver python API')]

config = cfg.CONF
config.register_opts(options)


# noinspection PyAbstractClass
class OpenvStorageEdgeBaseVD(driver.BaseVD):
    """
    Open vStorage Edge Volume Driver plugin for Cinder base functionality
    """
    VERSION = '0.0.1'
    OVS_FILE_NAME = '/{0}.raw'

    def __init__(self, *args, **kwargs):
        """
        Init: args, kwargs pass through
        Options come from 'config'
        """
        super(OpenvStorageEdgeBaseVD, self).__init__(*args, **kwargs)
        self.configuration.append_config_values(options)
        self.volume_backend_name = kwargs['host'].split('@')[1]
        self._ip = self.configuration.storage_ip
        self._port = self.configuration.edge_port
        self._protocol = self.configuration.edge_protocol

        # Client can be initialized at initialization time because client is internally re-established for each call
        contact = ClusterContact(self._ip, self.configuration.xml_rpc_port)
        self._sd_client = StorageRouterClient(self.configuration.vpool_guid, [contact])

    def create_volume(self, volume):
        """
        Creates a volume
        Called on "cinder create ..." or "nova volume-create ..."

        :param volume: Volume reference (sqlalchemy Model)
        :type volume: cinder.objects.volume.Volume
        :return: None
        """
        cleaned_name = OpenvStorageEdgeBaseVD._clean_display_name(name=volume.display_name)
        voldrv_path = OpenvStorageEdgeBaseVD.OVS_FILE_NAME.format(cleaned_name)
        # noinspection PyArgumentList
        if voldrv_path in self._sd_client.list_volumes_by_path():
            raise ValueError('Volume already exists. Display name: {0}, cleaned name: {1}'.format(volume.display_name, cleaned_name))

        logger.debug('Creating volume. OpenStack name: {0}, OVS name: {1}'.format(volume.display_name, cleaned_name))
        self._sd_client.create_volume(voldrv_path, None, '{0}B'.format(volume.size * 1024 ** 3))

    def create_volume_from_snapshot(self, volume, snapshot):
        """
        Creates a volume from a snapshot.
        Called on "cinder create --snapshot-id ..."

        :param volume: Volume reference (sqlalchemy Model)
        :type volume: cinder.objects.volume.Volume
        :param snapshot: Snapshot reference (sqlalchemy Model)
        :type snapshot: cinder.objects.snapshot.Snapshot
        :return: None
        """
        # Gather information
        parent_volume_id = self._get_volume_id(volume=snapshot.volume)
        snapshots = self._sd_client.list_snapshots(parent_volume_id)
        cleaned_vol_name = OpenvStorageEdgeBaseVD._clean_display_name(name=volume.display_name)
        cleaned_snap_name = OpenvStorageEdgeBaseVD._clean_display_name(name=snapshot.display_name)
        voldrv_path = OpenvStorageEdgeBaseVD.OVS_FILE_NAME.format(cleaned_vol_name)

        # Validate information
        if cleaned_snap_name not in self._sd_client.list_snapshots(parent_volume_id):
            raise ValueError('Snapshot {0} does not belong to volume {1}'.format(snapshot.display_name, volume.display_name))
        # noinspection PyArgumentList
        if voldrv_path in self._sd_client.list_volumes_by_path():
            raise ValueError('Volume already exists. Display name: {0}, cleaned name: {1}'.format(volume.display_name, cleaned_vol_name))

        # Wait for specified snapshot to be synced to backend
        if len(snapshots) > 0:
            logger.debug('Verifying snapshot synced to backend')
            self._wait_for_snapshot(volume_id=parent_volume_id, snapshot_id=cleaned_snap_name)

        # Create volume from the snapshot
        logger.debug('Creating volume from snapshot. OpenStack name: {0}, OVS name: {1}'.format(volume.display_name, cleaned_vol_name))
        self._sd_client.create_clone(voldrv_path, None, parent_volume_id, cleaned_snap_name)

    def delete_volume(self, volume):
        """
        Deletes a logical volume.
        Called on "cinder delete ... "

        :param volume: Volume reference (sqlalchemy Model)
        :type volume: cinder.objects.volume.Volume
        :return: None
        """
        volume_id = self._get_volume_id(volume=volume)
        snapshots = self._sd_client.list_snapshots(volume_id)
        if len(snapshots) > 0:
            raise RuntimeError('Volume {0} still has snapshots'.format(volume_id))

        cleaned_name = OpenvStorageEdgeBaseVD._clean_display_name(name=volume.display_name)
        # noinspection PyArgumentList
        if OpenvStorageEdgeBaseVD.OVS_FILE_NAME.format(cleaned_name) in self._sd_client.list_volumes_by_path():
            logger.debug('Deleting volume. OpenStack name: {0}, OVS name: {1}'.format(volume.display_name, cleaned_name))
            self._sd_client.unlink('/{0}.raw'.format(cleaned_name))
        else:
            logger.debug('Volume no longer exists in OVS. OpenStack name: {0}, supposedly OVS name: {1}'.format(volume.display_name, cleaned_name))

    def create_snapshot(self, snapshot):
        """
        Creates a snapshot.
        Called on "nova image-create " or "cinder snapshot-create "

        :param snapshot: Snapshot reference (sqlalchemy Model)
        :type snapshot: cinder.objects.snapshot.Snapshot
        :return: None
        """
        # Gather information and validate
        volume_id = self._get_volume_id(volume=snapshot.volume)
        snapshots = self._sd_client.list_snapshots(volume_id)
        cleaned_snap_name = OpenvStorageEdgeBaseVD._clean_display_name(name=snapshot.display_name)
        if cleaned_snap_name in snapshots:
            raise ValueError('Snapshot already exists. OpenStack name: {0}, OVS name: {1}'.format(snapshot.display_name, cleaned_snap_name))

        # Wait for last snapshot to be synced to backend
        if len(snapshots) > 0:
            logger.debug('Verifying last snapshot synced to backend')
            self._wait_for_snapshot(volume_id=volume_id, snapshot_id=snapshots[-1])

        # Create the snapshot
        logger.debug('Creating new snapshot. OpenStack name: {0}, OVS name: {1}'.format(snapshot.display_name, cleaned_snap_name))
        self._sd_client.create_snapshot(volume_id, str(cleaned_snap_name))

    def delete_snapshot(self, snapshot):
        """
        Deletes a snapshot.

        :param snapshot: Snapshot reference (sqlalchemy Model)
        :type snapshot: cinder.objects.snapshot.Snapshot
        :return: None
        """
        volume_id = self._get_volume_id(volume=snapshot.volume)
        cleaned_snap_name = OpenvStorageEdgeBaseVD._clean_display_name(name=snapshot.display_name)
        if cleaned_snap_name in self._sd_client.list_snapshots(volume_id):
            logger.debug('Deleting snapshot. OpenStack name: {0}, OVS name: {1}'.format(snapshot.display_name, cleaned_snap_name))
            self._sd_client.delete_snapshot(volume_id, cleaned_snap_name)
        else:
            logger.debug('Snapshot no longer exists in OVS. OpenStack name: {0}, supposedly OVS name: {1}'.format(snapshot.display_name, cleaned_snap_name))

    def get_volume_stats(self, refresh=False):
        """
        Get volume stats.

        :param refresh: Refresh the stats (Not implemented)
        :type refresh: bool
        :return: Volume statistics
        :rtype: dict
        """
        _ = refresh
        return {'volume_backend_name': self.volume_backend_name,
                'vendor_name': 'Open vStorage',
                'driver_version': OpenvStorageEdgeBaseVD.VERSION,
                'storage_protocol': 'openvstorage_edge',
                'total_capacity_gb': 'unknown',
                'free_capacity_gb': 'unknown',
                'reserved_percentage': 0,
                'QoS_support': False}

    def copy_image_to_volume(self, context, volume, image_service, image_id):
        """
        Fetch the image from image_service and write it to the volume.
        Called on "nova volume-create --image-id ..." or "cinder create --image-id"
        Downloads image from glance server into volume

        :param context: Context object
        :type context: cinder.context
        :param volume: Volume reference (sqlalchemy Model)
        :type volume: cinder.objects.volume.Volume
        :param image_service: Image service reference
        :type image_service: glance.cmd.replicator.ImageService
        :param image_id: ID of the image
        :type image_id: str
        :return: None
        """
        cleaned_name = OpenvStorageEdgeBaseVD._clean_display_name(name=volume.display_name)
        location = 'openvstorage+{0}:{1}:{2}/{3}'.format(self._protocol, self._ip, self._port, cleaned_name)
        image_path = os.path.join('/tmp', image_id)
        if not os.path.exists(image_path):
            logger.debug('Downloading image to temporary location {0}'.format(image_path))
            image_utils.fetch_to_raw(context=context,
                                     image_service=image_service,
                                     image_id=image_id,
                                     dest=image_path,
                                     blocksize='1M',
                                     size=volume.size)
        logger.debug('Creating volume from image at location: {0}'.format(location))
        OpenvStorageEdgeBaseVD._execute_qemu_command(parameters=['convert', '-n', '-O', 'raw', image_path, location])

    def extend_volume(self, volume, new_size):
        """
        Extend volume to the new size.
        """
        raise NotImplementedError('Method "extend_volume" not implemented')

    def copy_volume_to_image(self, context, volume, image_service, image_meta):
        """
        Copy the volume to the specified image.
        """
        raise NotImplementedError('Method "copy_volume_to_image" not implemented')

    # Prevent NotImplementedError being raised
    # Not actually implemented, these actions do not make sense for this driver
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

    def initialize_connection(self, volume, connector, initiator_data=None):
        """
        Allow connection to connector and return connection info.
        """
        return

    def create_export(self, context, volume, connector=None):
        """
        Exports the volume.
        """
        pass

    def remove_export(self, context, volume):
        """
        Removes an export for a volume.
        """
        return

    def ensure_export(self, context, volume):
        """
        Synchronously recreates an export for a volume.
        """
        pass

    def terminate_connection(self, volume, connector, **kwargs):
        """
        Disallow connection from connector.
        """
        return

    def attach_volume(self, context, volume, instance_uuid, host_name, mountpoint):
        """
        Callback for volume attached to instance or host.
        """
        pass

    def detach_volume(self, context, volume, attachment=None):
        """
        Callback for volume detached.
        """
        pass

    ##################
    # HELPER METHODS #
    ##################
    def _get_volume_id(self, volume):
        """
        Retrieve the volume ID used by the OpenvStorage StorageDriver
        :param volume: The OpenStack volume object
        :type volume: cinder.objects.volume.Volume
        :return: The volume ID known by the StorageDriver
        :rtype: str
        """
        cleaned_name = OpenvStorageEdgeBaseVD._clean_display_name(name=volume.display_name)
        ovs_path = OpenvStorageEdgeBaseVD.OVS_FILE_NAME.format(cleaned_name)
        volume_id = self._sd_client.get_volume_id(ovs_path)
        if volume_id is None:
            raise ValueError('Volume with path {0} could not be found in OVS'.format(ovs_path))
        return volume_id

    def _wait_for_snapshot(self, volume_id, snapshot_id):
        """
        Waits for a given snapshot to be available in the backend

        :param volume_id: ID of the volume to check
        :type volume_id: str
        :param snapshot_id: ID of the snapshot to check
        :type snapshot_id: str
        :return: True if the snapshot has been synced to backend, false otherwise
        :rtype: bool
        """
        tries = 60
        while tries > 0:
            if self._sd_client.is_volume_synced_up_to_snapshot(volume_id, snapshot_id) is True:
                return True
            tries -= 1
            time_to_sleep = 60 - tries
            logger.debug('Snapshot {0} for volume {1} not yet synced to backend, sleeping {2} seconds'.format(snapshot_id, volume_id, time_to_sleep))
            time.sleep(time_to_sleep)
        if tries == 0:
            raise RuntimeError('Snapshot {0} did not become available on the backend in due time'.format(snapshot_id))

    @staticmethod
    def _clean_display_name(name):
        """
        Change the name to be allowed to be used by OpenvStorage
        :param name: Name to clean
        :type name: str
        :return: Cleaned volume name
        :rtype: str
        """
        name = str(name.strip('/').replace(' ', '_').lower())
        while '//' in name:
            name = name.replace('//', '/')
        name = re.compile('[^/\w\-.]+').sub('', name)
        match = re.compile('([/\w\-.]+)\.[a-z]{3,4}$').search(name)
        if match is None:
            name = name.rstrip('.')
        else:
            name = match.groups()[0]
        return name

    @staticmethod
    def _execute_qemu_command(parameters):
        """
        Executes qemu-img command wrapper

        :param parameters: Parameters to pass on the command-line to the QEMU-IMG command
        :type parameters: list
        :return: Exit code of the command
        :rtype: int
        """
        command = ['env', 'LC_ALL=C', 'LANG=C', 'qemu-img'] + parameters
        logger.debug('Executing command: {0}'.format(command))
        try:
            channel = Popen(command, stdout=PIPE, stderr=PIPE)
        except OSError as ose:
            logger.error(ose)
            raise
        stdout, stderr = channel.communicate()
        exit_code = channel.returncode
        if exit_code != 0:
            raise Exception('Command {0} failed with error message {1}'.format(command, stderr))

        logger.debug('Output of command: {0}'.format(stdout.strip()))
        return stdout.strip()
