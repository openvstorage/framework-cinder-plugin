# Installing OpenvStorage in OpenStack

## Description
This guide describes how to install OpenvStorage in OpenStack.

Before we begin, I want to mention that the directories that are present in this document can differ with the reality as every openstack distribution is different. 
Nevertheless once you get a hold of it, the main directories do not differ that much.

https://github.com/openvstorage/framework-cinder-plugin/issues/17

## Architectural overview

![](../../docs/ovs_os_architecture_newton.png)

### The edge client

The edge client is provided by the following packages of Open vStorage:
* qemu
* libvirt-bin

It is used for the following features: 
* Copy image to volume
* Copy volume to image
* Create empty volume
* Extending a existing volume

### The automation library

The automation library that contacts Open vStorage via URI approach is provided in this repo.

It is used for the following features:
* Create volume from existing volume
* Create snapshot from volume
* Create volume from snapshot
* Delete volume
* Delete snapshot from volume

## Sources

https://docs.openstack.org/developer/openstack-ansible/developer-docs/quickstart-aio.html

https://developer.rackspace.com/blog/life-without-devstack-openstack-development-with-osa/

https://docs.openstack.org/project-deploy-guide/openstack-ansible/ocata/

https://docs.openstack.org/project-deploy-guide/openstack-ansible/ocata/verify-operation.html

https://github.com/openstack-dev/devstack

https://github.com/openstack/cinder/blob/master/cinder/volume/drivers/lvm.py

https://github.com/openstack/nova/blob/master/nova/virt/libvirt/storage/lvm.py

## Setups

### OpenStack ALL IN ONE - Virtual machine details
* Hypervisor: 10.100.199.50
* IP address: 10.100.198.200
* Horizon: 10.100.198.200:80
* Amount CPU's: 12
* Amount RAM: 32GB
* Amount disk 210GB (On NVMe)
* Clean snapshot: `clean-snapshot-distupgrade`
* Users:
    * `root/rooter`
    * `ovs-support/rooter`
    
