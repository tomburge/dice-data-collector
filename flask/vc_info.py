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
    parent = vm.parent
    summary = vm.summary

    storage_used_gb = int(((summary.storage.committed / 1024) / 1024) / 1024)
    storage_alloc_gb = int(((summary.storage.uncommitted / 1024) / 1024) / 1024)
    vmtype = 'server'

    for i in config.extraConfig:
        if i.key == 'machine.id':
            vmtype = 'vdi'

    instanceUuid = summary.config.instanceUuid if summary.config.instanceUuid is not None else 'error'
    datacenter = parent.parent.name if parent.parent.name is not None else 'error'
    host = summary.runtime.host.name if summary.runtime.host.name is not None else 'error'
    esx_version = summary.runtime.host.summary.config.product.version if summary.runtime.host.summary.config.product.version is not None else 'error'
    esx_type = summary.runtime.host.summary.config.product.name if summary.runtime.host.summary.config.product.name is not None else 'error'
    name = summary.vm.name if summary.vm.name is not None else 'error'
    num_cpu = summary.config.numCpu if summary.config.numCpu is not None else 'error'
    memory_mb = summary.config.memorySizeMB if summary.config.memorySizeMB is not None else 'error'
    cpu_usage = summary.quickStats.overallCpuUsage if summary.quickStats.overallCpuUsage is not None else 'error'
    cpu_demand = summary.quickStats.overallCpuDemand if summary.quickStats.overallCpuDemand is not None else 'error'
    guest_mem_usage = summary.quickStats.guestMemoryUsage if summary.quickStats.guestMemoryUsage is not None else 'error'
    host_mem_usage = summary.quickStats.hostMemoryUsage if summary.quickStats.hostMemoryUsage is not None else 'error'
    balloon_mem = summary.quickStats.balloonedMemory if summary.quickStats.balloonedMemory is not None else 'error'
    swapped_mem = summary.quickStats.swappedMemory if summary.quickStats.swappedMemory is not None else 'error'
    compressed_mem = summary.quickStats.compressedMemory if summary.quickStats.compressedMemory is not None else 'error'
    uptime = summary.quickStats.uptimeSeconds if summary.quickStats.uptimeSeconds is not None else 'error'
    guest_id = summary.guest.guestId if summary.guest.guestId is not None else 'error'
    os_name = summary.guest.guestFullName if summary.guest.guestFullName is not None else 'error'
    tools_status = summary.guest.toolsStatus if summary.guest.toolsStatus is not None else 'error'
    tools_ver_status = summary.guest.toolsVersionStatus if summary.guest.toolsVersionStatus is not None else 'error'
    tools_run_status = summary.guest.toolsRunningStatus if summary.guest.toolsRunningStatus is not None else 'error'
    tools_version = config.tools.toolsVersion if config.tools.toolsVersion is not None else 'error'
    vhw_version = config.version if config.version is not None else 'error'
    vm_ds = config.datastoreUrl[0].name if config.datastoreUrl[0].name is not None else 'error'
    power_state = summary.runtime.powerState if summary.runtime.powerState is not None else 'error'
    connection_state = summary.runtime.connectionState if summary.runtime.connectionState is not None else 'error'

    vm_obj = {}

    vm_obj.update(
        {
            instanceUuid: {
                "Datacenter": parent.parent.name,
                "Cluster": datacenter,
                "Host": host,
                "ESXVersion": esx_version,
                "ESXType": esx_type,
                "Name": name,
                "NumCpu": num_cpu,
                "MemoryMB": memory_mb,
                "CpuUsage": cpu_usage,
                "CpuDemand": cpu_demand,
                "GuestMemoryUsage": guest_mem_usage,
                "HostMemoryUsage": host_mem_usage,
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

    uuid = summary.hardware.uuid if summary.hardware.uuid is not None else 'error'
    datacenter = parent.parent.name if parent.parent.name is not None else 'error'
    cluster = summary.host.parent.name if summary.host.parent.name is not None else 'error'
    host = summary.host.name if summary.host.name is not None else 'error'
    esx_version = summary.config.product.version if summary.config.product.version is not None else 'error'
    esx_build = summary.config.product.build if summary.config.product.build is not None else 'error'
    esx_type = summary.config.product.name if summary.config.product.name is not None else 'error'
    api_version = summary.config.product.apiVersion if summary.config.product.apiVersion is not None else 'error'
    vendor = summary.hardware.vendor if summary.hardware.vendor is not None else 'error'
    model = summary.hardware.model if summary.hardware.model is not None else 'error'
    cpus = summary.hardware.numCpuPkgs if summary.hardware.numCpuPkgs is not None else 'error'
    cores = summary.hardware.numCpuCores if summary.hardware.numCpuCores is not None else 'error'
    threads = summary.hardware.numCpuThreads if summary.hardware.numCpuThreads is not None else 'error'
    ghz = round(summary.hardware.cpuMhz / 1000, 2) if summary.hardware.cpuMhz is not None else 'error'
    mhz = summary.hardware.cpuMhz if summary.hardware.cpuMhz is not None else 'error'
    hz = hardware.cpuInfo.hz if hardware.cpuInfo.hz is not None else 'error'
    cpu_type = summary.hardware.cpuModel if summary.hardware.cpuModel is not None else 'error'
    cpu_usage = summary.quickStats.overallCpuUsage if summary.quickStats.overallCpuUsage is not None else 'error'
    ram = summary.hardware.memorySize if summary.hardware.memorySize is not None else 'error'
    ramgb = int(((summary.hardware.memorySize / 1024) / 1024) / 1024) if summary.hardware.memorySize is not None else 'error' 
    ram_usage = summary.quickStats.overallMemoryUsage if summary.quickStats.overallMemoryUsage is not None else 'error'
    connection_state = summary.runtime.connectionState if summary.runtime.connectionState is not None else 'error'
    power_state = summary.runtime.powerState if summary.runtime.powerState is not None else 'error'
    maint_mode = summary.runtime.inMaintenanceMode if summary.runtime.inMaintenanceMode is not None else 'error'
    boot_time = str(summary.runtime.bootTime) if summary.runtime.bootTime is not None else 'error'
    overall_status = summary.overallStatus if summary.overallStatus is not None else 'error'

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
            }
        }
    )

    return host_obj


