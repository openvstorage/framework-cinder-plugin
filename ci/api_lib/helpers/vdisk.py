# Copyright (C) 2016 iNuron NV
#
# This file is part of Open vStorage Open Source Edition (OSE),
# as available from
#
#      http://www.openvstorage.org and
#      http://www.openvstorage.com.
#
# This file is free software; you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License v3 (GNU AGPLv3)
# as published by the Free Software Foundation, in version 3 as it comes
# in the LICENSE.txt file of the Open vStorage OSE distribution.
#
# Open vStorage is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY of any kind.

from ..helpers.log_handler import LogHandler
from ..helpers.storagedriver import StoragedriverHelper


class VDiskHelper(object):
    """
    vDiskHelper class
    """

    LOGGER = LogHandler.get(source="helpers", name="ci_vdisk_helper")

    def __init__(self):
        pass

    @staticmethod
    def get_vdisk_guid_by_name(vdisk_name, vpool_guid, api):
        """
        Fetch vdisk guid by vdisk name

        :param vdisk_name: location of a vdisk on the vpool
        :type vdisk_name: str
        :param vpool_guid: guid of a existing vpool
        :type vpool_guid: str
        :param api: specify a valid api connection to the setup
        :type api: ci.helpers.api.OVSClient
        :return: a vdisk guid
        :rtype: str
        """

        return VDiskHelper.get_vdisk_by_name(vdisk_name=vdisk_name, vpool_guid=vpool_guid, api=api)['guid']

    @staticmethod
    def get_vdisk_location_by_name(vdisk_name, vpool_guid, api):
        """
        Fetch vdisk location AKA storage_ip by vdisk name

        :param vdisk_name: location of a vdisk on the vpool
        :type vdisk_name: str
        :param vpool_guid: guid of a existing vpool
        :type vpool_guid: str
        :param api: specify a valid api connection to the setup
        :type api: ci.helpers.api.OVSClient
        :return: a dict of a storagedriver
        {u'cluster_ip': u'10.100.199.192',
         u'cluster_node_config': {u'failovercache_host': u'10.100.199.192',
          u'failovercache_port': 26208,
          u'host': u'10.100.199.192',
          u'message_port': 26206,
          u'network_server_uri': u'tcp://10.100.199.192:26209',
          u'node_distance_map': {u'myvpool01UzU8PHIryg5Y4e5b': 10000,
           u'myvpool01t73EUyATNxpzfUvE': 10000},
          u'vrouter_id': u'myvpool014CCmf5mMoqd22tPW',
          u'xmlrpc_host': u'10.100.199.192',
          u'xmlrpc_port': 26207},
         u'description': u'myvpool014CCmf5mMoqd22tPW',
         u'guid': u'adbff642-ba97-4ebb-9ee3-56cb19f7fc97',
         u'mountpoint': u'/mnt/myvpool01',
         u'name': u'myvpool014CCmf5mMoqd22tPW',
         u'ports': {u'dtl': 26208,
          u'edge': 26209,
          u'management': 26206,
          u'xmlrpc': 26207},
         u'startup_counter': 1,
         u'storage_ip': u'10.100.199.192',
         u'storagedriver_id': u'myvpool014CCmf5mMoqd22tPW'}
        :rtype: dict
        """
        storagedrivers = StoragedriverHelper.get_storagedrivers_by_vpoolguid(vpool_guid=vpool_guid, api=api)
        storagedriver_id = VDiskHelper.get_vdisk_by_name(vdisk_name=vdisk_name, vpool_guid=vpool_guid, api=api)['storagedriver_id']
        return [sd for sd in storagedrivers if sd['storagedriver_id'] == storagedriver_id][0]

    @staticmethod
    def get_vdisk_by_name(vdisk_name, vpool_guid, api):
        """
        Fetch vdisk guid by vdisk name

        :param vdisk_name: location of a vdisk on the vpool
        :type vdisk_name: str
        :param vpool_guid: guid of a existing vpool
        :type vpool_guid: str
        :param api: specify a valid api connection to the setup
        :type api: ci.helpers.api.OVSClient
        :return: a vdisk
        {u'cinder_id': None,
         u'description': None,
         u'devicename': u'/volume-3a78def9-c92e-47a0-9343-3c05888eea30.raw',
         u'guid': u'7a5bfcd2-e6d4-455f-aa0f-ab1b4878db59',
         u'has_manual_dtl': False,
         u'metadata': {u'cluster_multiplier': 8, u'lba_size': 512},
         u'name': u'volume-3a78def9-c92e-47a0-9343-3c05888eea30',
         u'pagecache_ratio': 1.0,
         u'parentsnapshot': None,
         u'size': 1073741824,
         u'storagedriver_id': u'myvpool014CCmf5mMoqd22tPW',
         u'volume_id': u'c42d5dbb-d1d9-4fa6-b626-41b72ab046e2'}
        :rtype: dict
        """
        return [vdisk for vdisk in VDiskHelper.list_vdisks(vpool_guid=vpool_guid, api=api, contents='storagedriver_id')
                if vdisk['name'] == vdisk_name][0]

    @staticmethod
    def list_vdisks(vpool_guid, api, contents=''):
        """
        Lists the vdisks with a optional extra content

        :param vpool_guid: guid of a existing vpool
        :type vpool_guid: str
        :param api: specify a valid api connection to the setup
        :type api: ci.helpers.api.OVSClient
        :param contents: optional extra content
        :type contents: str
        :return:
        """

        return api.get(api='/vdisks', params={'contents': contents, 'vpoolguid': vpool_guid})['data']

    @staticmethod
    def get_snapshot_by_name(snapshot_name, vpool_guid, api):
        """
        Fetch snapshot by snapshot_name

        :param snapshot_name: name of a existing snapshot
        :type snapshot_name: str
        :param vpool_guid: guid of a existing vpool
        :type vpool_guid: str
        :param api: specify a valid api connection to the setup
        :type api: ci.helpers.api.OVSClient
        :param api: specify a valid api connection to the setup
        :type api: ci.helpers.api.OVSClient
        :return: vdisk name & snapshot
        ({u'guid': u'61d57466-1912-441f-b672-10f983f9051d',
          u'in_backend': True,
          u'is_automatic': False,
          u'is_consistent': False,
          u'is_sticky': False,
          u'label': u'bla',
          u'stored': 0,
          u'timestamp': u'1490605267'},
         u'3a78def9-c92e-47a0-9343-3c05888eea30')
        :rtype: tuple
        """
        vdisks = VDiskHelper.list_vdisks(vpool_guid=vpool_guid, api=api, contents='snapshots')
        return next((snapshot, vdisk['guid']) for vdisk in vdisks for snapshot in vdisk['snapshots']
                    if snapshot["label"] == snapshot_name)
