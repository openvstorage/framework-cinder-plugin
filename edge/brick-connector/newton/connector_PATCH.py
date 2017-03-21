# https://github.com/openstack/os_brick/blob/master/os_brick/initiator/connector.py

# line 85
OPENVSTORAGE_EDGE = "OPENVSTORAGE_EDGE"

# line 93
"""
connector_list = [
        'os.brick.initiator.connector.OpenvStorageEdgeConnector',
        #...

"""

# line 277
"""
        elif protocol == OPENVSTORAGE_EDGE:
            return OpenvStorageEdgeConnector(root_helper=root_helper,
                                             driver=driver,
                                             device_scan_attempts=device_scan_attempts,
                                             *args, **kwargs)
"""
