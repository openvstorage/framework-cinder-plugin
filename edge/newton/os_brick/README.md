# OS BRICK

## Description

The custom OS_BRICK connectors provide a connection between nova & cinder driver.

**IMPORTANT:** These files must be patched on machines where `cinder-volume` & `nova-compute` are installed. Preferably under their own directories.

## Patches

Here you can find detailed information about the patches. Although these are provided, 
the patched `initiator/connector.py` can be found in this directory.

OS_BRICK main `initiator/connector.py` : `https://github.com/openstack/os_brick/blob/master/os_brick/initiator/connector.py`
Open vStorage custom connector: `initiator/connectors/openvstorage.py`

After installation of these patches, you should restart the following services: 
* nova-compute
* cinder-volume

### line 85
OPENVSTORAGE_EDGE = "OPENVSTORAGE_EDGE"

### line 93
"""
connector_list = [
        'os_brick.initiator.connectors.openvstorage.OpenvStorageEdgeConnector',
        #...
        ]
"""

### line 277
"""
        elif protocol == OPENVSTORAGE_EDGE:
            return OpenvStorageEdgeConnector(root_helper=root_helper,
                                             driver=driver,
                                             device_scan_attempts=device_scan_attempts,
                                             *args, **kwargs)
"""
