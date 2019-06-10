import requests
import json
import os
import platform
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# disable ssl warnings for self signed certs
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# global auth variables
host = ''
username = ''
password = ''

# resource kinds
virtual_machines = {}
host_systems = {}
host_clusters = {}
vmware_dvs = {}
dvs_portgroups = {}
datastore = {}
vmware_adapter_resouces = {}

# global dict for objects
dice_json = {
    'source': 'vrops',
    'vms': {},
    'hosts': {},
    'clusters':{},
    'dvs': {},
    'pgs': {},
    'datastores': {}
    }

def pull_data_from_vrops(vropshost, vropsuser, vropspass):
    # ------------------------------------------------------
    # Pulling data from flask form and populating global auth variables
    # ------------------------------------------------------
    host = vropshost
    username = vropsuser
    password = vropspass
    # ------------------------------------------------------
    # formatting vROPS API URL
    # ------------------------------------------------------
    def vrops_url():
        url = "https://" + host + '/suite-api/api'
        return url
    # ------------------------------------------------------
    # creating vROPs API URL
    vrops_url = vrops_url()
    # ------------------------------------------------------
    # setting auth values
    auth_values = (username, password)
    # ------------------------------------------------------
    def get_vmware_adapter_resources():
        """ This functions builds a full list of resources in vRealize Operations by type VMware adapter. """
        headers = {'Accept': 'application/json'}
        new_url = vrops_url + '/adapterkinds/VMWARE/resources'
        response = requests.request("GET", url=new_url, headers=headers, auth=auth_values, verify=False)
        return response.text
    # ------------------------------------------------------
    vmware_adapter_resouces = json.loads(get_vmware_adapter_resources())
    # ------------------------------------------------------
    def populate_global_variables():
        """ This function populates global variables for resource kinds. """
        for i in vmware_adapter_resouces['resourceList']:
            if i['resourceKey']['resourceKindKey'] == 'VirtualMachine':
                virtual_machines.update({i['resourceKey']['name']: i['identifier']})
            if i['resourceKey']['resourceKindKey'] == 'HostSystem':
                host_systems.update({i['resourceKey']['name']: i['identifier']})
            if i['resourceKey']['resourceKindKey'] == 'ClusterComputeResource':
                host_clusters.update({i['resourceKey']['name']: i['identifier']})
            if i['resourceKey']['resourceKindKey'] == 'VmwareDistributedVirtualSwitch':
                vmware_dvs.update({i['resourceKey']['name']: i['identifier']})
            if i['resourceKey']['resourceKindKey'] == 'DistributedVirtualPortgroup':
                dvs_portgroups.update({i['resourceKey']['name']: i['identifier']})
            if i['resourceKey']['resourceKindKey'] == 'Datastore':
                datastore.update({i['resourceKey']['name']: i['identifier']})
    # ------------------------------------------------------
    def get_resource_latest_stats(ident):
        """ This function retrieves a full list of the latest stats for an object in vRealize Operations. """
        headers = {'Accept': 'application/json'}
        identity = ident
        new_url = vrops_url + '/resources/' + ident + '/stats/latest'
        response = requests.request("GET", url=new_url, headers=headers, auth=auth_values, verify=False)
        return response.text
    # ------------------------------------------------------
    def get_res_properties(ident):
        """ This function retrieves a full list of the latest stats for an object in vRealize Operations. """
        headers = {'Accept': 'application/json'}
        identity = ident
        new_url = vrops_url + '/resources/' + ident + '/properties'
        response = requests.request("GET", url=new_url, headers=headers, auth=auth_values, verify=False)
        return response.text
    # ------------------------------------------------------
    def populate_virtual_machine():
        for k in virtual_machines:
            stats = json.loads(get_resource_latest_stats(virtual_machines[k]))
            dice_json['vms'].update({k: {'identifier': virtual_machines[k]}})
            for i in stats['values']:
                for e in i['stat-list']['stat']:
                    key = e['statKey']['key']
                    value = e['data'][0]
                    dice_json['vms'][k].update({key: value})
    # ------------------------------------------------------
    def populate_virtual_machine_properties():
        for k in virtual_machines:
            properties = json.loads(get_res_properties(virtual_machines[k]))
            for p in properties['property']:
                key = p['name']
                value = p['value']
                dice_json['vms'][k].update({key: value})
    # ------------------------------------------------------
    def populate_host_system():
        for k in host_systems:
            stats = json.loads(get_resource_latest_stats(host_systems[k]))
            dice_json['hosts'].update({k: {'identifier': host_systems[k]}})
            for i in stats['values']:
                for e in i['stat-list']['stat']:
                    key = e['statKey']['key']
                    value = e['data'][0]
                    dice_json['hosts'][k].update({key: value})
    # ------------------------------------------------------
    def populate_host_system_properties():
        for k in host_systems:
            properties = json.loads(get_res_properties(host_systems[k]))
            for p in properties['property']:
                key = p['name']
                value = p['value']
                dice_json['hosts'][k].update({key: value})
    # ------------------------------------------------------
    def populate_host_cluster():
        for k in host_clusters:
            stats = json.loads(get_resource_latest_stats(host_clusters[k]))
            dice_json['clusters'].update({k: {'identifier': host_clusters[k]}})
            for i in stats['values']:
                for e in i['stat-list']['stat']:
                    key = e['statKey']['key']
                    value = e['data'][0]
                    dice_json['clusters'][k].update({key: value})
    # ------------------------------------------------------
    def populate_vmware_dvs():
        for k in vmware_dvs:
            stats = json.loads(get_resource_latest_stats(vmware_dvs[k]))
            dice_json['dvs'].update({k: {'identifier': vmware_dvs[k]}})
            for i in stats['values']:
                for e in i['stat-list']['stat']:
                    key = e['statKey']['key']
                    value = e['data'][0]
                    dice_json['dvs'][k].update({key: value})
    # ------------------------------------------------------
    def populate_dvs_portgroups():
        for k in dvs_portgroups:
            stats = json.loads(get_resource_latest_stats(dvs_portgroups[k]))
            dice_json['pgs'].update({k: {'identifier': dvs_portgroups[k]}})
            for i in stats['values']:
                for e in i['stat-list']['stat']:
                    key = e['statKey']['key']
                    value = e['data'][0]
                    dice_json['pgs'][k].update({key: value})
    # ------------------------------------------------------
    def populate_datastore():
        for k in datastore:
            stats = json.loads(get_resource_latest_stats(datastore[k]))
            dice_json['datastores'].update({k: {'identifier': datastore[k]}})
            for i in stats['values']:
                for e in i['stat-list']['stat']:
                    key = e['statKey']['key']
                    value = e['data'][0]
                    dice_json['datastores'][k].update({key: value})
    # ------------------------------------------------------
    # calls all populate functions
    def populate_data():
        populate_global_variables()
        populate_virtual_machine()
        populate_virtual_machine_properties()
        populate_host_system()
        populate_host_system_properties()
        populate_host_cluster()
        populate_vmware_dvs()
        populate_dvs_portgroups()
        populate_datastore()
    # ------------------------------------------------------
    # populating global data
    populate_data()
    # ------------------------------------------------------
    return dice_json