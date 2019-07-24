import requests
import json
import datetime
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning

start = time.time()

# disable ssl warnings for self signed certs
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# global auth variables
host = input("Enter vROPs FQDN: ")
username = input("Enter a user that has access to vROPs: ")
password = input("Enter the password for the specified user: ")
port = input('Enter the port for vROPs: ')
cust_id = input('Please enter a customer ID: ')

# random vars
formatting = datetime.datetime.now()

# resource kinds
virtual_machines = {}
host_systems = {}
host_clusters = {}
vmware_dvs = {}
dvs_portgroups = {}
datastore = {}
vmware_adapter_resources = {}

# stats to pull data for
stat_keys = [
    "mem|usage_average", "OnlineCapacityAnalytics|diskspace|capacityRemaining", "cpu|usage_average"
]

prop_keys = [
    "config|hardware|diskSpace", "config|hardware|memoryKB", "config|hardware|numCpu", "config|name",
    "config|product|apiVersion", "config|version", "cpu|cpuModel", 
    "hardware|cpuInfo|hz", "hardware|cpuInfo|numCpuCores", "hardware|cpuInfo|numCpuPackages",
    "hardware|memorySize", "hardware|serialNumberTag", "hardware|vendor", "hardware|vendorModel",
    "runtime|connectionState", "runtime|maintenanceState", "runtime|powerState", "summary|datastore",
    "summary|folder", "summary|guest|fullName", "summary|guest|toolsRunningStatus",
    "summary|guest|toolsVersion", "summary|guest|toolsVersionStatus", 
    "summary|guest|toolsVersionStatus2", "summary|MOID", "summary|parentCluster", 
    "summary|parentDatacenter", "summary|parentHost", "summary|parentVcenter",
    "summary|runtime|powerState", "summary|total_number_vms", "summary|UUID", "summary|version",
    "sys|build", "sys|productString"
]


# global dict for objects
dice_json = {
    'source': 'vrops',
    'vrops': host,
    "customer_id": cust_id,
    'collect_time': '',
    'vms': {},
    'hosts': {},
    'clusters': {},
    'dvs': {},
    'pgs': {},
    'datastores': {}
    }


