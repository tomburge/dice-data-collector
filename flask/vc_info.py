from pyVmomi import vim

def get_vm_info(vm, depth=1, max_depth=20):
    """ Get info for a particular virtual machine """

    # if this is a group it will have children. if it does, recurse into them and then return
    if hasattr(vm, 'childEntity'):
        if depth > max_depth:
            return
        vmlist = vm.childEntity
        for c in vmlist:
            get_vm_info(c, depth + 1)
        return

    config = vm.config
    network = vm.network
    parent = vm.parent
    resource_pool = vm.resourcePool
    summary = vm.summary

    vmtype = 'server'
    datacenter = ''
    vm_ds = ''
    switch = []
    netwk = {}
    portgroup = ''

    for i in config.extraConfig:
        if i.key == 'machine.id':
            vmtype = 'vdi'

    if network:
        if network is not None and type(network[0]) == vim.dvs.DistributedVirtualPortgroup:
            for i, net in enumerate(network):
                if network[i].name is not 'none' and network[i].summary.accessible is not False:
                    portgroup = network[0].name
                    if network[i].config.distributedVirtualSwitch.name is not None:
                        switch.append(network[i].config.distributedVirtualSwitch.name)
                        netwk.update({i: {str(network[i].config.distributedVirtualSwitch.name): network[i].name}})
                elif network[i].summary.accessible is False:
                    continue
                else:
                    switch.append('error')
                    portgroup = 'error'
                    netwk.update({'error': 'error'})
        elif type(network[0]) == vim.Network:
            for i, net in enumerate(network):
                if network[i].name is not 'none' and network[i].summary.accessible is not False:
                    portgroup = network[0].name
                    for s, vds in enumerate(summary.runtime.host.config.network.vswitch):
                        if summary.runtime.host.config.network.vswitch[s].name is not None:
                            switch.append(summary.runtime.host.config.network.vswitch[s].name)
                            netwk.update({i: {str(summary.runtime.host.config.network.vswitch[s].name): network[i].name}})
                elif network[i].summary.accessible is False:
                    continue
                else:
                    switch.append('error')
                    portgroup = 'error'
                    netwk.update({'error': 'error'})
    
    if config.datastoreUrl:
        vm_ds = config.datastoreUrl[0].name
    else:
        vm_ds = 'error'

    try:
        if parent and type(parent) == vim.Datacenter and type(parent) is not None:
            datacenter = parent.name
        elif parent.parent and type(parent.parent) == vim.Datacenter and type(parent.parent) is not None:
            datacenter = parent.parent.name
        elif parent.parent.parent and type(parent.parent.parent) == vim.Datacenter and type(parent.parent.parent) is not None:
            datacenter = parent.parent.parent.name
        elif parent.parent.parent.parent and type(parent.parent.parent.parent) == vim.Datacenter and type(parent.parent.parent.parent) is not None:
            datacenter = parent.parent.parent.parent.name
        elif parent.parent.parent.parent.parent and type(parent.parent.parent.parent.parent) == vim.Datacenter and type(parent.parent.parent.parent.parent) is not None:
            datacenter = parent.parent.parent.parent.parent.name
        elif parent.parent.parent.parent.parent.parent and type(parent.parent.parent.parent.parent.parent) == vim.Datacenter and type(parent.parent.parent.parent.parent.parent) is not None:
            datacenter = parent.parent.parent.parent.parent.parent.name
        elif parent.parent.parent.parent.parent.parent.parent and type(parent.parent.parent.parent.parent.parent.parent) == vim.Datacenter and type(parent.parent.parent.parent.parent.parent.parent) is not None:
            datacenter = parent.parent.parent.parent.parent.parent.parent.name
        elif parent.parent.parent.parent.parent.parent.parent.parent and type(parent.parent.parent.parent.parent.parent.parent.parent) == vim.Datacenter and type(parent.parent.parent.parent.parent.parent.parent.parent) is not None:
            datacenter = parent.parent.parent.parent.parent.parent.parent.parent.name
    except AttributeError as error:
            datacenter = 'error'

    try:
        instanceUuid = summary.config.instanceUuid
        cluster = summary.runtime.host.parent.name
        host = summary.runtime.host.name
        esx_version = summary.runtime.host.summary.config.product.version
        esx_type = summary.runtime.host.summary.config.product.name
        name = summary.vm.name
        num_cpu = summary.config.numCpu
        memory_gb = int(summary.config.memorySizeMB /1024)
        cpu_usage = summary.quickStats.overallCpuUsage
        cpu_demand = summary.quickStats.overallCpuDemand
        guest_mem_usage = int(summary.quickStats.guestMemoryUsage / 1024)
        host_mem_usage = int(summary.quickStats.hostMemoryUsage / 1024)
        balloon_mem = summary.quickStats.balloonedMemory
        swapped_mem = summary.quickStats.swappedMemory
        compressed_mem = summary.quickStats.compressedMemory
        uptime = summary.quickStats.uptimeSeconds
        guest_id = summary.guest.guestId
        os_name = summary.guest.guestFullName
        storage_used_gb = int(((summary.storage.committed / 1024) / 1024) / 1024)
        storage_alloc_gb = int(((summary.storage.uncommitted / 1024) / 1024) / 1024)
        tools_status = summary.guest.toolsStatus
        tools_ver_status = summary.guest.toolsVersionStatus
        tools_run_status = summary.guest.toolsRunningStatus
        tools_version = config.tools.toolsVersion
        vhw_version = config.version
        power_state = summary.runtime.powerState
        connection_state = summary.runtime.connectionState

        if resource_pool:
            res_pool = resource_pool.name
        else:
            res_pool = 'error'
    except:
        pass

    vm_obj = {}

    vm_obj.update(
        {
            instanceUuid: {
                "Datacenter": datacenter,
                "Cluster": cluster,
                "Host": host,
                "ESXVersion": esx_version,
                "ESXType": esx_type,
                "Name": name,
                "NumCpu": num_cpu,
                "MemoryGB": memory_gb,
                "CpuUsage": cpu_usage,
                "CpuDemand": cpu_demand,
                "GuestMemoryUsageGB": guest_mem_usage,
                "HostMemoryUsageGB": host_mem_usage,
                "BalloonedMemory": balloon_mem,
                "SwappedMemory": swapped_mem,
                "CompressedMemory": compressed_mem,
                "UptimeSeconds": uptime,
                "GuestId": guest_id,
                "OS": os_name,
                "VMType": vmtype,
                "ToolsStatus": tools_status,
                "ToolsVersionStatus": tools_ver_status,
                "ToolsRunningStatus": tools_run_status,
                "ToolsVersion": tools_version,
                "vHWVersion": vhw_version,
                "Datastore": vm_ds,
                "StorageUsed": storage_used_gb,
                "StorageUnused": storage_alloc_gb,
                "StorageAllocated": storage_used_gb + storage_alloc_gb,
                "Network": netwk,
                "Portgroup": portgroup,
                "Switch": switch,
                "ResourcePool": res_pool,
                "PowerState": power_state,
                "ConnectionState": connection_state
            }
        }
    )

    return vm_obj


