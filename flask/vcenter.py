import ssl
import json
import datetime
import time
from pyVim import connect
from pyVmomi import vmodl
from pyVmomi import vim
import vc_info as info

# global dict for objects
dice_json = {
    'source': 'vcenter',
    'vcenter': '',
    'customer_id': '',
    'collect_time': '',
    'filename': '',
    'vms': {},
    'hosts': {},
    'clusters': {},
    'dvs': {},
    'pgs': {},
    'datastores': {}
    }


def pull_data_from_vcenter(vchost, vcuser, vcpass, vcport, customer_id):

    start = time.time()
    
    # ssl context setting
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.verify_mode = ssl.CERT_NONE

    # connect service instance
    service_instance = connect.SmartConnect(host=vchost, user=vcuser, pwd=vcpass, port=int(vcport), sslContext=context)
    content = service_instance.RetrieveContent()
    object_view = content.viewManager.CreateContainerView(content.rootFolder, [], True)

    for obj in object_view.view:

        try:
            if isinstance(obj, vim.VirtualMachine):
                vm_obj = info.get_vm_info(obj)
                dice_json['vms'].update(vm_obj)
            if isinstance(obj, vim.HostSystem):
                host_obj = info.get_host_info(obj)
                dice_json['hosts'].update(host_obj)
        except:
            continue
        # commented out objects below for future collection - not needed now
        # if isinstance(obj, vim.ClusterComputeResource):
        #     cluster_obj = info.get_cluster_info(obj)
        #     dice_json['clusters'].update(cluster_obj)
        # if isinstance(obj, vim.Datastore):
        #     ds_obj = info.get_ds_info(obj)
        #     dice_json['datastores'].update(ds_obj)
        # if isinstance(obj, vim.VmwareDistributedVirtualSwitch):
        #     vds_obj = info.get_net_info(obj)
        #     dice_json['dvs'].update(vds_obj)
        # if isinstance(obj, vim.DistributedVirtualPortgroup):
        #     pg_obj = info.get_pg_info(obj)
        #     dice_json['pgs'].update(pg_obj)
    # ------------------------------------------------------
    # building var for filename format
    formatting = datetime.datetime.now()
    # updating global dict for identifying data
    dice_json['customer_id'] = customer_id
    dice_json['vcenter'] = vchost
    dice_json['filename'] = 'dice_vc_output_' + formatting.strftime("%Y_%m_%d_%H_%M") + '.json'
    # ------------------------------------------------------
    fw_time = time.time()
    before_write_time = fw_time - start
    dice_json['collect_time'] = round(before_write_time, 2)
    print(f'it took {before_write_time} seconds to run before writing the file')
    
    # writing JSON
    dice_file = 'dice_vc_output_' + formatting.strftime("%Y_%m_%d_%H_%M") + '.json'
    with open('static/json/' + dice_file, 'w') as j:
        json.dump(dice_json, j, indent=4)
    
    end = time.time()
    comp_time = end - start
    print(f'it took {comp_time} seconds to finish total')

    return 'complete'