* Ready to go OpenStack `ocata` snapshot: `openstack`
* Ready to go OpenStack `newton` snapshot: `openstack newton 2` (and private key for user `root`)
```
-----BEGIN RSA PRIVATE KEY-----
MIIEpgIBAAKCAQEAydfGmklPjf+CSfBnFmC9Pie2+FibbQ7ensyKLoEQW/4N1aJO
UqAuND2j12LBJILPcq6AMouamEIHaEREzMsHwKqjvs88iWQ+3w30TX0WZCgcd2Xh
g+xZN0mXdRoTfQQZqD334tFApRb1ONZn5rU5zyFZ3IkmVI8Xu6ujj986nOTw9WUh
/nHLKBc8pwJSY03SGXBlHbgJewfkioSDx6urfuulqP7v2YFc2vLpzbY/sDlMwAKq
hK//n0+BlMix0U2HUepH63HBJE8ZOMJGKLO+B+PW5rP8yWCbsG+L6hOllwFYjV8l
4nZmBGsm4BlTDq6NS0zurVCy9it8pQmtM57AuQIDAQABAoIBAQCJvUEfepXajhmo
QXDn2X5rEwkOstDl/Ha5IVXO5G54iIeCWS9fvUWqisHrMs4hD09nsGN1msUV0EFj
yuq0YnzY4tm5VYy3KXyqFMi5tHn6QVEjvZfGwhwj2YmM9Q2Fi63CnP8zfp7Bykfv
0Ii47MUVb2n2UHWi0L9eZ4PHo4tJEs72RJpmrfVgacxnFl7y+UspsDQltM5BfuGk
z+jmEItLBzS/x1Tn4zklncHj3Mx81aCszMZ5bJBabR/4iNKzdjpFCNtN3pJon8hQ
WQwhgFFlpN7szWAHcTu9QvHBHGlsikhnpOMmHOc3Y+xMN5fm3HlLbyFp7+SBZbLd
AjJRhxkdAoGBAPtk8PbU56HBvCHY2fanksErTTL2rUK+VeF/24EGpyzNhkO2lK+w
Upr1bFuhme8SW8zhQOjV6hqXAJ2Gzjl6CNwS5fhvvj5akfm0vzMTPwmWancI0uWh
3mKjQluYdajGoV1D8F426nr4EiT1WtqOSn/vkXh7o36WHiDQpmupoc2fAoGBAM2K
bzsHJahAANSiSJW+zxUmJVxOM3sUYebnUm9ej2IL0TEpCjaMftZz7NkpFw1sW0uv
w9O/NO63vQbEhCO/hyCm9GsaimeEZr8WGd2CM0F8Y3Qb7VLo1XBrB/QGu7LLq99R
tsAkk78zI6ebTiVCOvyGMnYdD+/+P6Y9PHS+LaKnAoGBANpTK8Hx3MhqTEzI22KO
3bDNPlpISOhyDHuuYp+He6A5TaV452A9LUBObDCYA+vQcdFYvtp3DLzS70HfVTIt
fYxDDV3ZDctxNN07z+E3kcNt0kBWdXHgRhY72uFZYrWU64bn/dSUtMbeskNOofy1
HpZFJH0SQ0cocDnneuB9jXvZAoGBALFaIxIW36pm15CiGumDBCJmkNQt8gPgmX1o
2luYhzX9plq548MfxY3750GWT/rYJYqQNfPux5i32BYP2UkTSWCmTr5f307lEtcN
FfJpFxsJXrNgKY5hs1HWOL2aVbk4PqxqULtIlGflk31a57oEhOtCTCZYe1kE1Bz4
N8MwGiZ/AoGBAIBTwa4CTLimehA5EEXFOHCS/uMz6pmCEeSs09bY2gDgseR66mof
UcoZVS/GxzyF6H6wWvWTz90E7PBJ03/RzSynyeGYH5do9Aq3nRxzod3MeeCzem3b
0brJoo4AFD1YkOAzGmIykFVa6lgnd1yu4vC3rMCg5IEtydi+JAI+bRet
-----END RSA PRIVATE KEY-----
```

### DevStack - Virtual machine details
* Hypervisor: 10.100.199.50
* IP address: 10.100.198.201
* Horizon: 10.100.198.201:80
* Amount CPU's: 12
* Amount RAM: 32GB
* Amount disk 210GB (On NVMe)
* Clean snapshot: `clean`
* Users:
    * `root/rooter`
    * `ovs-support/rooter`

I used DevStack to debug some driver issues. I strongly suggest to use DevStack only for development and Ansible AIO for POCs.

When I was installing DevStack, I encountered an error that has something to do with METADATA. I fixed it by installing the following package: `pip install requests[security]` and rerunning `./stack.sh` again. As seen here: https://github.com/ActiveState/appdirs/issues/89#issuecomment-285481179

To install DevStack on `ovs-support@10.100.198.201`, I used the following commands: (To access DevStack, you will have to use user `ovs-support` NOT `root`)
```
git clone https://github.com/openstack-dev/devstack.git
cd devstack
git checkout stable/newton
./stack.sh

. openrc
echo $ADMIN_PASSWORD
```

Cinder volume driver location: `/opt/stack/cinder/cinder/volume/drivers/openvstorage_edge.py`

Cinder brick connector: `/usr/local/lib/python2.7/dist-packages/os_brick/initiator/connector.py`

Cinder driver brick connector: `/usr/local/lib/python2.7/dist-packages/os_brick/initiator/connectors/openvstorage.py`

Nova driver location: `/opt/stack/nova/nova/virt/libvirt/volume/openvstorage_edge.py`

Nova libvirt driver location: `/opt/stack/nova/nova/virt/libvirt/driver.py`

Nova libvirt config location: `/opt/stack/nova/nova/virt/libvirt/config.py`

## What did I test?