def pull_data_from_vrops():
    # formatting vROPS API URL
    # ------------------------------------------------------
    def vrops_url():
        url = "https://" + host + ':' + port + '/suite-api/api'
        return url
    # ------------------------------------------------------
    # creating vROPs API URL
    vrops_url = vrops_url()
    # ------------------------------------------------------
    # setting auth values
    auth_values = (username, password)
    # ------------------------------------------------------
    def get_vmware_adapter_resources(page, pagesize):
        """ This functions builds a list of resources in vRealize Operations by type VMware adapter. """
        page = str(page)
        pagesize = str(pagesize)
        headers = {'Accept': 'application/json'}
        new_url = vrops_url + '/adapterkinds/VMWARE/resources' + '?page=' + page + '&' + 'pageSize=' + pagesize
        response = requests.request("GET", url=new_url, headers=headers, auth=auth_values, verify=False)
        return response.text
    # ------------------------------------------------------
    # building global resource list
    def build_global_resource_list():
        i = 0
        rslist_len = 1
        while rslist_len != 0:
            testing = json.loads(get_vmware_adapter_resources(i, 1000))
            rslist_len = len(testing['resourceList'])
            vmware_adapter_resources.update({i: testing})
            i = i + 1
    # ------------------------------------------------------
    def populate_global_variables():
        """ This function populates global variables for resource kinds. """
        for p in vmware_adapter_resources:
            for i in vmware_adapter_resources[p]['resourceList']:
                if i['resourceKey']['resourceKindKey'] == 'VirtualMachine':
                    virtual_machines.update({i['identifier']: i['resourceKey']['name']})
                if i['resourceKey']['resourceKindKey'] == 'HostSystem':
                    host_systems.update({i['identifier']: i['resourceKey']['name']})
                # commented out objects below for future collection - not needed now
                # if i['resourceKey']['resourceKindKey'] == 'ClusterComputeResource':
                #     host_clusters.update({i['identifier']: i['resourceKey']['name']})
                # if i['resourceKey']['resourceKindKey'] == 'VmwareDistributedVirtualSwitch':
                #     vmware_dvs.update({i['identifier']: i['resourceKey']['name']})
                # if i['resourceKey']['resourceKindKey'] == 'DistributedVirtualPortgroup':
                #     dvs_portgroups.update({i['identifier']: i['resourceKey']['name']})
                # if i['resourceKey']['resourceKindKey'] == 'Datastore':
                #     datastore.update({i['identifier']: i['resourceKey']['name']})
    # ------------------------------------------------------
    def get_resource_latest_stats(ident):
        """ This function retrieves a full list of the latest stats for an object in vRealize Operations. """
        headers = {'Accept': 'application/json'}
        new_url = vrops_url + '/resources/' + ident + '/stats/latest'
        response = requests.request("GET", url=new_url, headers=headers, auth=auth_values, verify=False)
        return response.text
    # ------------------------------------------------------
    def get_res_properties(ident):
        """ This function retrieves a full list of the latest stats for an object in vRealize Operations. """
        headers = {'Accept': 'application/json'}
        new_url = vrops_url + '/resources/' + ident + '/properties'
        response = requests.request("GET", url=new_url, headers=headers, auth=auth_values, verify=False)
        return response.text
    # ------------------------------------------------------
    def get_res_parent(ident):
        """ This function retrieves the parent for an object in vRealize Operations. """
        headers = {'Accept': 'application/json'}
        new_url = vrops_url + '/resources/' + ident + '/relationships/parents'
        response = requests.request("GET", new_url, headers=headers, auth=auth_values, verify=False)
        return response.text
    # ------------------------------------------------------
    def get_stat_keys(k):
        stats = json.loads(get_resource_latest_stats(k))
        obj_dict = {}
        for i in stats['values']:
            for e in i['stat-list']['stat']:
                try:
                    if e.get('statKey', {}).get('key') in stat_keys and e['data'][0] is not None:
                        obj_dict.update({e['statKey']['key']: e['data'][0]})
                except:
                    continue
        return obj_dict
    # ------------------------------------------------------
    def get_props(k):
        properties = json.loads(get_res_properties(k))
        obj_dict = {}
        for p in properties['property']:
            try:
                if p.get('name') in prop_keys:
                    obj_dict.update({p['name']: p['value']})
            except:
                continue
        return obj_dict
    # ------------------------------------------------------
    def populate_object_data():
        for k in virtual_machines:
            dice_json['vms'].update({k: {'name': virtual_machines[k]}})
            dice_json['vms'][k].update(get_stat_keys(k))
        for k in host_systems:
            dice_json['hosts'].update({k: {'name': host_systems[k]}})
            dice_json['hosts'][k].update(get_stat_keys(k))
        # commented out objects below for future collection - not needed now
        # for k in host_clusters:
        #     dice_json['clusters'].update({k: {'name': host_clusters[k]}})
        #     dice_json['clusters'][k].update(get_stat_keys(k))
        # for k in vmware_dvs:
        #     dice_json['dvs'].update({k: {'name': vmware_dvs[k]}})
        #     dice_json['dvs'][k].update(get_stat_keys(k))
        # for k in dvs_portgroups:
        #     dice_json['pgs'].update({k: {'name': dvs_portgroups[k]}})
        #     dice_json['pgs'][k].update(get_stat_keys(k))
        # for k in datastore:
        #     dice_json['datastores'].update({k: {'name': datastore[k]}})
        #     dice_json['datastores'][k].update(get_stat_keys(k))
    # ------------------------------------------------------
    def populate_object_properties():
        for k in virtual_machines:
            dice_json['vms'][k].update(get_props(k))
        for k in host_systems:
            dice_json['hosts'][k].update(get_props(k))
        # commented out objects below for future collection - not needed now
        # for k in host_clusters:
        #     dice_json['clusters'][k].update(get_props(k))
        # for k in vmware_dvs:
        #     dice_json['dvs'][k].update(get_props(k))
        # for k in dvs_portgroups:
        #     dice_json['pgs'][k].update(get_props(k))
        # for k in datastore:
        #     dice_json['datastores'][k].update(get_props(k))
    # ------------------------------------------------------
    # commented out objects below for future collection - not needed now
    # def populate_object_parents():
    #     for k in vmware_dvs:
    #         parent = json.loads(get_res_parent(k))
    #         for p in parent['resourceList']:
    #             try:
    #                 if p['resourceKey']['adapterKindKey'] == 'VMWARE' and p['resourceKey']['resourceKindKey'] == 'Datacenter':
    #                     key = 'objectParent'
    #                     value = p['resourceKey']['name']
    #                     dice_json['dvs'][k].update({key: value})
    #             except KeyError:
    #                 pass
    #     for k in dvs_portgroups:
    #         parent = json.loads(get_res_parent(k))
    #         for p in parent['resourceList']:
    #             try:
    #                 if p['resourceKey']['adapterKindKey'] == 'VMWARE' and p['resourceKey']['resourceKindKey'] == 'VmwareDistributedVirtualSwitch':
    #                     key = 'objectParent'
    #                     value = p['resourceKey']['name']
    #                     dice_json['pgs'][k].update({key: value})
    #             except KeyError:
    #                 pass
    # ------------------------------------------------------
    # calls all populate functions
    def populate_data():
        build_global_resource_list()
        populate_global_variables()
        populate_object_data()
        populate_object_properties()
        # populate_object_parents()
    # ------------------------------------------------------
    dice_json['filename'] = 'dice_vrops_output_' + formatting.strftime("%Y_%m_%d_%H_%M") + '.json'
    # populating global data
    populate_data()


pull_data_from_vrops()

fw_time = time.time()
before_write_time = fw_time - start
dice_json['collect_time'] = round(before_write_time, 2)
print(f'it took {before_write_time} seconds to run before writing the file')

dice_file = 'dice_vrops_output_' + formatting.strftime("%Y_%m_%d_%H_%M") + '.json'
with open('static/json/' + dice_file, 'w') as j:
    json.dump(dice_json, j, indent=4)

end = time.time()
comp_time = end - start
print(f'it took {comp_time} seconds to finish total')