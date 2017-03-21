# Installing OpenStack via Ansible the ALL IN ONE way

## Description
This setup is a easy way to setup OpenStack on 1 VM in LXE containers.
This walkthrough is mainly focussing on OpenStack but in `Remarks` section, you can find all the directories for DevStack.

Outside sources: 

https://docs.openstack.org/developer/openstack-ansible/developer-docs/quickstart-aio.html

https://developer.rackspace.com/blog/life-without-devstack-openstack-development-with-osa/

https://docs.openstack.org/project-deploy-guide/openstack-ansible/ocata/

https://docs.openstack.org/project-deploy-guide/openstack-ansible/ocata/verify-operation.html

https://github.com/openstack-dev/devstack

Inside sources:

https://github.com/openvstorage/framework-cinder-plugin/tree/ovs-23-cinder-cleanup

http://confluence.openvstorage.com/display/~kvanhijf/Install+OpenStack

## Virtual machine details
* IP address: 10.100.198.200
* Amount CPU's: 12
* Amount RAM: 32GB
* Amount disk 210GB (On NVMe)

## Remarks

Before we begin, I want to mention that the directories that are present in this document can differ with the reality as every openstack distribution is different. Nevertheless once you get a hold of it, the main directories do not differ that much.

I used DevStack to debug some driver issues. I strongly suggest to use DevStack only for development and Ansible AIO for POCs.

When I was installing DevStack, I encountered an error that has something to do with METADATA. I fixed it by installing the following package: `pip install requests[security]` and rerunning `./stack.sh` again. As seen here: https://github.com/ActiveState/appdirs/issues/89#issuecomment-285481179

To install DevStack on `ovs-support@10.100.198.201` I used the following commands:
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

## What did I test?

* Ocata: the cinder driver is working correctly but the nova driver has issues as ocata requires a minimum of libvirt-bin version 2.2.0. And mine was only 1.3.1 at 17/03/2017
* Newton: the cinder driver is working correctly, nova is still being tested but it should because we only need libvirt-bin 1.3.1 - 1.3.3

## Install OpenStack

```
sudo apt-get dist-upgrade
sudo reboot

sudo apt-get install ansible -y

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

## Accessing horizon

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

## Orchestration through GUI

Logout from horizon dashboard and perform these command FROM the deployment node: 

Search the admin password to login to horizon: `grep keystone_auth_admin_password /etc/openstack_deploy/user_secrets.yml`

setup ssh tunneling to access horizon: `sudo ssh -L 8100:172.29.237.193:80 root@10.100.198.200 -i ~/.ssh/id_rsa`

Go with your browser to: `10.100.198.200:8100`
login into horizon with user `admin` & the `keystone_auth_admin_password`

## Orchestration through CLi

There is 1 LXE container that can orchestrate everything in OpenStack.

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

Cinder driver directory: `/openstack/venvs/cinder-15.0.0/lib/python2.7/site-packages/cinder/volume/drivers/`
Open vStorage cinder driver: `/openstack/venvs/cinder-15.0.0/lib/python2.7/site-packages/cinder/volume/drivers/openvstorage_edge.py`
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
storage_ip = 10.100.199.191
edge_port = 26203
edge_protocol = tcp
xml_rpc_port = 26201
vpool_guid = 7968a798-a0ab-4f6a-8f3d-32f785215307
```

| Options | Type | Examples |
| ------------- |:-------------:| :-----:|
| enabled_backends | list seperated by commas | lvm,myvpool01,myvpool02 |
| volume_backend_name | vpool_name | must be the same as in `enabled_backends` and as between brackets |
| volume_driver | string | must always be `cinder.volume.drivers.openvstorage.OpenvStorageEdgeBaseVD` |
| storage_ip | ip address | storage ip of a storagedriver that belongs to the vpool, this storagedriver will be used to deploy the volumes on via Open Stack |
| edge_port | port | edge port of a storagedriver |
| edge_protocol | protocol | tcp or rdma |
| xml_rpc_port | port | xml_rpc communication port with the storagedriver |
| vpool_guid | ovs guid | guid of the vpool in openvstorage |

