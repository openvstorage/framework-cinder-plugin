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


class StoragedriverHelper(object):
    """
    StoragedriverHelper class
    """

    LOGGER = LogHandler.get(source="helpers", name="ci_storagedriver_helper")

    def __init__(self):
        pass

    @staticmethod
    def get_storagedrivers_by_vpoolguid(vpool_guid, api):
        """
        Fetches the storagedrivers and their details through a vpool_guid

        :param vpool_guid: guid of a existing vpool
        :type vpool_guid: str
        :param api: specify a valid api connection to the setup
        :type api: ci.helpers.api.OVSClient
        :return: a list with dicts like this:
          [{u'cluster_ip': u'10.100.199.192',
            u'cluster_node_config': {u'failovercache_host': u'10.100.199.192',
            u'failovercache_port': 26208,
            u'host': u'10.100.199.192',
            u'message_port': 26206,
            u'network_server_uri': u'tcp://10.100.199.192:26209',
            u'node_distance_map': {u'myvpool01UrpSne6PNIRGTer3': 10000,
            u'myvpool01UzU8PHIryg5Y4e5b': 10000,
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
            u'storagedriver_id': u'myvpool014CCmf5mMoqd22tPW'}]
        :rtype: list
        """
        data = api.get(api='/storagedrivers', params={'vpool_guid': vpool_guid,
                                                      'contents': 'cluster_node_config'})['data']
        return data
