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


class VPoolHelper(object):
    """
    vDiskHelper class
    """

    LOGGER = LogHandler.get(source="helpers", name="ci_vpool_helper")

    def __init__(self):
        pass

    @staticmethod
    def get_vpool_by_name(vpool_name, api):
        """
        Fetch vpool by vpool name

        :param vpool_name: name of a existing vpool
        :type vpool_name: str
        :param api: specify a valid api connection to the setup
        :type api: ci.helpers.api.OVSClient
        :return: a vpool
        :rtype: dict
        """

        return [vpool for vpool in api.get(api='/vpools',
                                           params={'contents': ''})['data'] if vpool['name'] == vpool_name][0]
