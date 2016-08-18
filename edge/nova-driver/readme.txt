openvstorage_edge.py -> https://github.com/openstack/nova/tree/master/nova/virt/libvirt/volume
DEVSTACK: /opt/stack/nova/nova/virt/libvirt/volume/openvstorage_edge.py
OPENSTACK: /usr/lib/python2.7/dist-packages/nova/virt/libvirt/volume/openvstorage_edge.py


###
PATCH:
https://github.com/openstack/nova/blob/master/nova/virt/libvirt/driver.py

DEVSTACK: /opt/stack/nova/nova/virt/libvirt/driver.py
OPENSTACK: /usr/lib/python2.7/dist-packages/nova/virt/libvirt/driver.py

line 147:
 'openvstorage_edge=nova.virt.libvirt.volume.openvstorage_edge.LibvirtOpenvStorageEdgeVolumeDriver'