def get_host_info(host, depth=1, max_depth=20):
    """ Get info for a particular host system """

    # if this is a group it will have children. if it does, recurse into them and then return
    if hasattr(host, 'childEntity'):
        if depth > max_depth:
            return
        vmlist = host.childEntity
        for c in vmlist:
            get_host_info(c, depth + 1)
        return

    hardware = host.hardware
    parent = host.parent
    summary = host.summary
    vm = host.vm

    datacenter = ''

    if type(parent) == vim.Datacenter:
        datacenter = parent.name
    elif type(parent.parent) == vim.Datacenter:
        datacenter = parent.parent.name
    elif type(parent.parent.parent) == vim.Datacenter:
        datacenter = parent.parent.parent.name
    elif type(parent.parent.parent.parent) == vim.Datacenter:
        datacenter = parent.parent.parent.parent.name
    elif type(parent.parent.parent.parent.parent) == vim.Datacenter:
        datacenter = parent.parent.parent.parent.parent.name
    elif type(parent.parent.parent.parent.parent.parent) == vim.Datacenter:
        datacenter = parent.parent.parent.parent.parent.parent.name
    elif type(parent.parent.parent.parent.parent.parent.parent) == vim.Datacenter:
        datacenter = parent.parent.parent.parent.parent.parent.parent.name
    elif type(parent.parent.parent.parent.parent.parent.parent.parent) == vim.Datacenter:
        datacenter = parent.parent.parent.parent.parent.parent.parent.parent.name

    try:
        uuid = summary.hardware.uuid
        cluster = summary.host.parent.name
        host = summary.host.name
        esx_version = summary.config.product.version
        esx_build = summary.config.product.build
        esx_type = summary.config.product.name
        api_version = summary.config.product.apiVersion
        vendor = summary.hardware.vendor
        model = summary.hardware.model
        cpus = summary.hardware.numCpuPkgs
        cores = summary.hardware.numCpuCores
        threads = summary.hardware.numCpuThreads
        ghz = round(summary.hardware.cpuMhz / 1000, 2)
        mhz = summary.hardware.cpuMhz
        hz = hardware.cpuInfo.hz
        cpu_type = summary.hardware.cpuModel
        cpu_usage = summary.quickStats.overallCpuUsage
        ram = summary.hardware.memorySize
        ramgb = int(((summary.hardware.memorySize / 1024) / 1024) / 1024)
        ram_usage = int(summary.quickStats.overallMemoryUsage / 1024)
        connection_state = summary.runtime.connectionState
        power_state = summary.runtime.powerState
        maint_mode = summary.runtime.inMaintenanceMode
        boot_time = str(summary.runtime.bootTime)
        overall_status = summary.overallStatus
        total_vm_count = len(vm)
    except:
        pass

    host_obj = {}

    host_obj.update(
        {
            uuid: {
                "Datacenter": datacenter,
                "Cluster": cluster,
                "Host": host,
                "ESXVersion": esx_version,
                "ESXBuild": esx_build,
                "ESXType": esx_type,
                "APIVersion": api_version,
                "Vendor": vendor,
                "Model": model,
                "CPUs": cpus,
                "Cores": cores,
                "Threads": threads,
                "Ghz": ghz,
                "Mhz": mhz,
                "Hz": hz,
                "CPUType": cpu_type,
                "CPUUsage": cpu_usage,
                "RAM": ram,
                "RAMGB": ramgb,
                "RAMUsage": ram_usage,
                "ConnectionState": connection_state,
                "PowerState": power_state,
                "MaintMode": maint_mode,
                "BootTime": boot_time,
                "OverallStatus": overall_status,
                "TotalVMCount": total_vm_count
            }
        }
    )

    return host_obj