After adding this config to `/etc/cinder/cinder.conf` add the `openvstorage_edge.py` cinder driver to `/openstack/venvs/cinder-15.0.0/lib/python2.7/site-packages/cinder/volume/drivers/openvstorage_edge.py`

```
# Copyright 2016 iNuron NV
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
OpenStack Cinder driver - interface to Open vStorage Edge
- uses qemu-img calls (requires libovsvolumedriver, qemu, libvirt-bin packages from openvstorage repo)
- uses libovsvolumedriver calls where needed
"""
import os, ctypes, errno
from ctypes import cdll, CDLL

from oslo_config import cfg
from oslo_log import log as logging
import six

from cinder import exception
from cinder import utils
from cinder.image import image_utils
from cinder.volume import driver


LOG = logging.getLogger(__name__)
OPTS = [cfg.StrOpt('storage_ip',
                   default = '',
                   help = 'IP address of first storage node'),
        cfg.StrOpt('edge_port',
                   default = '26203',
                   help = 'PORT of the edge server'),
        cfg.StrOpt('edge_protocol',
                   default = 'tcp',
                   help = 'Protocol to use - edge client')]

CONF = cfg.CONF
CONF.register_opts(OPTS)


class OpenvStorageEdgeVolumeDriver(driver.VolumeDriver):
    """Open vStorage Edge Volume Driver plugin for Cinder."""
    VERSION = '0.0.1'

    def __init__(self, *args, **kwargs):
        """Init: args, kwargs pass through;

        Options come from CONF
        """
        super(OpenvStorageEdgeVolumeDriver, self).__init__(*args, **kwargs)
        LOG.debug('INIT %s %s %s %s %s', CONF.storage_ip, CONF.edge_port, CONF.edge_protocol, args, kwargs)
        self.configuration.append_config_values(OPTS)
        self.volume_backend_name = kwargs['host'].split('@')[1]

    def _get_volume_location(self, volume_name):
        """Return volume location."""
        return 'openvstorage+{0}:{1}:{2}/{3}'.format(self.configuration.edge_protocol,
                                                     self.configuration.storage_ip,
                                                     self.configuration.edge_port,
                                                     volume_name)

    def _run_qemu_img(self, command, *params):
        """Executes qemu-img command wrapper."""
        cmd = ['env', 'LC_ALL=C', 'LANG=C', 'qemu-img', command] + list(params)
        output = utils.execute(*cmd)
        LOG.debug('Run: {0} Output: {1}'.format(cmd, output))
        return output

    def check_for_setup_error(self):
        """Check for setup errors"""
        pass

    def do_setup(self, context):
        """Any initialization the volume driver does while starting."""
        cdll.LoadLibrary('libovsvolumedriver.so')
        libovsvolumedriver = CDLL('libovsvolumedriver.so', use_errno=True)
        ctx_attr = libovsvolumedriver.ovs_ctx_attr_new()
        libovsvolumedriver.ovs_ctx_attr_set_transport(ctx_attr,
                                                      self.configuration.edge_protocol,
                                                      self.configuration.storage_ip,
                                                      int(self.configuration.edge_port))
        self.ctx = libovsvolumedriver.ovs_ctx_new(ctx_attr)
        LOG.debug('libovsvolumedriver do_setup: {0} {1} {2} {3} > {4}'.format(ctx_attr, self.configuration.edge_protocol, self.configuration.storage_ip, self.configuration.edge_port, self.ctx))
        self.libovsvolumedriver = libovsvolumedriver

    # Volume operations
    def initialize_connection(self, volume, connector):
        """Allow connection to connector and return connection info."""
        _ = connector
        return {'driver_volume_type': 'openvstorage_edge',
                'volume_backend_name': self.volume_backend_name,
                'data': {'device_path': volume.provider_location}}

    def create_volume(self, volume):
        """Creates a volume.

        Called on "cinder create ..." or "nova volume-create ..."
        :param volume: volume reference (sqlalchemy Model)
        """
        location = self._get_volume_location(volume.display_name)
        #out = self.libovsvolumedriver.ovs_create_volume(self.ctx, str(volume.display_name), int(volume.size*1024**3))
        out = self._run_qemu_img('create', location, '{0}G'.format(volume.size))
        LOG.debug('libovsvolumedriver.ovs_create_volume: {0} {1} {2} > {3}'.format(self.ctx, volume.display_name, volume.size, out))
        #if out == -1:
        #    raise OSError(errno.errorcode[ctypes.get_errno()])

        volume['provider_location'] = location
        #self.extend_volume(volume, volume.size)
        return {'provider_location': volume['provider_location']}

    def delete_volume(self, volume):
        """Deletes a logical volume.

        Called on "cinder delete ... "
        :param volume: volume reference (sqlalchemy Model)
        """
        out = self.libovsvolumedriver.ovs_remove_volume(self.ctx, str(volume.display_name))
        LOG.debug('libovsvolumedriver.ovs_remove_volume: {0} {1} > {2}'.format(self.ctx, volume.display_name, out))
        if out == -1:
            errno = ctypes.get_errno()
            if errno == 2:
                return
            raise OSError(errno.errorcode[errno])

    def copy_image_to_volume(self, context, volume, image_service, image_id):
        """Copy image to volume

        Called on "nova volume-create --image-id ..."
        or "cinder create --image-id"
        Downloads image from glance server into volume
        :param context: Context object
        :param volume: volume reference (sqlalchemy Model)
        :param image_service: image service reference
        :param image_id: id of the image
        """
        #self.extend_volume(volume, volume.size)

        location = self._get_volume_location(volume.display_name)
        image_path = os.path.join('/tmp', image_id)
        if not os.path.exists(image_path):
            image_utils.fetch_to_raw(context,
                                     image_service,
                                     image_id,
                                     image_path,
                                     '1M',
                                     size=volume['size'])
        self._run_qemu_img('convert', '-n', '-O', 'raw', image_path, location)

    def extend_volume(self, volume, size_gb):
        """Extend volume to new size size_gb."""
        if size_gb < volume.size:
            raise RuntimeError('Cannot shrink volume.')
        out = self.libovsvolumedriver.ovs_truncate_volume(self.ctx, str(volume.display_name), int(volume.size*1024**3))
        LOG.debug('libovsvolumedriver.ovs_truncate_volume: {0} {1} {2} > {3}'.format(self.ctx, volume.display_name, volume.size, out))
        if out == -1:
            raise OSError(errno.errorcode[ctypes.get_errno()])

    # Attach/detach volume to instance/host
    def attach_volume(self, context, volume, instance_uuid, host_name,
                      mountpoint):
        """Callback for volume attached to instance or host."""
        pass

    def detach_volume(self, context, volume, attachment=None):
        """Callback for volume detached."""
        pass

    def get_volume_stats(self, refresh=False):
        """Get volumedriver stats

        Refresh not implemented
        """
        _ = refresh
        return {'volume_backend_name': self.volume_backend_name,
                'vendor_name': 'Open vStorage',
                'driver_version': self.VERSION,
                'storage_protocol': 'openvstorage_edge',
                'total_capacity_gb': 'unknown',
                'free_capacity_gb': 'unknown',
                'reserved_percentage': 0,
                'QoS_support': False}


    # Prevent NotImplementedError being raised
    # Not actually implemented, these actions do not make sense for this driver
    def create_export(self, context, volume, connector=None):
        """Exports the volume."""
        pass


    def remove_export(self, context, volume):
        """Removes an export for a volume."""
        pass

    def ensure_export(self, context, volume):
        """Synchronously recreates an export for a volume."""
        pass


    def terminate_connection(self, volume, connector, force):
        """Disallow connection from connector"""
        pass
```

