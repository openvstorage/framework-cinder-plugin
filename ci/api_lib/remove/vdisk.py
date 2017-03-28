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
from ..helpers.vdisk import VDiskHelper


class VDiskRemover(object):

    LOGGER = LogHandler.get(source="remove", name="ci_vdisk_remover")
    REMOVE_SNAPSHOT_TIMEOUT = 60
    REMOVE_VTEMPLATE_TIMEOUT = 60

    def __init__(self):
        pass

    @staticmethod
    def remove_snapshot(snapshot_name, vpool_guid, api, timeout=REMOVE_SNAPSHOT_TIMEOUT):
        """
        Remove a existing snapshot from a existing vdisk

        :param snapshot_name: name of a snapshot
        :type snapshot_name: str
        :param api: specify a valid api connection to the setup
        :type api: helpers.api.OVSClient
        :param timeout: time to wait for the task to complete
        :type timeout: int
        :param vpool_guid: name of a existing vpool
        :type vpool_guid: str
        :return: if success
        :rtype: bool
        """
        snapshot, vdisk_guid, vdisk_name = VDiskHelper.get_snapshot_by_name(snapshot_name=snapshot_name,
                                                                            vpool_guid=vpool_guid, api=api)

        data = {"snapshot_id": snapshot['guid']}
        task_guid = api.post(
            api='/vdisks/{0}/remove_snapshot/'.format(vdisk_guid),
            data=data
        )
        task_result = api.wait_for_task(task_id=task_guid, timeout=timeout)

        if not task_result[0]:
            error_msg = "Deleting snapshot `{0}` for vdisk `{1}` has failed".format(snapshot['guid'], vdisk_name)
            VDiskRemover.LOGGER.error(error_msg)
            raise RuntimeError(error_msg)
        else:
            VDiskRemover.LOGGER.info("Deleting snapshot `{0}` for vdisk `{1}` should have succeeded"
                                     .format(snapshot['guid'], vdisk_name))
            return True