* **Ocata:** the cinder driver is working correctly but the nova driver has issues as ocata requires a minimum of libvirt-bin version 2.2.0. And mine was only 1.3.1 at 17/03/2017
* **Newton:** the cinder driver is working correctly, nova is still being tested but it should because we only need libvirt-bin 1.3.1 - 1.3.3

## Installing & managing OpenStack

```
sudo apt-get dist-upgrade
sudo reboot

sudo apt-get install ansible -y # mine was 2.0.0.2-2ubuntu1

git clone https://git.openstack.org/openstack/openstack-ansible /opt/openstack-ansible
cd /opt/openstack-ansible
git checkout 15.0.0  # ocata latest stable atm
git checkout 14.1.1  # newton latest stable atm

./scripts/bootstrap-ansible.sh

./scripts/bootstrap-aio.sh

./scripts/run-playbooks.sh  # this took 1 hour to complete
```

Output of `./scripts/run-playbooks.sh`:

```
The "./scripts/run-playbooks.sh" script has exited. This script is no longer needed from now on.
If you need to re-run parts of the stack, adding new nodes to the environment,
or have encountered an error you will no longer need this application to
interact with the environment. All jobs should be executed out of the
"/opt/openstack-ansible/playbooks" directory using the "openstack-ansible"
command line wrapper.

For more information about OpenStack-Ansible please review our documentation at:
  http://docs.openstack.org/developer/openstack-ansible

Additionally if there's ever a need for information on common operational tasks please
see the following information:
  http://docs.openstack.org/developer/openstack-ansible/developer-docs/ops.html


If you ever have any questions please join the community conversation on IRC at
#openstack-ansible on freenode.
```

### Accessing horizon

Search for the horizon LXE container: `lxc-ls -f`

`aio1_horizon_container-75889311 RUNNING 1 onboot, openstack 10.255.255.190, 172.29.237.193`

access it: `ssh root@172.29.237.193`

edit the following file: `/etc/apache2/sites-enabled/openstack-dashboard.conf`
```
change this line from this:

RequestHeader set X-Forwarded-Proto "https"

to this:

RequestHeader set X-Forwarded-Proto "http"
```

Edit the following file: `/etc/horizon/local_settings.py` & comment the following lines:
```
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
```

Restart apache2: `systemctl restart apache2`

### Orchestration through GUI

Logout from horizon dashboard and perform these command FROM the deployment node: 

Search the admin password to login to horizon: `grep keystone_auth_admin_password /etc/openstack_deploy/user_secrets.yml`

* go with your browser to: `10.100.198.200`
* or setup ssh tunneling to access horizon: `sudo ssh -L 8100:172.29.237.193:80 root@10.100.198.200 -i ~/.ssh/id_rsa` and go with your browser to `10.100.198.200:8100`

login into horizon with user `admin` & the `keystone_auth_admin_password`

### Orchestration through CLi

There is 1 LXE container that can orchestrate everything in OpenStack: `lxc-ls -f | grep utility`

`aio1_utility_container-945241a4 RUNNING 1 onboot, openstack 10.255.255.64, 172.29.239.17`

ssh into the machine: `ssh root@172.29.239.17`

check if its working properly:
```
root@aio1-utility-container-945241a4:~# source openrc
root@aio1-utility-container-945241a4:~# openstack user list
+----------------------------------+--------------------+
| ID                               | Name               |
+----------------------------------+--------------------+
| 032e7af35af643a89f6c1cfbe4e149ca | keystone           |
| 0b475c2eaf9c440c8e2d81314e3fed14 | nova               |
| 12f2e941730c46919fd06c5adbc38001 | designate          |
| 34ad62240294492d84ea904a174c9b38 | heat               |
| 440219a5391648da9d5ec34881564a71 | demo               |
| 45eacbb4e15647beac747b3b19d2db0f | alt_demo           |
| 4eece68429ee41b3be560cef1256c34d | cinder             |
| 57b003735da3470f9b4771985cd482fa | dispersion         |
| 7602efa3dc0e439d885aa1d2b7f657ed | glance             |
| 833888ece0d547fda7f7aa65d00988af | stack_domain_admin |
| 8ebdabf424ef474c9c9bc5542ed00d4c | placement          |
| a3df2f2d82cc4e1c86bc10cf5b88bbba | swift              |
| ab72f3803f2f4b729482b61eb5cea2a0 | ovs_jonas          |
| f48eef0426724cc5b83361994b24bc4e | neutron            |
| fa136f98e40e4ac08d1ea0bb000cbaed | admin              |
+----------------------------------+--------------------+
```

