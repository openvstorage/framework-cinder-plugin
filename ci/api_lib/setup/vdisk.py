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
from ..helpers.storagerouter import StoragerouterHelper
from ..helpers.vdisk import VDiskHelper


class VDiskSetup(object):

    LOGGER = LogHandler.get(source="setup", name="ci_vdisk_setup")
    CREATE_SNAPSHOT_TIMEOUT = 60
    CREATE_VDISK_TIMEOUT = 60
    CREATE_CLONE_TIMEOUT = 60
    SET_VDISK_AS_TEMPLATE_TIMEOUT = 60
    ROLLBACK_VDISK_TIMEOUT = 60
    SET_CONFIG_VDISK_TIMEOUT = 60

    def __init__(self):
        pass

    @staticmethod
    def create_clone(vpool_guid, new_vdisk_name, storagerouter_ip, api, timeout=CREATE_CLONE_TIMEOUT,
                     snapshot_name=None, vdisk_name=None):
        """
        Create a new vDisk on a certain vPool/storagerouter

        :param vdisk_name: location of a vdisk on a vpool
                           (e.g. /mnt/vpool/test.raw = test, /mnt/vpool/volumes/test.raw = volumes/test )
        :type vdisk_name: str
        :param vpool_guid: guid of a existing vpool
        :type vpool_guid: str
        :param new_vdisk_name: location of the NEW vdisk on the vpool
                           (e.g. /mnt/vpool/test.raw = test, /mnt/vpool/volumes/test.raw = volumes/test )
        :type new_vdisk_name: str
        :param storagerouter_ip: ip address of a existing storagerouter where the clone will be deployed
        :type storagerouter_ip: str
        :param api: specify a valid api connection to the setup
        :type api: ci.helpers.api.OVSClient
        :param timeout: time to wait for the task to complete
        :type timeout: int
        :param snapshot_name: name of a existing snapshot (DEFAULT=None -> will create new snapshot)
        :type snapshot_name: str
        :return: details about cloned vdisk e.g
        {u'backingdevice': u'/test2.raw',
         u'name': u'test2',
         u'vdisk_guid': u'c4414c07-3796-4dcd-96a1-2cb00f4dc82b'}
        :rtype: dict
        """
        storagerouter_guid = StoragerouterHelper.get_storagerouter_guid_by_ip(storagerouter_ip=storagerouter_ip,
                                                                              api=api)
        if not snapshot_name:
            vdisk_guid = VDiskHelper.get_vdisk_guid_by_name(vdisk_name=vdisk_name, vpool_guid=vpool_guid, api=api)
            data = {"name": new_vdisk_name,
                    "storagerouter_guid": storagerouter_guid}
        else:
            snapshot, vdisk_guid = VDiskHelper.get_snapshot_by_name(snapshot_name=snapshot_name,
                                                                    vpool_guid=vpool_guid, api=api)
            data = {"name": new_vdisk_name,
                    "storagerouter_guid": storagerouter_guid,
                    "snapshot_id": snapshot.get('guid')}

        task_guid = api.post(
            api='/vdisks/{0}/clone'.format(vdisk_guid),
            data=data
        )
        task_result = api.wait_for_task(task_id=task_guid, timeout=timeout)

        if not task_result[0]:
            error_msg = "Creating clone `{0}` on vPool `{1}` on storagerouter `{2}` has failed with error {3}"\
                .format(vdisk_name, vpool_guid, storagerouter_ip, task_result[1])
            VDiskSetup.LOGGER.error(error_msg)
            raise RuntimeError(error_msg)
        else:
            VDiskSetup.LOGGER.info("Creating clone `{0}` on vPool `{1}` on storagerouter `{2}` should have succeeded"
                                   .format(vdisk_name, vpool_guid, storagerouter_ip))
            return task_result[1]
