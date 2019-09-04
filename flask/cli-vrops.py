import requests
import json
import datetime
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# disable ssl warnings for self signed certs
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# global auth variables
host = input("Enter vROPs FQDN: ")
username = input("Enter a user that has access to vROPs: ")
password = input("Enter the password for the specified user: ")
port = input('Enter the port for vROPs: ')
cust_id = input('Please enter a customer ID: ')

start = time.time()

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
test_vm = []
test_host = []

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
                    test_vm.append(i['identifier'])
                    virtual_machines.update({i['identifier']: i['resourceKey']['name']})
                if i['resourceKey']['resourceKindKey'] == 'HostSystem':
                    test_host.append(i['identifier'])
                    host_systems.update({i['identifier']: i['resourceKey']['name']})
    # ------------------------------------------------------
    def get_res_stats(ident):
        payload = {}
        if ident == 'vms':
            payload = {"intervalType": "HOURS", "intervalQuantifier": 1, "rollUpType": "AVG", "resourceId": test_vm, "statKey": stat_keys}
        elif ident == 'hosts':
            payload = {"intervalType": "HOURS", "intervalQuantifier": 1, "rollUpType": "AVG", "resourceId": test_host, "statKey": stat_keys}
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        new_url = vrops_url + '/resources/stats/query'
        response = requests.request("POST", url=new_url, headers=headers, json=payload, auth=auth_values, verify=False)
        return response.text
    # ------------------------------------------------------
    def get_res_properties(ident):
        """ This function retrieves a full list of the latest stats for all objects collected in vRealize Operations. """
        payload = {}
        if ident == 'vms':
            payload = {"resourceIds": test_vm, 'propertyKeys': prop_keys }
        elif ident == 'hosts':
            payload = {"resourceIds": test_host, 'propertyKeys': prop_keys }
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        new_url = vrops_url + '/resources/properties/latest/query'
        response = requests.request("POST", url=new_url, headers=headers, json=payload, auth=auth_values, verify=False)
        return response.text
    # ------------------------------------------------------
    def get_res_parent(ident):
        """ This function retrieves the parent for an object in vRealize Operations. """
        headers = {'Accept': 'application/json'}
        new_url = vrops_url + '/resources/' + ident + '/relationships/parents'
        response = requests.request("GET", new_url, headers=headers, auth=auth_values, verify=False)
        return response.text
    # ------------------------------------------------------
    def get_stats(ident):
        stats = json.loads(get_res_stats(ident))
        for stat in stats['values']:
            k = stat['resourceId']
            for s in stat['stat-list']['stat']:
                try:
                    if s.get('statKey', {}).get('key') in stat_keys:
                        dice_json[ident][k].update({s['statKey']['key'] : s['data'][0]})
                except:
                    continue
    # ------------------------------------------------------
    def get_props(ident):
        properties = json.loads(get_res_properties(ident))
        for p in properties['values']:
            k = p['resourceId']
            dice_json[ident].update({k: {}})
            for s in p['property-contents']['property-content']:
                try:
                    if s.get('statKey', {}) and s.get('values', {}):
                        dice_json[ident][k].update({s['statKey'] : s['values'][0]})
                    elif s.get('statKey', {}) and s.get('data', {}):
                        dice_json[ident][k].update({s['statKey'] : s['data'][0]})
                except:
                    continue
    # ------------------------------------------------------
    # def populate_object_name():
    #     for k in virtual_machines:
    #         try:
    #             print(k)
    #             print(virtual_machines[k])
    #             dice_json['vms'].update({k: {'name': virtual_machines[k]}})
    #         except:
    #             continue
    #     for k in host_systems:
    #         try:
    #             dice_json['hosts'].update({k: {'name': virtual_machines[k]}})
    #         except:
    #             continue
    # ------------------------------------------------------
    # calls all populate functions
    def populate_data():
        build_global_resource_list()
        populate_global_variables()
        get_props('vms')
        get_props('hosts')
        get_stats('vms')
        get_stats('hosts')
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