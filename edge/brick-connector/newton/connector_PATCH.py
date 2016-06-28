#https://github.com/openstack/os-brick/blob/master/os_brick/initiator/connector.py

#line 92
OPENVSTORAGE_EDGE = "OPENVSTORAGE_EDGE"

#line 93
connector_list = [
        'os.brick.initiator.connector.OpenvStorageEdgeConnector',
        #...


#line 279
elif protocol == OPENVSTORAGE_EDGE:
    return OpenvStorageEdgeConnector(root_helper=root_helper,
                                     driver=driver,
                                     device_scan_attempts=device_scan_attempts,
                                     *args, **kwargs)

#line 427:
class OpenvStorageEdgeConnector(InitiatorConnector):
    ... TODO ...