def get_cluster_info(cluster, depth=1, max_depth=10):
    """ Get info for a particular datastore """

    # if this is a group it will have children. if it does, recurse into them and then return
    if hasattr(cluster, 'childEntity'):
        if depth > max_depth:
            return
        vmlist = cluster.childEntity
        for c in vmlist:
            get_ds_info(c, depth + 1)
        return

    parent = cluster.parent
    summary = cluster.summary
    config = cluster.configuration
    datastore = cluster.datastore

    cpufrp = 0
    memfrp = 0

    if summary.admissionControlInfo is not None:
        cpufrp = summary.admissionControlInfo.currentCpuFailoverResourcesPercent
        memfrp = summary.admissionControlInfo.currentMemoryFailoverResourcesPercent
    else:
        cpufrp = 0
        memfrp = 0

    name = cluster.name if cluster.name is not None else 'error'
    total_cpu = summary.totalCpu if summary.totalCpu is not None else 'error'
    total_mem = summary.totalMemory if summary.totalMemory is not None else 'error'
    total_cores = summary.numCpuCores if summary.numCpuCores is not None else 'error'
    total_threads = summary.numCpuThreads if summary.numCpuThreads is not None else 'error'
    eff_cpu = summary.effectiveCpu if summary.effectiveCpu is not None else 'error'
    eff_mem = summary.effectiveMemory if summary.effectiveMemory is not None else 'error'
    total_hosts = summary.numHosts if summary.numHosts is not None else 'error'
    eff_hosts = summary.numEffectiveHosts if summary.numEffectiveHosts is not None else 'error'
    overall_status = summary.overallStatus if summary.overallStatus is not None else 'error'
    total_cpu_mhz = summary.usageSummary.totalCpuCapacityMhz if summary.usageSummary.totalCpuCapacityMhz is not None else 'error'
    total_mem_mb = summary.usageSummary.totalMemCapacityMB if summary.usageSummary.totalMemCapacityMB is not None else 'error'
    cpu_demand = summary.usageSummary.cpuDemandMhz if summary.usageSummary.cpuDemandMhz is not None else 'error'
    mem_demand = summary.usageSummary.memDemandMB if summary.usageSummary.memDemandMB is not None else 'error'
    total_vm_count = summary.usageSummary.totalVmCount if summary.usageSummary.totalVmCount is not None else 'error'

    cluster_obj = {}

    cluster_obj.update(
        {
            name: {
                "TotalCPU": total_cpu,
                "TotalMem": total_mem,
                "TotalCores": total_cores,
                "TotalThreads": total_threads,
                "EffectiveCPU": eff_cpu,
                "EffectiveMem": eff_mem,
                "TotalHosts": total_hosts,
                "EffectiveHosts": eff_hosts,
                "OverallStatus": overall_status,
                "CPUFailover": cpufrp,
                "MemFailover": memfrp,
                "TotalCPUMhz": total_cpu_mhz,
                "TotalMemMB": total_mem_mb,
                "CPUDemand": cpu_demand,
                "MemDemand": mem_demand,
                "TotalVMCount": total_vm_count
            }           
        }
    )

    return cluster_obj