## Installing the Open vStorage cinder driver

Cinder driver directory: `/openstack/venvs/cinder-14.1.1/lib/python2.7/site-packages/cinder/volume/drivers/`

Open vStorage cinder driver: `/openstack/venvs/cinder-14.1.1/lib/python2.7/site-packages/cinder/volume/drivers/openvstorage_edge.py`

Cinder config file: `/etc/cinder/cinder.conf`

**Remarks:** The openvstorage cinder plugin & connectors should be installed where:
 * `cinder-volume` is running
 *  on the cinder node where the vPool is defined

### Configuring a vPool in Open Stack

Login into the cinder api LXE container

This is an example of how to configure a vPool on a cinder API.
```
enabled_backends=myvpool01

[myvpool01]
volume_backend_name = myvpool01
volume_driver = cinder.volume.drivers.openvstorage_edge.OpenvStorageEdgeVolumeDriver
management_ips = 10.100.199.191,10.100.199.192,10.100.199.193
vpool_guid = 7968a798-a0ab-4f6a-8f3d-32f785215307
username = admin
password = admin
port = 443
```

| Options | Type | Examples |
| ------------- |:-------------:| :-----:|
| enabled_backends | list seperated by commas | lvm,myvpool01,myvpool02 |
| volume_backend_name | vpool_name | must be the same as in `enabled_backends` and as between brackets |
| volume_driver | string | must always be `cinder.volume.drivers.openvstorage.OpenvStorageEdgeVolumeDriver` |
| management_ips | list seperated by commas | these ip addresses must be the Open vStorage master nodes |
| vpool_guid | string | guid of the vpool in openvstorage |
| username | string | username to login into Open vStorage |
| password | string | password to login into Open vStorage |
| port | int | port to login into Open vStorage (80 or 443) |

After adding this config to `/etc/cinder/cinder.conf` add the `openvstorage_edge.py` cinder driver to `/openstack/venvs/cinder-14.1.1/lib/python2.7/site-packages/cinder/volume/drivers/openvstorage_edge.py`

### Installing Open vStorage components

Remove all present `libvirt` & `qemu` packages:
```
dpkg -l | grep 'libvirt\|qemu' | tr -s ' ' | cut -d ' ' -f 2 | xargs sudo apt-get purge -y
```

Now install Open vStorage `qemu` & `libvirt-bin`:
```
echo "deb http://apt.openvstorage.com unstable main" > /etc/apt/sources.list.d/ovsaptrepo.list
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 4EFFB1E7

cat > /etc/apt/preferences << EOF
Package: *
Pin: origin apt.openvstorage.com
Pin-Priority: 1000
EOF 

apt-get update

apt-get install qemu libvirt-bin -y

mkdir -p /opt/OpenvStorage/
git clone https://github.com/openvstorage/framework-cinder-plugin.git /opt/OpenvStorage/
cd /opt/OpenvStorage/
git checkout ovs-23-cinder-cleanup  # IN THE FUTURE THIS CAN BE MASTER
find . -type d -exec touch {}/__init__.py \;
cd /opt/
sudo chown -R cinder:cinder OpenvStorage/
```

Restart the following services on all cinder nodes:
```
systemctl restart cinder-volume; systemctl status cinder-volume
systemctl restart cinder-backup; systemctl status cinder-backup
```

