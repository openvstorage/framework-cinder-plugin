# Installing OpenStack via Ansible the ALL IN ONE way

## Description
This setup is a easy way to setup OpenStack on 1 VM in LXE containers.
This walkthrough is mainly focusing on OpenStack but in `DevStack Virtual machine details` section, you can find all the directories for DevStack.

Before we begin, I want to mention that the directories that are present in this document can differ with the reality as every openstack distribution is different. 
Nevertheless once you get a hold of it, the main directories do not differ that much.

## Architectural overview

![](../../docs/ovs_os_architecture_newton.png)

### The edge client

The edge client is provided by the following packages of Open vStorage:
* qemu
* libvirt-bin

It is used for the following features: 
* Copy image to volume
* Copy volume to image

### The automation library

The automation library that contacts Open vStorage via URI approach is provided in this repo.

## Sources

https://docs.openstack.org/developer/openstack-ansible/developer-docs/quickstart-aio.html

https://developer.rackspace.com/blog/life-without-devstack-openstack-development-with-osa/

https://docs.openstack.org/project-deploy-guide/openstack-ansible/ocata/

https://docs.openstack.org/project-deploy-guide/openstack-ansible/ocata/verify-operation.html

https://github.com/openstack-dev/devstack

https://github.com/openstack/cinder/blob/master/cinder/volume/drivers/lvm.py

https://github.com/openstack/nova/blob/master/nova/virt/libvirt/storage/lvm.py

## Setups

### OpenStack Virtual machine details
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
* Ready to go OpenStack `newton` snapshot: `openstack-newton` (and private key for user `root`)
```
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEA2L/PKYssOqBNUfrOv/nOJjxzrLuFjD8u9kW72bnCbgu7hYsP
7nXXhfWJ7xlaN/Mjn/xkfwuPpaqQ01FWJZxNgkpkymZq4zVUTY3W+DNNMdEDyPDm
usV3V/rFwXQWOpgQrzeMD0cUwUMLHo+GWOhMj+1kdNw6tnbWZBkRuEVAkTMfhqub
XjtjNV5U/OxL1nbcNTbwpT4tteUTMaiHa0xnPlMqzEe+g5RuQhjIfziJ+GpC169h
UixBTdlOIKnNSJJ2LKPmmGaglBlLgzjMcfin2h6/Ln8DEoxhyTNof3r5JMIxvIEf
p28bLZ8yHMVlVVrYR1fFSXK3DVAM8cQJMdHbHwIDAQABAoIBACUk4byN1BuL4xQ8
dffiOFjHHU+ppx48qbCcjK+oLNCtBArDpQxJd5DGXkfyQUq7SQyetR4sfgZ273C3
TJsPaRz94L3qxUCAoBzWRNOt/vmdhxeFaRTyyBv0prUbTr/l1V4hl8f6d20TLzGi
iPRtgslbdk6sewdP4DexMB8zBviayFl4lN4CgSpUoJrwXIytgjyonqc48glz5OVl
UBfo2JAS3kNbTho6Mld1hs8dz9fSRJz3yXEl0iRknavdk3wbXEySlDXMPxJENdRb
Fdx4HV5qY7i3pAeliBIxuNEiRaTo9obVRkFx0i8FkgjyUqTD4bCObGLFh4F8wNyd
KooJcNECgYEA+cG66eYdNq5mq42XVwb7wSU1rKRAngDEp1vRAEOdANDbSvRblVQF
Rx5BrWW2u/mbEscNzoghjHByHsMhp4QAZqQvo4xd7gxaMgVy77+EcA+oVc1gP3O2
SmQJ0Eipu3uJ6WHX13C7QvFpHydF8InwKjlwvsqouE/dzFdJa8PQbucCgYEA3ira
nvJsGlGK+zUArPCfQk9gLEdjPV3ICm4Cns9nuY8xkeH2M90yjOxcz0WfRz7KKcS3
w/Ud2M5jJiVFPS9AD6vbKMHCsygkTZAUFhpIC/f3CQydRuKFltfMaYkCu1fgeFFG
Tuvp2i0gjiBR2svE+sTj+OfTcsLpNOEAzNBcwwkCgYB8KPcGuELloCWiOy11Mh+N
kTXxsWX+Jluc52QrQXGXqjyaMogk4DQPetcjoGELabbRyuruNXaYHn5dFJxybojU
feLA51L6uGFOZK8SyJ7KJr6EiSjD4n5I1Rqb1MOsVGnm/6ERlRVC3khoGFoIjko6
c3u9HXpqxil5IBt720iPGQKBgG+UkFZyJM8XEzlVhnBVLXdtTD0Q4YvJlRV/6Pr/
6fVtMJU3KqMjvia+82H6cqOiqoBN14moiwP/rBZVc6/mEkOMqbaPkgzO5WS7Lwtm
ybaRJFY8KqWWUUfQPE7ozCFxYkCreSdcHwg/z/Dx1IqR+u2Dg4fYTv99Wwj+1JsJ
Lv2ZAoGBAMAJlxH1vRUPwVT11lwJpiFtVJJNzktjsqdzOirUN+70rnniG27Bk+lo
PytChCND4tpUY4nAyZl92wktTZ9+KgFGEJMvKjN4l3MnNKS5Dy3bosv+wWus9FD/
jGirZrIq1IY1Z4QGA2u50MX4CIvPcF5qcwrzRSAMhSR0DLT6COIr
-----END RSA PRIVATE KEY-----
```