def get_ds_info(ds, depth=1, max_depth=10):
    """ Get info for a particular datastore """

    # if this is a group it will have children. if it does, recurse into them and then return
    if hasattr(ds, 'childEntity'):
        if depth > max_depth:
            return
        vmlist = ds.childEntity
        for c in vmlist:
            get_ds_info(c, depth + 1)
        return

    parent = ds.parent
    summary = ds.summary

    name = summary.name if summary.name is not None else 'error'
    datacenter = parent.parent.name if parent.parent.name is not None else 'error'
    storage_free_gb = int(((summary.freeSpace / 1024) / 1024) / 1024) if summary.freeSpace is not None else 'error'
    storage_cap_gb = int(((summary.capacity / 1024) / 1024) / 1024) if summary.capacity is not None else 'error'
    ds_type = summary.type if summary.type is not None else 'error'

    ds_obj = {}

    ds_obj.update(
        {
            name: {
                "Datacenter": datacenter,
                "Capacity": storage_cap_gb,
                "FreeSpace": storage_free_gb,
                "Type": ds_type
            }           
        }
    )

    return ds_obj


def get_net_info(net, depth=1, max_depth=10):
    """ Get info for a particular distributed switch """

    # if this is a group it will have children. if it does, recurse into them and then return
    if hasattr(net, 'childEntity'):
        if depth > max_depth:
            return
        vmlist = net.childEntity
        for c in vmlist:
            get_net_info(c, depth + 1)
        return

    config = net.config
    parent = net.parent
    runtime = net.runtime
    summary = net.summary

    name = summary.name if summary.name is not None else 'error'
    uuid = summary.uuid if summary.uuid is not None else 'error'

    net_obj = {}

    net_obj.update(
        {
            name: {
                "vDSUUID": uuid,
            }           
        }
    )

    return net_obj


def get_pg_info(pg, depth=1, max_depth=10):
    """ Get info for a particular vds portgroup """

    # if this is a group it will have children. if it does, recurse into them and then return
    if hasattr(pg, 'childEntity'):
        if depth > max_depth:
            return
        vmlist = pg.childEntity
        for c in vmlist:
            get_net_info(c, depth + 1)
        return

    config = pg.config
    parent = pg.parent
    summary = pg.summary

    name = summary.name if summary.name is not None else 'error'
    vds = config.distributedVirtualSwitch.name if config.distributedVirtualSwitch.name is not None else 'error'

    pg_obj = {}

    pg_obj.update(
        {
            name: {
                "vDS": vds,
            }           
        }
    )

    return pg_obj