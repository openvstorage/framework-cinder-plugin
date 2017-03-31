# NOVA

## Description

The custom NOVA driver provides the ability to generate custom Open vStorage XML files for Libvirt.

**IMPORTANT:** These files must be patched on machines where `nova-compute` is installed. Preferably under their own directories.

## Driver

The NOVA driver can be found under `virt/libvirt/volume` and should be installed under its respective directory.
After installing the driver, you should restart `nova-compute`.

## Patches

### Config.py

Here we've patched the `virt/libvirt/config.py` of nova. This makes it possible for us to deploy a XML with Open vStorage configuration.

Source: `https://github.com/openstack/nova/blob/master/nova/virt/libvirt/config.py`

line 904

```
class LibvirtConfigOpenvStorageEdgeGuestDisk(LibvirtConfigGuestDisk):
    def __init__(self, **kwargs):
        super(LibvirtConfigGuestDisk, self).__init__(root_name="disk", **kwargs)
        self.source_type = "network"
        self.source_device = "disk"
        self.driver_name = 'qemu'
        self.driver_type = 'raw'
        # https://specs.openstack.org/openstack/nova-specs/specs/juno/implemented/libvirt-disk-discard-option.html#proposed-change
        self.driver_discard = 'ignore'
        self.source_protocol = "openvstorage"
        self.source_name = None
        self.source_snapshot_timeout = '120'
        self.source_host_name = None
        self.source_host_port = None
        self.source_host_transport = 'tcp'
        self.target_dev = 'vda'
        self.target_bus = 'virtio'

    def format_dom(self):
        """
        Example
        <disk type='network' device='disk'>
            <driver name='qemu' type='raw'/>
            <source protocol='openvstorage' name='vol1' snapshot-timeout='120'>
                <host name='ovs.include.gr' port='12329' transport='rdma'/>
            </source>
            <target dev='vda' bus='virtio'/>
        </disk>
        @return:
        """
        dev = super(LibvirtConfigGuestDisk, self).format_dom()

        dev.set("type", self.source_type)
        dev.set("device", self.source_device)
        drv = etree.Element("driver",
                            name = self.driver_name,
                            type = self.driver_type)
        dev.append(drv)
        source = etree.Element("source",
                               protocol=self.source_protocol,
                               snapshot_timeout=self.source_snapshot_timeout)
        etree.SubElement(source, "host",
                         name=self.source_host_name,
                         port=self.source_host_port,
                         transport=self.source_host_transport)
        if self.source_name is not None:
            source.set('name', self.source_name)
        dev.append(source)

        dev.append(etree.Element("target",
                                 dev=self.target_dev,
                                 bus=self.target_bus))
        return dev

    def parse_dom(self, xmldoc):

        self.source_type = xmldoc.get('type')

        for c in xmldoc.getchildren():
            if c.tag == 'driver':
                self.driver_name = c.get('name')
                self.driver_format = c.get('type')
            elif c.tag == 'source':
                self.source_protocol = c.get('protocol')
                self.source_name = c.get('name')
                self.source_snapshot_timeout = c.get('snapshot-timeout')
                for sub in c.getchildren():
                    if sub.tag == 'host':
                        self.source_host_name = sub.get('name')
                        self.source_host_port = sub.get('port')
                        self.source_host_transport = sub.get('transport')
            elif c.tag == 'target':
                self.target_dev = c.get('dev')
                self.target_bus = c.get('bus', None)
```

### Driver.py

Here we've patched the `virt/libvirt/driver.py` of nova, this makes it possible to call the `LibvirtOpenvStorageEdgeVolumeDriver` volume module.
This module calls `os_brick` to connect & disconnect volumes to instances.

Source: `https://github.com/openstack/nova/blob/master/nova/virt/libvirt/driver.py`

line 148

```
You should add a libvirt_volume_driver to the list called:

openvstorage_edge=nova.virt.libvirt.volume.openvstorage_edge.LibvirtOpenvStorageEdgeVolumeDriver
```