### Patching the connector.py & adding a openvstorage connector

**IMPORTANT:** You will have to patch these files on the NOVA & CINDER part.

Base directory for the CINDER files: `/openstack/venvs/cinder-15.0.0/lib/python2.7/site-packages/os_brick/initiator/`
Base directory for the NOVA files: `/openstack/venvs/nova-14.1.1/lib/python2.7/site-packages/os_brick/initiator/`


#### Connector.py

This file is present in the following locations: 
* `/openstack/venvs/cinder-15.0.0/lib/python2.7/site-packages/os_brick/initiator/connector.py`
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

My `connector.py` looks like this:
```
# Copyright 2013 OpenStack Foundation.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
"""Brick Connector objects for each supported transport protocol.

.. module: connector

The connectors here are responsible for discovering and removing volumes for
each of the supported transport protocols.
"""

import platform
import re
import socket
import sys

from oslo_concurrency import lockutils
from oslo_log import log as logging
from oslo_utils import importutils

from os_brick import exception
from os_brick.i18n import _
from os_brick import initiator
from os_brick import utils

LOG = logging.getLogger(__name__)

synchronized = lockutils.synchronized_with_prefix('os-brick-')

# These constants are being deprecated and moving to the init file.
# Please use the constants there instead.

DEVICE_SCAN_ATTEMPTS_DEFAULT = 3
MULTIPATH_ERROR_REGEX = re.compile("\w{3} \d+ \d\d:\d\d:\d\d \|.*$")
MULTIPATH_DEV_CHECK_REGEX = re.compile("\s+dm-\d+\s+")
MULTIPATH_PATH_CHECK_REGEX = re.compile("\s+\d+:\d+:\d+:\d+\s+")

PLATFORM_ALL = 'ALL'
PLATFORM_x86 = 'X86'
PLATFORM_S390 = 'S390'
OS_TYPE_ALL = 'ALL'
OS_TYPE_LINUX = 'LINUX'
OS_TYPE_WINDOWS = 'WIN'

S390X = "s390x"
S390 = "s390"

ISCSI = "ISCSI"
ISER = "ISER"
FIBRE_CHANNEL = "FIBRE_CHANNEL"
AOE = "AOE"
DRBD = "DRBD"
NFS = "NFS"
GLUSTERFS = "GLUSTERFS"
LOCAL = "LOCAL"
GPFS = "GPFS"
HUAWEISDSHYPERVISOR = "HUAWEISDSHYPERVISOR"
HGST = "HGST"
RBD = "RBD"
SCALEIO = "SCALEIO"
SCALITY = "SCALITY"
QUOBYTE = "QUOBYTE"
DISCO = "DISCO"
VZSTORAGE = "VZSTORAGE"
SHEEPDOG = "SHEEPDOG"
OPENVSTORAGE_EDGE = "OPENVSTORAGE_EDGE"

# List of connectors to call when getting
# the connector properties for a host
connector_list = [
    'os_brick.initiator.connectors.base.BaseLinuxConnector',
    'os_brick.initiator.connectors.iscsi.ISCSIConnector',
    'os_brick.initiator.connectors.fibre_channel.FibreChannelConnector',
    ('os_brick.initiator.connectors.fibre_channel_s390x.'
     'FibreChannelConnectorS390X'),
    'os_brick.initiator.connectors.aoe.AoEConnector',
    'os_brick.initiator.connectors.remotefs.RemoteFsConnector',
    'os_brick.initiator.connectors.rbd.RBDConnector',
    'os_brick.initiator.connectors.local.LocalConnector',
    'os_brick.initiator.connectors.gpfs.GPFSConnector',
    'os_brick.initiator.connectors.drbd.DRBDConnector',
    'os_brick.initiator.connectors.huawei.HuaweiStorHyperConnector',
    'os_brick.initiator.connectors.hgst.HGSTConnector',
    'os_brick.initiator.connectors.scaleio.ScaleIOConnector',
    'os_brick.initiator.connectors.disco.DISCOConnector',
    'os_brick.initiator.connectors.vmware.VmdkConnector',
    'os_brick.initiator.windows.base.BaseWindowsConnector',
    'os_brick.initiator.windows.iscsi.WindowsISCSIConnector',
    'os_brick.initiator.windows.fibre_channel.WindowsFCConnector',
    'os_brick.initiator.windows.smbfs.WindowsSMBFSConnector',
    'os_brick.initiator.connectors.openvstorage.OpenvStorageEdgeConnector',
]

# Mappings used to determine who to contruct in the factory
_connector_mapping_linux = {
    initiator.AOE:
        'os_brick.initiator.connectors.aoe.AoEConnector',
    initiator.DRBD:
        'os_brick.initiator.connectors.drbd.DRBDConnector',

    initiator.GLUSTERFS:
        'os_brick.initiator.connectors.remotefs.RemoteFsConnector',
    initiator.NFS:
        'os_brick.initiator.connectors.remotefs.RemoteFsConnector',
    initiator.SCALITY:
        'os_brick.initiator.connectors.remotefs.RemoteFsConnector',
    initiator.QUOBYTE:
        'os_brick.initiator.connectors.remotefs.RemoteFsConnector',
    initiator.VZSTORAGE:
        'os_brick.initiator.connectors.remotefs.RemoteFsConnector',

    initiator.ISCSI:
        'os_brick.initiator.connectors.iscsi.ISCSIConnector',
    initiator.ISER:
        'os_brick.initiator.connectors.iscsi.ISCSIConnector',
    initiator.FIBRE_CHANNEL:
        'os_brick.initiator.connectors.fibre_channel.FibreChannelConnector',

    initiator.LOCAL:
        'os_brick.initiator.connectors.local.LocalConnector',
    initiator.HUAWEISDSHYPERVISOR:
        'os_brick.initiator.connectors.huawei.HuaweiStorHyperConnector',
    initiator.HGST:
        'os_brick.initiator.connectors.hgst.HGSTConnector',
    initiator.RBD:
        'os_brick.initiator.connectors.rbd.RBDConnector',
    initiator.SCALEIO:
        'os_brick.initiator.connectors.scaleio.ScaleIOConnector',
    initiator.DISCO:
        'os_brick.initiator.connectors.disco.DISCOConnector',
    initiator.SHEEPDOG:
        'os_brick.initiator.connectors.sheepdog.SheepdogConnector',
    initiator.VMDK:
        'os_brick.initiator.connectors.vmware.VmdkConnector',
    initiator.GPFS:
        'os_brick.initiator.connectors.gpfs.GPFSConnector',

}

# Mapping for the S390X platform
_connector_mapping_linux_s390x = {
    initiator.FIBRE_CHANNEL:
        'os_brick.initiator.connectors.fibre_channel_s390x.'
        'FibreChannelConnectorS390X',
    initiator.DRBD:
        'os_brick.initiator.connectors.drbd.DRBDConnector',
    initiator.NFS:
        'os_brick.initiator.connectors.remotefs.RemoteFsConnector',
    initiator.ISCSI:
        'os_brick.initiator.connectors.iscsi.ISCSIConnector',
    initiator.LOCAL:
        'os_brick.initiator.connectors.local.LocalConnector',
    initiator.RBD:
        'os_brick.initiator.connectors.rbd.RBDConnector',
    initiator.GPFS:
        'os_brick.initiator.connectors.gpfs.GPFSConnector',
}

# Mapping for the windows connectors
_connector_mapping_windows = {
    initiator.ISCSI:
        'os_brick.initiator.windows.iscsi.WindowsISCSIConnector',
    initiator.FIBRE_CHANNEL:
        'os_brick.initiator.windows.fibre_channel.WindowsFCConnector',
    initiator.SMBFS:
        'os_brick.initiator.windows.smbfs.WindowsSMBFSConnector',
}


# Create aliases to the old names until 2.0.0
# TODO(smcginnis) Remove this lookup once unit test code is updated to
# point to the correct location
for item in connector_list:
    _name = item.split('.')[-1]
    globals()[_name] = importutils.import_class(item)


@utils.trace
def get_connector_properties(root_helper, my_ip, multipath, enforce_multipath,
                             host=None, execute=None):
    """Get the connection properties for all protocols.

    When the connector wants to use multipath, multipath=True should be
    specified. If enforce_multipath=True is specified too, an exception is
    thrown when multipathd is not running. Otherwise, it falls back to
    multipath=False and only the first path shown up is used.
    For the compatibility reason, even if multipath=False is specified,
    some cinder storage drivers may export the target for multipath, which
    can be found via sendtargets discovery.

    :param root_helper: The command prefix for executing as root.
    :type root_helper: str
    :param my_ip: The IP address of the local host.
    :type my_ip: str
    :param multipath: Enable multipath?
    :type multipath: bool
    :param enforce_multipath: Should we enforce that the multipath daemon is
                              running?  If the daemon isn't running then the
                              return dict will have multipath as False.
    :type enforce_multipath: bool
    :param host: hostname.
    :param execute: execute helper.
    :returns: dict containing all of the collected initiator values.
    """
    props = {}
    props['platform'] = platform.machine()
    props['os_type'] = sys.platform
    props['ip'] = my_ip
    props['host'] = host if host else socket.gethostname()

    for item in connector_list:
        connector = importutils.import_class(item)

        if (utils.platform_matches(props['platform'], connector.platform) and
           utils.os_matches(props['os_type'], connector.os_type)):
            props = utils.merge_dict(props,
                                     connector.get_connector_properties(
                                         root_helper,
                                         host=host,
                                         multipath=multipath,
                                         enforce_multipath=enforce_multipath,
                                         execute=execute))

    return props


# TODO(walter-boring) We have to keep this class defined here
# so we don't break backwards compatibility
class InitiatorConnector(object):

    @staticmethod
    def factory(protocol, root_helper, driver=None,
                use_multipath=False,
                device_scan_attempts=initiator.DEVICE_SCAN_ATTEMPTS_DEFAULT,
                arch=None,
                *args, **kwargs):
        """Build a Connector object based upon protocol and architecture."""

        # We do this instead of assigning it in the definition
        # to help mocking for unit tests
        if arch is None:
            arch = platform.machine()

        # Set the correct mapping for imports
        if sys.platform == 'win32':
            _mapping = _connector_mapping_windows
        elif arch in (initiator.S390, initiator.S390X):
            _mapping = _connector_mapping_linux_s390x
        else:
            _mapping = _connector_mapping_linux

        LOG.debug("Factory for %(protocol)s on %(arch)s",
                  {'protocol': protocol, 'arch': arch})
        protocol = protocol.upper()

        # set any special kwargs needed by connectors
        if protocol in (initiator.NFS, initiator.GLUSTERFS,
                        initiator.SCALITY, initiator.QUOBYTE,
                        initiator.VZSTORAGE):
            kwargs.update({'mount_type': protocol.lower()})
        elif protocol == initiator.ISER:
            kwargs.update({'transport': 'iser'})
        elif protocol == OPENVSTORAGE_EDGE:
            return OpenvStorageEdgeConnector(root_helper=root_helper,
                                             driver=driver,
                                             device_scan_attempts=device_scan_attempts,
                                             *args, **kwargs)

        # now set all the default kwargs
        kwargs.update(
            {'root_helper': root_helper,
             'driver': driver,
             'use_multipath': use_multipath,
             'device_scan_attempts': device_scan_attempts,
             })

        connector = _mapping.get(protocol)
        if not connector:
            msg = (_("Invalid InitiatorConnector protocol "
                     "specified %(protocol)s") %
                   dict(protocol=protocol))
            raise exception.InvalidConnectorProtocol(msg)

        conn_cls = importutils.import_class(connector)
        return conn_cls(*args, **kwargs)

```

