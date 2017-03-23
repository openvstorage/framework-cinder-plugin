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


class StoragerouterHelper(object):
    """
    StoragerouterHelper class
    """

    LOGGER = LogHandler.get(source="helpers", name="ci_storagerouter_helper")

    def __init__(self):
        pass

    @staticmethod
    def get_storagerouters(api):
        """
        Fetches the storagerouters and some meta information

        :param api: specify a valid api connection to the setup
        :type api: ci.helpers.api.OVSClient
        :return: a dict like this:
        {'10.100.199.191': {'machine_id': str, 'guid': str, 'node_type': str, 'vpools_guids': list}}
        :rtype: dict
        """
        data = api.get(api='/storagerouters', params={'contents': 'vpools_guids'})['data']

        # cleanup to much data from api call
        storagerouters = {}
        for storagerouter in data:
            storagerouters[storagerouter['ip']] = {
                'machine_id': storagerouter['machine_id'],
                'guid': storagerouter['guid'],
                'node_type': storagerouter['node_type'],
                'vpools_guids': storagerouter['vpools_guids']
            }
        return storagerouters

    @staticmethod
    def get_storagerouter_guid_by_ip(storagerouter_ip, api):
        """
        Fetches a storagerouter guid by storagerouter ip

        :param storagerouter_ip: storagerouter ip
        :type storagerouter_ip: str
        :param api: specify a valid api connection to the setup
        :type api: ci.helpers.api.OVSClient
        :return: storagerouter guid
        :rtype: str
        """

        data = StoragerouterHelper.get_storagerouters(api=api)
        if not data.get(storagerouter_ip):
            raise RuntimeError("No storagerouter with ip {0} was found".format(storagerouter_ip))
        else:
            return data.get(storagerouter_ip)['guid']