### DevStack Virtual machine details
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
git checkout -b 15.0.0  # ocata latest stable atm
git checkout -b 14.1.1  # newton latest stable atm

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

### Patching the connector.py & adding a openvstorage connector

**IMPORTANT:** You will have to patch these files on the NOVA & CINDER part.

Base directory for the CINDER files: `/openstack/venvs/cinder-14.1.1/lib/python2.7/site-packages/os_brick/initiator/`
Base directory for the NOVA files: `/openstack/venvs/nova-14.1.1/lib/python2.7/site-packages/os_brick/initiator/`

#### Connector.py

This file is present in the following locations: 
* `/openstack/venvs/cinder-14.1.1/lib/python2.7/site-packages/os_brick/initiator/connector.py`
* `/openstack/venvs/nova-14.1.1/lib/python2.7/site-packages/os_brick/initiator/connector.py`

We have to edit the following lines:

* line 85 
`OPENVSTORAGE_EDGE = "OPENVSTORAGE_EDGE"`

* line 93
```
connector_list = [
        'os_brick.initiator.connectors.openvstorage.OpenvStorageEdgeConnector',
        #...
```

* line 277
```
elif protocol == OPENVSTORAGE_EDGE:
    return OpenvStorageEdgeConnector(root_helper=root_helper,
                                     driver=driver,
                                     device_scan_attempts=device_scan_attempts,
                                     *args, **kwargs)
```

#### Connectors/openvstorage.py

This file is present in the following locations: 
* `/openstack/venvs/cinder-14.1.1/lib/python2.7/site-packages/os_brick/initiator/connectors/openvstorage.py`
* `/openstack/venvs/nova-14.1.1/lib/python2.7/site-packages/os_brick/initiator/connectors/openvstorage.py`

### Installing Open vStorage components on compute node

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
```

Restart the following services on all cinder nodes:
```
systemctl restart cinder-volume
systemctl restart cinder-backup
```

In the cinder-volume logs you should see the cinder driver initializing in the cinder volume manager:
```
root@osa-aio-ctrl:~# grep "libovsvolumedriver.init\|libovsvolumedriver.do_setup" /var/log/cinder/cinder-volume.log
2017-03-28 14:33:28.638 DEBUG cinder.volume.drivers.openvstorage_edge [req-ef7d53ee-68cc-4573-89b2-c51d1dae5856 None None] libovsvolumedriver.init from (pid=3059) __init__ /opt/stack/cinder/cinder/volume/drivers/openvstorage_edge.py:96
2017-03-28 14:33:28.694 DEBUG cinder.volume.drivers.openvstorage_edge [req-abb3f01d-fda4-4d8c-9742-0805d4386f48 None None] libovsvolumedriver.do_setup 10.100.199.191,10.100.199.192,10.100.199.193 7968a798-a0ab-4f6a-8f3d-32f785215307 admin admin 443 from (pid=3079) do_setup /opt/stack/cinder/cinder/volume/drivers/openvstorage_edge.py:191
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

**Remarks:** The openvstorage nova plugin, `config.py` & `driver.py` should be installed where: `nova-compute` is running

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

Now restart the `nova-compute` services on all nova nodes: `systemctl restart nova-compute`

Checking if everything properly started: `ovs-support@dsa-aio-ctrl:~$ grep libovsvolumedriver.init /var/log/nova/nova-compute.log`
```
2017-03-27 10:50:26.681 DEBUG nova.virt.libvirt.volume.openvstorage_edge [req-44bf8b60-2a8d-4740-ad8b-495ad8b7452d None None] libovsvolumedriver.init from (pid=25690) __init__ /opt/stack/nova/nova/virt/libvirt/volume/openvstorage_edge.py:44
```