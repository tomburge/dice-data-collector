import ssl
import json
from pyVim import connect
from pyVmomi import vmodl
from pyVmomi import vim
import vc_info as info

# global auth vars
host = input('Enter the vCenter FQDN: ')
user = input('Enter the username for vCenter: ')
pwd = input('Enter the password for the user: ')
port = 443

# ssl context setting
context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
context.verify_mode = ssl.CERT_NONE

# connect service instance
service_instance = connect.SmartConnect(host=host, user=user, pwd=pwd, port=int(port), sslContext=context)
content = service_instance.RetrieveContent()
object_view = content.viewManager.CreateContainerView(content.rootFolder, [], True)

# global dict for objects
dice_json = {
    'source': 'vcenter',
    'vcenter': host,
    'vms': {},
    'hosts': {},
    'clusters': {},
    'dvs': {},
    'pgs': {},
    'datastores': {}
    }

for obj in object_view.view:
    if isinstance(obj, vim.VirtualMachine):
        vm_obj = info.get_vm_info(obj)
        dice_json['vms'].update(vm_obj)
    if isinstance(obj, vim.HostSystem):
        host_obj = info.get_host_info(obj)
        dice_json['hosts'].update(host_obj)
    if isinstance(obj, vim.ClusterComputeResource):
        cluster_obj = info.get_cluster_info(obj)
        dice_json['clusters'].update(cluster_obj)
    if isinstance(obj, vim.Datastore):
        ds_obj = info.get_ds_info(obj)
        dice_json['datastores'].update(ds_obj)
    if isinstance(obj, vim.VmwareDistributedVirtualSwitch):
        vds_obj = info.get_net_info(obj)
        dice_json['dvs'].update(vds_obj)
    if isinstance(obj, vim.DistributedVirtualPortgroup):
        pg_obj = info.get_pg_info(obj)
        dice_json['pgs'].update(pg_obj)

with open('dice_vcenter.json', 'w') as j:
    json.dump(dice_json, j, indent=4)