In the cinder-volume logs you should see the cinder driver initializing in the cinder volume manager:
```
root@osa-aio-ctrl:~# grep "libovsvolumedriver.init\|libovsvolumedriver.do_setup" /var/log/cinder/cinder-volume.log
2017-03-28 14:33:28.638 DEBUG cinder.volume.drivers.openvstorage_edge [req-ef7d53ee-68cc-4573-89b2-c51d1dae5856 None None] libovsvolumedriver.init from (pid=3059) __init__ /opt/stack/cinder/cinder/volume/drivers/openvstorage_edge.py:96
2017-03-28 14:33:28.694 DEBUG cinder.volume.drivers.openvstorage_edge [req-abb3f01d-fda4-4d8c-9742-0805d4386f48 None None] libovsvolumedriver.do_setup 10.100.199.191,10.100.199.192,10.100.199.193 7968a798-a0ab-4f6a-8f3d-32f785215307 admin admin 443 from (pid=3079) do_setup /opt/stack/cinder/cinder/volume/drivers/openvstorage_edge.py:191
```

If you cannot find the above logs, there is probably something wrong. You can debug it as so:
```
root@osa-aio-ctrl:~# grep openvstorage /var/log/cinder/cinder-volume.log 
2017-03-29 15:13:04.112 30231 ERROR cinder.cmd.volume   File "/openstack/venvs/cinder-14.1.1/lib/python2.7/site-packages/cinder/volume/drivers/openvstorage_edge.py", line 47, in <module>
2017-03-29 15:13:04.186 30231 DEBUG oslo_service.service [req-2fc177f9-930d-4dd2-94f6-6fc416198c32 - - - - -] vmstor.volume_driver           = cinder.volume.drivers.openvstorage_edge.OpenvStorageEdgeVolumeDriver log_opt_values /openstack/venvs/cinder-14.1.1/lib/python2.7/site-packages/oslo_config/cfg.py:2626
```

### Adding a new volume type to OpenStack

ssh into the utility container: `aio1_utility_container-a5ba154c RUNNING 1 onboot, openstack 10.255.255.199, 172.29.239.36`

In my case `ssh root@172.29.239.36` and perform the following commands.

```
source openrc admin admin

ovs-support@dsa-aio-ctrl:~/devstack$ cinder type-list
+--------------------------------------+------+-------------+-----------+
| ID                                   | Name | Description | Is_Public |
+--------------------------------------+------+-------------+-----------+
| 8fa1d999-914c-44b5-b2a0-e214107d00ee | lvm  | -           | True      |
+--------------------------------------+------+-------------+-----------+

ovs-support@dsa-aio-ctrl:~/devstack$ cinder type-create myvpool01
+--------------------------------------+-----------+-------------+-----------+
| ID                                   | Name      | Description | Is_Public |
+--------------------------------------+-----------+-------------+-----------+
| d3213e52-05b8-4c49-bdaf-7f143aae757f | myvpool01 | -           | True      |
+--------------------------------------+-----------+-------------+-----------+

ovs-support@dsa-aio-ctrl:~/devstack$ cinder type-list
+--------------------------------------+-----------+-------------+-----------+
| ID                                   | Name      | Description | Is_Public |
+--------------------------------------+-----------+-------------+-----------+
| 8fa1d999-914c-44b5-b2a0-e214107d00ee | lvm       | -           | True      |
| d3213e52-05b8-4c49-bdaf-7f143aae757f | myvpool01 | -           | True      |
+--------------------------------------+-----------+-------------+-----------+

ovs-support@dsa-aio-ctrl:~/devstack$ cinder type-key myvpool01 set volume_backend_name=myvpool01
ovs-support@dsa-aio-ctrl:~/devstack$ cinder extra-specs-list
+--------------------------------------+-----------+----------------------------------------+
| ID                                   | Name      | extra_specs                            |
+--------------------------------------+-----------+----------------------------------------+
| 8fa1d999-914c-44b5-b2a0-e214107d00ee | lvm       | {u'volume_backend_name': u'LVM_iSCSI'} |
| d3213e52-05b8-4c49-bdaf-7f143aae757f | myvpool01 | {u'volume_backend_name': u'myvpool01'} |
+--------------------------------------+-----------+----------------------------------------+
```