# def get_cluster_info(cluster, depth=1, max_depth=10):
#     """ Get info for a particular datastore """

#     # if this is a group it will have children. if it does, recurse into them and then return
#     if hasattr(cluster, 'childEntity'):
#         if depth > max_depth:
#             return
#         vmlist = cluster.childEntity
#         for c in vmlist:
#             get_ds_info(c, depth + 1)
#         return

#     parent = cluster.parent
#     summary = cluster.summary
#     config = cluster.configuration
#     datastore = cluster.datastore

#     cpufrp = 0
#     memfrp = 0

#     if summary.admissionControlInfo is not None:
#         cpufrp = summary.admissionControlInfo.currentCpuFailoverResourcesPercent
#         memfrp = summary.admissionControlInfo.currentMemoryFailoverResourcesPercent
#     else:
#         cpufrp = 0
#         memfrp = 0

#     datacenter = ''

#     if type(parent) == vim.Datacenter:
#         datacenter = parent.name
#     elif type(parent.parent) == vim.Datacenter:
#         datacenter = parent.parent.name
#     elif type(parent.parent.parent) == vim.Datacenter:
#         datacenter = parent.parent.parent.name
#     elif type(parent.parent.parent.parent) == vim.Datacenter:
#         datacenter = parent.parent.parent.parent.name
#     elif type(parent.parent.parent.parent.parent) == vim.Datacenter:
#         datacenter = parent.parent.parent.parent.parent.name
#     elif type(parent.parent.parent.parent.parent.parent) == vim.Datacenter:
#         datacenter = parent.parent.parent.parent.parent.parent.name
#     elif type(parent.parent.parent.parent.parent.parent.parent) == vim.Datacenter:
#         datacenter = parent.parent.parent.parent.parent.parent.parent.name
#     elif type(parent.parent.parent.parent.parent.parent.parent.parent) == vim.Datacenter:
#         datacenter = parent.parent.parent.parent.parent.parent.parent.parent.name

#     name = cluster.name if cluster.name is not None else 'error'
#     total_cpu_ghz = round(summary.totalCpu  / 1000, 2) if summary.totalCpu is not None else 'error'
#     total_mem_gb = int(((summary.totalMemory / 1024) / 1024) / 1024) if summary.totalMemory is not None else 'error'
#     total_cores = summary.numCpuCores if summary.numCpuCores is not None else 'error'
#     total_threads = summary.numCpuThreads if summary.numCpuThreads is not None else 'error'
#     eff_cpu_ghz = round(summary.effectiveCpu / 1000, 2) if summary.effectiveCpu is not None else 'error'
#     eff_mem_gb = int(summary.effectiveMemory / 1024) if summary.effectiveMemory is not None else 'error'
#     total_hosts = summary.numHosts if summary.numHosts is not None else 'error'
#     eff_hosts = summary.numEffectiveHosts if summary.numEffectiveHosts is not None else 'error'
#     overall_status = summary.overallStatus if summary.overallStatus is not None else 'error'
#     total_cpu_use_ghz = round(summary.usageSummary.totalCpuCapacityMhz / 1000, 2) if summary.usageSummary.totalCpuCapacityMhz is not None else 'error'
#     total_mem_use_gb = int(summary.usageSummary.totalMemCapacityMB / 1024) if summary.usageSummary.totalMemCapacityMB is not None else 'error'
#     cpu_demand_ghz = round(summary.usageSummary.cpuDemandMhz / 1000, 2) if summary.usageSummary.cpuDemandMhz is not None else 'error'
#     mem_demand_gb = int(summary.usageSummary.memDemandMB / 1024) if summary.usageSummary.memDemandMB is not None else 'error'
#     total_vm_count = summary.usageSummary.totalVmCount if summary.usageSummary.totalVmCount is not None else 'error'