#### Connectors/openvstorage.py

This file is present in the following locations: 
* `/openstack/venvs/cinder-15.0.0/lib/python2.7/site-packages/os_brick/initiator/connectors/openvstorage.py`
* `/openstack/venvs/nova-14.1.1/lib/python2.7/site-packages/os_brick/initiator/connectors/openvstorage.py`

```
from oslo_log import log as logging
from oslo_utils import fileutils

from os_brick.initiator import initiator_connector

LOG = logging.getLogger(__name__)
DEVICE_SCAN_ATTEMPTS_DEFAULT = 3


class OpenvStorageEdgeConnector(initiator_connector.InitiatorConnector):
    def __init__(self, root_helper, driver=None, execute=None,
                 device_scan_attempts=DEVICE_SCAN_ATTEMPTS_DEFAULT,
                 *args, **kwargs):
        super(OpenvStorageEdgeConnector, self).__init__(root_helper, execute=execute,
                                                       *args, **kwargs)

    @staticmethod
    def get_connector_properties(root_helper, *args, **kwargs):
        """The generic connector properties."""
        return {}

    def check_valid_device(self, path, run_as_root=True):
        """Test to see if the device path is a real device.
        :param path: The file system path for the device.
        :type path: str
        :param run_as_root: run the tests as root user?
        :type run_as_root: bool
        :returns: bool
        """
        LOG.debug('OVSEdgeConnector check_valid_device {0}'.format(path))

    def connect_volume(self, connection_properties):
        """Connect to a volume.
        The connection_properties describes the information needed by
        the specific protocol to use to make the connection.
        The connection_properties is a dictionary that describes the target
        volume.  It varies slightly by protocol type (iscsi, fibre_channel),
        but the structure is usually the same.
        :param connection_properties: The dictionary that describes all
                                      of the target volume attributes.
        :type connection_properties: dict
        :returns: dict
        """
        LOG.debug('OVSEdgeConnector connect_volume {0}'.format(connection_properties))
        device_info = {'type': 'openvstorage_edge',
                       'path': connection_properties['device_path']}

        return device_info

    def disconnect_volume(self, connection_properties, device_info):
        """Disconnect a volume from the local host.
        The connection_properties are the same as from connect_volume.
        The device_info is returned from connect_volume.
        :param connection_properties: The dictionary that describes all
                                      of the target volume attributes.
        :type connection_properties: dict
        :param device_info: historical difference, but same as connection_props
        :type device_info: dict
        """
        LOG.debug('OVSEdgeConnector disconnect_volume {0} {1}'.format(connection_properties, device_info))

    def get_volume_paths(self, connection_properties):
        """Return the list of existing paths for a volume.
        The job of this method is to find out what paths in
        the system are associated with a volume as described
        by the connection_properties.
        :param connection_properties: The dictionary that describes all
                                      of the target volume attributes.
        :type connection_properties: dict
        """
        LOG.debug('OVSEdgeConnector get_volume_paths {0}'.format(connection_properties))
        path = connection_properties['device_path']
        return [path]

    def get_search_path(self):
        """Return the directory where a Connector looks for volumes.
        Some Connectors need the information in the
        connection_properties to determine the search path.
        """
        LOG.debug('OVSEdgeConnector get_search_path > returning None')
        return None

    def extend_volume(self, connection_properties):
        """Update the attached volume's size.
        This method will attempt to update the local hosts's
        volume after the volume has been extended on the remote
        system.  The new volume size in bytes will be returned.
        If there is a failure to update, then None will be returned.
        :param connection_properties: The volume connection properties.
        :returns: new size of the volume.
        """
        LOG.debug('OVSEdgeConnector extend_volume {0}'.format(connection_properties))

    def get_all_available_volumes(self, connection_properties=None):
        """Return all volumes that exist in the search directory.
        At connect_volume time, a Connector looks in a specific
        directory to discover a volume's paths showing up.
        This method's job is to return all paths in the directory
        that connect_volume uses to find a volume.
        This method is used in coordination with get_volume_paths()
        to verify that volumes have gone away after disconnect_volume
        has been called.
        :param connection_properties: The dictionary that describes all
                                      of the target volume attributes.
        :type connection_properties: dict
        """
        LOG.debug('OVSEdgeConnector get_all_available_volumes {0}'.format(connection_properties))
        return []

```

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
```

Restart the following services on all cinder nodes:
```
systemctl restart cinder-volume
systemctl restart cinder-backup
systemctl restart cinder-api
```

In the cinder-volume logs you should see the cinder driver initializing in the cinder volume manager:
```
root@osa-aio-ctrl:~# grep INIT /var/log/cinder/cinder-volume.log 
2017-03-17 12:56:52.554 14860 DEBUG cinder.volume.drivers.openvstorage_edge [req-1c0916ad-1b4e-4c75-911c-4efc7cb82ced - - - - -] INIT  26203 tcp () {'is_vol_db_empty': False, 'db': <module 'cinder.db' from '/openstack/venvs/cinder-15.0.0/lib/python2.7/site-packages/cinder/db/__init__.pyc'>, 'cluster_name': None, 'host': 'osa-aio-ctrl@myvpool01', 'active_backend_id': None, 'configuration': <cinder.volume.configuration.Configuration object at 0x7ffbcbad6750>} __init__ /openstack/venvs/cinder-15.0.0/lib/python2.7/site-packages/cinder/volume/drivers/openvstorage_edge.py:58
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