Now start creating a volume with `volume_type` of Open vStorage. (In this case it would be `myvpool01`)

## Installing the Open vStorage nova driver

Nova driver location: `/openstack/venvs/nova-14.1.1/lib/python2.7/site-packages/nova/virt/libvirt/driver.py`

Nova config location: `/openstack/venvs/nova-14.1.1/lib/python2.7/site-packages/nova/virt/libvirt/config.py`

Open vStorage nova driver: `/openstack/venvs/nova-14.1.1/lib/python2.7/site-packages/nova/virt/libvirt/volume/openvstorage_edge.py`

Nova config file: `/etc/nova/nova.conf`

**Remarks:** The openvstorage nova plugin, `driver.py` & `config.py` should be installed where:
 * `nova-compute` is running
 *  on the nova node where the vPool is defined in cinder
 
### Installing the nova driver

Install the following nova driver in Open Stack: `/openstack/venvs/nova-14.1.1/lib/python2.7/site-packages/nova/virt/libvirt/volume/openvstorage_edge.py`

### Patching driver & config.py

#### config.py

Nova config location: `/openstack/venvs/nova-14.1.1/lib/python2.7/site-packages/nova/virt/libvirt/config.py`

Add this on line 904

```
class LibvirtConfigOpenvStorageEdgeGuestDisk(LibvirtConfigGuestDisk):
    def __init__(self, **kwargs):
        super(LibvirtConfigGuestDisk, self).__init__(root_name="disk", **kwargs)
        self.source_type = "network"
        self.source_device = "disk"
        self.driver_name = 'qemu'
        self.driver_type = 'raw'
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

#### driver.py

Nova driver location: `/openstack/venvs/nova-14.1.1/lib/python2.7/site-packages/nova/virt/libvirt/driver.py`

You should add a `libvirt_volume_driver` to the list called `openvstorage_edge=nova.virt.libvirt.volume.openvstorage_edge.LibvirtOpenvStorageEdgeVolumeDriver` on line 148

Now restart the `nova-compute` services on all nova nodes: `systemctl restart nova-compute; systemctl status nova-compute`

Checking if everything properly started: `ovs-support@dsa-aio-ctrl:~$ grep libovsvolumedriver.init /var/log/nova/nova-compute.log`
```
2017-03-27 10:50:26.681 DEBUG nova.virt.libvirt.volume.openvstorage_edge [req-44bf8b60-2a8d-4740-ad8b-495ad8b7452d None None] libovsvolumedriver.init from (pid=25690) __init__ /opt/stack/nova/nova/virt/libvirt/volume/openvstorage_edge.py:44
```

## Adding a image to glance

Login into the utility LXE container and perform following commands

```
wget http://download.cirros-cloud.net/0.3.5/cirros-0.3.5-x86_64-disk.img
root@aio1-utility-container-f7adfdd4:~# glance image-create --name cirros-img --visibility public --file cirros-0.3.5-x86_64-disk.img --container-format bare --disk-format qcow2
+------------------+--------------------------------------+
| Property         | Value                                |
+------------------+--------------------------------------+
| checksum         | c8c4bca1793ed3d398accff4212c97e1     |
| container_format | bare                                 |
| created_at       | 2017-03-29T13:32:46Z                 |
| disk_format      | qcow2                                |
| id               | 2da15b70-c441-4a69-9ad9-5cd7a6de5078 |
| min_disk         | 0                                    |
| min_ram          | 0                                    |
| name             | cirros-img                           |
| owner            | cd307d26efb544dc8581375828bf6936     |
| protected        | False                                |
| size             | 7779384                              |
| status           | active                               |
| tags             | []                                   |
| updated_at       | 2017-03-29T13:32:47Z                 |
| virtual_size     | None                                 |
| visibility       | public                               |
+------------------+--------------------------------------+

```