#     cluster_obj = {}

#     cluster_obj.update(
#         {
#             name: {
#                 "Datacenter": datacenter,
#                 "TotalCPUGhz": total_cpu_ghz,
#                 "TotalMemGB": total_mem_gb,
#                 "TotalCores": total_cores,
#                 "TotalThreads": total_threads,
#                 "EffectiveCPUGhz": eff_cpu_ghz,
#                 "EffectiveMemGB": eff_mem_gb,
#                 "TotalHosts": total_hosts,
#                 "EffectiveHosts": eff_hosts,
#                 "OverallStatus": overall_status,
#                 "CPUFailover": cpufrp,
#                 "MemFailover": memfrp,
#                 "TotalCPUUsageGhz": total_cpu_use_ghz,
#                 "TotalMemUsageGB": total_mem_use_gb,
#                 "CPUDemandGhz": cpu_demand_ghz,
#                 "MemDemandGB": mem_demand_gb,
#                 "TotalVMCount": total_vm_count
#             }
#         }
#     )

#     return cluster_obj


# def get_ds_info(ds, depth=1, max_depth=10):
#     """ Get info for a particular datastore """

#     # if this is a group it will have children. if it does, recurse into them and then return
#     if hasattr(ds, 'childEntity'):
#         if depth > max_depth:
#             return
#         vmlist = ds.childEntity
#         for c in vmlist:
#             get_ds_info(c, depth + 1)
#         return

#     parent = ds.parent
#     summary = ds.summary

#     name = summary.name if summary.name is not None else 'error'
#     datacenter = parent.parent.name if parent.parent.name is not None else 'error'
#     storage_free_gb = int(((summary.freeSpace / 1024) / 1024) / 1024) if summary.freeSpace is not None else 'error'
#     storage_cap_gb = int(((summary.capacity / 1024) / 1024) / 1024) if summary.capacity is not None else 'error'
#     ds_type = summary.type if summary.type is not None else 'error'

#     ds_obj = {}

#     ds_obj.update(
#         {
#             name: {
#                 "Datacenter": datacenter,
#                 "CapacityGB": storage_cap_gb,
#                 "FreeSpaceGB": storage_free_gb,
#                 "Type": ds_type
#             }
#         }
#     )

#     return ds_obj


# def get_net_info(net, depth=1, max_depth=10):
#     """ Get info for a particular distributed switch """

#     # if this is a group it will have children. if it does, recurse into them and then return
#     if hasattr(net, 'childEntity'):
#         if depth > max_depth:
#             return
#         vmlist = net.childEntity
#         for c in vmlist:
#             get_net_info(c, depth + 1)
#         return

#     config = net.config
#     parent = net.parent
#     runtime = net.runtime
#     summary = net.summary

#     name = summary.name if summary.name is not None else 'error'
#     uuid = summary.uuid if summary.uuid is not None else 'error'

#     net_obj = {}

#     net_obj.update(
#         {
#             name: {
#                 "vDSUUID": uuid,
#             }
#         }
#     )

#     return net_obj


# def get_pg_info(pg, depth=1, max_depth=10):
#     """ Get info for a particular vds portgroup """

#     # if this is a group it will have children. if it does, recurse into them and then return
#     if hasattr(pg, 'childEntity'):
#         if depth > max_depth:
#             return
#         vmlist = pg.childEntity
#         for c in vmlist:
#             get_net_info(c, depth + 1)
#         return

#     config = pg.config
#     parent = pg.parent
#     summary = pg.summary

#     name = summary.name if summary.name is not None else 'error'
#     vds = config.distributedVirtualSwitch.name if config.distributedVirtualSwitch.name is not None else 'error'

#     pg_obj = {}

#     pg_obj.update(
#         {
#             name: {
#                 "vDS": vds,
#             }
#         }
#     )

#     return pg_obj
