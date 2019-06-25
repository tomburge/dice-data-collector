import requests
import json
import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# disable ssl warnings for self signed certs
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# global auth variables
# host = input("Enter vROPs FQDN: ")
# username = input("Enter a user that has access to vROPs: ")
# password = input("Enter the password for the specified user: ")

# random vars
cust_id = 'CUST-1234567890'
formatting = datetime.datetime.now()

# resource kinds
virtual_machines = {}
host_systems = {}
host_clusters = {}
vmware_dvs = {}
dvs_portgroups = {}
datastore = {}



vmware_adapter_resources = {}

with open('att_resources_debug.json') as json_file:
    data = json.load(json_file)

# global dict for objects
dice_json = {
    'source': 'vrops',
    'vrops': '',
    "customer_id": cust_id,
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
    # def vrops_url():
    #     url = "https://" + host + '/suite-api/api'
    #     return url
    # ------------------------------------------------------
    # creating vROPs API URL
    # vrops_url = vrops_url()
    # ------------------------------------------------------
    # setting auth values
    # auth_values = (username, password)
    # ------------------------------------------------------

    # def get_vmware_adapter_resources(page, pagesize):
    #     """ This functions builds a list of resources in vRealize Operations by type VMware adapter. """
    #     page = str(page)
    #     pagesize = str(pagesize)
    #     headers = {'Accept': 'application/json'}
    #     new_url = vrops_url + '/adapterkinds/VMWARE/resources' + '?page=' + page + '&' + 'pageSize=' + pagesize
    #     response = requests.request("GET", url=new_url, headers=headers, auth=auth_values, verify=False)
    #     return response.text
    # ------------------------------------------------------
    # building global resource list

    # def build_global_resource_list():
    #     i = 0
    #     rslist_len = 1
    #     while rslist_len != 0:
    #         # testing = json.loads(get_vmware_adapter_resources(i, 1000))
    #         rslist_len = len(data['resourceList'])
    #         vmware_adapter_resources.update({i: data})
    #         i = i + 1
    # ------------------------------------------------------

    def populate_global_variables():
        """ This function populates global variables for resource kinds. """
        for p in data:
            for i in data[p]['resourceList']:
                if i['resourceKey']['resourceKindKey'] == 'VirtualMachine':
                    virtual_machines.update({i['identifier']: i['resourceKey']['name']})
                if i['resourceKey']['resourceKindKey'] == 'HostSystem':
                    host_systems.update({i['identifier']: i['resourceKey']['name']})
                if i['resourceKey']['resourceKindKey'] == 'ClusterComputeResource':
                    host_clusters.update({i['identifier']: i['resourceKey']['name']})
                if i['resourceKey']['resourceKindKey'] == 'VmwareDistributedVirtualSwitch':
                    vmware_dvs.update({i['identifier']: i['resourceKey']['name']})
                if i['resourceKey']['resourceKindKey'] == 'DistributedVirtualPortgroup':
                    dvs_portgroups.update({i['identifier']: i['resourceKey']['name']})
                if i['resourceKey']['resourceKindKey'] == 'Datastore':
                    datastore.update({i['identifier']: i['resourceKey']['name']})
    # ------------------------------------------------------

    # def get_resource_latest_stats(ident):
    #     """ This function retrieves a full list of the latest stats for an object in vRealize Operations. """
    #     headers = {'Accept': 'application/json'}
    #     ident = ident
    #     new_url = vrops_url + '/resources/' + ident + '/stats/latest'
    #     response = requests.request("GET", url=new_url, headers=headers, auth=auth_values, verify=False)
    #     return response.text
    # ------------------------------------------------------

    # def get_res_properties(ident):
    #     """ This function retrieves a full list of the latest stats for an object in vRealize Operations. """
    #     headers = {'Accept': 'application/json'}
    #     ident = ident
    #     new_url = vrops_url + '/resources/' + ident + '/properties'
    #     response = requests.request("GET", url=new_url, headers=headers, auth=auth_values, verify=False)
    #     return response.text
    # ------------------------------------------------------

    # def get_res_parent(ident):
    #     """ This function retrieves the parent for an object in vRealize Operations. """
    #     headers = {'Accept': 'application/json'}
    #     ident = ident
    #     new_url = vrops_url + '/resources/' + ident + '/relationships/parents'
    #     response = requests.request("GET", new_url, headers=headers, auth=auth_values, verify=False)
    #     return response.text
    # ------------------------------------------------------
    # merge the many similar functions below this block into common functions
    def populate_object_data():
        pass
    def populate_object_properties():
        pass
    def populate_object_parents():
        pass
    # ------------------------------------------------------

    def populate_virtual_machine():
        for k in virtual_machines:
            stats = json.loads(get_resource_latest_stats(k))
            dice_json['vms'].update({k: {'name': virtual_machines[k]}})
            for i in stats['values']:
                for e in i['stat-list']['stat']:
                    key = e['statKey']['key']
                    value = e['data'][0]
                    dice_json['vms'][k].update({key: value})
    # ------------------------------------------------------

    def populate_virtual_machine_properties():
        for k in virtual_machines:
            properties = json.loads(get_res_properties(k))
            for p in properties['property']:
                key = p['name']
                value = p['value']
                dice_json['vms'][k].update({key: value})
    # ------------------------------------------------------

    def populate_host_system():
        for k in host_systems:
            stats = json.loads(get_resource_latest_stats(k))
            dice_json['hosts'].update({k: {'name': host_systems[k]}})
            for i in stats['values']:
                for e in i['stat-list']['stat']:
                    key = e['statKey']['key']
                    value = e['data'][0]
                    dice_json['hosts'][k].update({key: value})
    # ------------------------------------------------------

    def populate_host_system_properties():
        for k in host_systems:
            properties = json.loads(get_res_properties(k))
            for p in properties['property']:
                key = p['name']
                value = p['value']
                dice_json['hosts'][k].update({key: value})
    # ------------------------------------------------------

    def populate_host_cluster():
        for k in host_clusters:
            stats = json.loads(get_resource_latest_stats(k))
            dice_json['clusters'].update({k: {'name': host_clusters[k]}})
            for i in stats['values']:
                for e in i['stat-list']['stat']:
                    key = e['statKey']['key']
                    value = e['data'][0]
                    dice_json['clusters'][k].update({key: value})
    # ------------------------------------------------------

    def populate_host_cluster_properties():
        for k in host_clusters:
            properties = json.loads(get_res_properties(k))
            for p in properties['property']:
                key = p['name']
                value = p['value']
                dice_json['clusters'][k].update({key: value})
    # ------------------------------------------------------

    def populate_vmware_dvs():
        for k in vmware_dvs:
            stats = json.loads(get_resource_latest_stats(k))
            dice_json['dvs'].update({k: {'name': vmware_dvs[k]}})
            for i in stats['values']:
                for e in i['stat-list']['stat']:
                    key = e['statKey']['key']
                    value = e['data'][0]
                    dice_json['dvs'][k].update({key: value})
    # ------------------------------------------------------

    def populate_vmware_dvs_properties():
        for k in vmware_dvs:
            properties = json.loads(get_res_properties(k))
            for p in properties['property']:
                key = p['name']
                value = p['value']
                dice_json['dvs'][k].update({key: value})
    # ------------------------------------------------------

    def populate_vmware_dvs_parents():
        for k in vmware_dvs:
            parent = json.loads(get_res_parent(k))
            for p in parent['resourceList']:
                if p['resourceKey']['adapterKindKey'] == 'VMWARE' and p['resourceKey']['resourceKindKey'] == 'Datacenter':
                    key = 'objectParent'
                    value = p['resourceKey']['name']
                    dice_json['dvs'][k].update({key: value})
    # ------------------------------------------------------

    def populate_dvs_portgroups():
        for k in dvs_portgroups:
            stats = json.loads(get_resource_latest_stats(k))
            dice_json['pgs'].update({k: {'name': dvs_portgroups[k]}})
            for i in stats['values']:
                for e in i['stat-list']['stat']:
                    key = e['statKey']['key']
                    value = e['data'][0]
                    dice_json['pgs'][k].update({key: value})
    # ------------------------------------------------------

    def populate_dvs_portgroups_properties():
        for k in dvs_portgroups:
            properties = json.loads(get_res_properties(k))
            for p in properties['property']:
                key = p['name']
                value = p['value']
                dice_json['pgs'][k].update({key: value})
    # ------------------------------------------------------

    def populate_dvs_portgroups_parents():
        for k in dvs_portgroups:
            parent = json.loads(get_res_parent(k))
            for p in parent['resourceList']:
                if p['resourceKey']['adapterKindKey'] == 'VMWARE' and p['resourceKey']['resourceKindKey'] == 'VmwareDistributedVirtualSwitch':
                    key = 'objectParent'
                    value = p['resourceKey']['name']
                    dice_json['pgs'][k].update({key: value})
    # ------------------------------------------------------

    def populate_datastore():
        for k in datastore:
            stats = json.loads(get_resource_latest_stats(k))
            dice_json['datastores'].update({k: {'name': datastore[k]}})
            for i in stats['values']:
                for e in i['stat-list']['stat']:
                    key = e['statKey']['key']
                    value = e['data'][0]
                    dice_json['datastores'][k].update({key: value})
    # ------------------------------------------------------

    def populate_datastore_properties():
        for k in datastore:
            properties = json.loads(get_res_properties(k))
            for p in properties['property']:
                key = p['name']
                value = p['value']
                dice_json['datastores'][k].update({key: value})
    # ------------------------------------------------------
    # calls all populate functions

    def populate_data():
        # build_global_resource_list()
        populate_global_variables()

        # create debug file for the global vmware adapter resources variable
        # with open('resources_debug.json', 'w') as jw:
        #     json.dump(vmware_adapter_resources, jw, indent=4)

        # populate_virtual_machine()
        # populate_virtual_machine_properties()
        # populate_host_system()
        # populate_host_system_properties()
        # populate_host_cluster()
        # populate_host_cluster_properties()
        # populate_vmware_dvs()
        # populate_vmware_dvs_properties()
        # populate_vmware_dvs_parents()
        # populate_dvs_portgroups()
        # populate_dvs_portgroups_properties()
        # populate_dvs_portgroups_parents()
        # populate_datastore()
        # populate_datastore_properties()
    # ------------------------------------------------------

    dice_json['filename'] = 'dice_vrops_output_' + formatting.strftime("%Y_%m_%d_%H_%M") + '.json'
    # populating global data
    populate_data()

    # print(len(virtual_machines)) # 2129 VMs
    # print(len(host_systems)) # 213 hosts
    # print(len(host_clusters)) # 56 clusters
    # print(len(vmware_dvs)) # 13 dvs
    # print(len(dvs_portgroups)) # 52 portgroups
    # print(len(datastore)) # 1900 datastores


pull_data_from_vrops()

dice_file = 'dice_vrops_output_' + formatting.strftime("%Y_%m_%d_%H_%M") + '.json'
with open('static/json/' + dice_file, 'w') as j:
    json.dump(dice_json, j, indent=4)