Nova driver location: `/openstack/venvs/nova-15.0.0/lib/python2.7/site-packages/nova/virt/libvirt/driver.py`

Nova config location: `/openstack/venvs/nova-15.0.0/lib/python2.7/site-packages/nova/virt/libvirt/config.py`

Open vStorage nova driver: `/openstack/venvs/nova-15.0.0/lib/python2.7/site-packages/nova/virt/libvirt/volume/openvstorage_edge.py`

Nova config file: `/etc/nova/nova.conf`

**Remarks:** The openvstorage nova plugin, `config.py` & `driver.py` should be installed where: `nova-compute` is running

### Installing the nova driver

Install the following nova driver in Open Stack: `/openstack/venvs/nova-15.0.0/lib/python2.7/site-packages/nova/virt/libvirt/volume/openvstorage_edge.py`

```
# Copyright 2016 iNuron NV
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
OpenStack Nova driver - interface to Open vStorage Edge for qemu
- requires qemu, libvirt-bin packages from openvstorage repo
- see also config_PATCH
"""

from os_brick.initiator import connector
from oslo_log import log as logging

from nova import utils
from nova.virt.libvirt.volume.volume import LibvirtVolumeDriver
from nova.virt.libvirt import config as vconfig
from nova.virt.libvirt import utils as libvirt_utils

LOG = logging.getLogger(__name__)


class LibvirtOpenvStorageEdgeVolumeDriver(LibvirtVolumeDriver):
    """
    Class for volumes backed by OpenvStorage Edge
    """
    def __init__(self, connection):
        super(LibvirtOpenvStorageEdgeVolumeDriver, self).__init__(connection)
        self.connector = connector.InitiatorConnector.factory('OPENVSTORAGE_EDGE', utils.get_root_helper())

    def get_config(self, connection_info, disk_info):
        """Returns xml for libvirt."""
        conf = vconfig.LibvirtConfigOpenvStorageEdgeGuestDisk()
        conf.driver_name = libvirt_utils.pick_disk_driver_name(self.connection._host.get_version(),
                                                               self.is_block_dev)

        source_path = connection_info['data']['device_path']
        #u'device_path': u'openvstorage+tcp:10.130.11.202:26203/volimage3'
        ovs_proto, host, port_volume = source_path.split(':')
        port, name = port_volume.split('/')
        _, transport = ovs_proto.split('+')

        conf.source_name = name
        conf.source_host_name = host
        conf.source_host_port = port
        conf.source_host_transport = transport

        conf.target_dev = disk_info['dev']
        conf.target_bus = disk_info['bus']
        conf.serial = connection_info.get('serial')

        return conf

    def connect_volume(self, connection_info, disk_info):
        """Attach the volume to instance_name."""
        LOG.debug("Calling os-brick to attach Volume")
        device_info = self.connector.connect_volume(connection_info['data'])
        LOG.debug("Attached volume %s", device_info)
        connection_info['data']['device_path'] = device_info['path']

    def disconnect_volume(self, connection_info, disk_dev):
        """Detach the volume from instance_name."""
        LOG.debug("Calling os-brick to detach Volume")
        self.connector.disconnect_volume(connection_info['data'], None)
        LOG.debug("Detached volume")
```

### Patching driver & config.py

#### config.py

Nova config location: `/openstack/venvs/nova-15.0.0/lib/python2.7/site-packages/nova/virt/libvirt/config.py`

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

Nova driver location: `/openstack/venvs/nova-15.0.0/lib/python2.7/site-packages/nova/virt/libvirt/driver.py`

You should add a `libvirt_volume_driver` to the list called `openvstorage_edge=nova.virt.libvirt.volume.openvstorage_edge.LibvirtOpenvStorageEdgeVolumeDriver` on line 148

Now restart the `nova-compute` services on all nova nodes: `systemctl restart nova-compute`