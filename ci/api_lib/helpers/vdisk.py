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

    LOGGER = LogHandler.get(source="setup", name="ci_vdisk_setup")

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
        :return: a storage ip
        :rtype: str
        """
        storagedrivers = StoragedriverHelper.get_storagedrivers_by_vpoolguid(vpool_guid=vpool_guid, api=api)
        storagedriver_id = VDiskHelper.get_vdisk_by_name(vdisk_name=vdisk_name, vpool_guid=vpool_guid, api=api)['storagedriver_id']
        return [sd['storage_ip'] for sd in storagedrivers if sd['storagedriver_id'] == storagedriver_id][0]

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
        :param api: specify a valid api connection to the setup
        :type api: ci.helpers.api.OVSClient
        :return: a vdisk
        :rtype: dict
        """
        return [vdisk for vdisk in api.get(api='/vdisks',
                                           params={'contents': 'storagedriver_id', 'vpoolguid': vpool_guid})['data']
                if vdisk['name'] == vdisk_name][0]
