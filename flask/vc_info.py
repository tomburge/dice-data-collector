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

    vm_ds = ''

    if config.datastoreUrl:
        vm_ds = config.datastoreUrl[0].name
    else:
        vm_ds = 'error'


    vm_obj = {}

    vm_obj.update(
        {
            summary.config.instanceUuid: {
                "Datacenter": parent.parent.name,
                "Cluster": summary.runtime.host.parent.name,
                "Host": summary.runtime.host.name,
                "ESXVersion": summary.runtime.host.summary.config.product.version,
                "ESXType": summary.runtime.host.summary.config.product.name,
                "Name": summary.vm.name,
                "NumCpu": summary.config.numCpu,
                "MemoryMB": summary.config.memorySizeMB,
                "CpuUsage": summary.quickStats.overallCpuUsage,
                "CpuDemand": summary.quickStats.overallCpuDemand,
                "GuestMemoryUsage": summary.quickStats.guestMemoryUsage,
                "HostMemoryUsage": summary.quickStats.hostMemoryUsage,
                "BalloonedMemory": summary.quickStats.balloonedMemory,
                "SwappedMemory": summary.quickStats.swappedMemory,
                "CompressedMemory": summary.quickStats.compressedMemory,
                "UptimeSeconds": summary.quickStats.uptimeSeconds,
                "GuestId": summary.guest.guestId,
                "OS": summary.guest.guestFullName,
                "VMType": vmtype,
                "ToolsStatus": summary.guest.toolsStatus,
                "ToolsVersionStatus": summary.guest.toolsVersionStatus,
                "ToolsRunningStatus": summary.guest.toolsRunningStatus,
                "ToolsVersion": config.tools.toolsVersion,
                "vHWVersion": config.version,
                "Datastore": vm_ds,
                "StorageUsed": storage_used_gb,
                "StorageUnused": storage_alloc_gb,
                "StorageAllocated": storage_used_gb + storage_alloc_gb,
                "PowerState": summary.runtime.powerState,
                "ConnectionState": summary.runtime.connectionState
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

    ghz = round(summary.hardware.cpuMhz / 1000, 2)
    ramgb = int(((summary.hardware.memorySize / 1024) / 1024) / 1024)

    host_obj = {}

    host_obj.update(
        {
            summary.hardware.uuid: {
                "Datacenter": parent.parent.name,
                "Cluster": summary.host.parent.name,
                "Host": summary.host.name,
                "ESXVersion": summary.config.product.version,
                "ESXBuild": summary.config.product.build,
                "ESXType": summary.config.product.name,
                "APIVersion": summary.config.product.apiVersion,
                "Vendor": summary.hardware.vendor,
                "Model": summary.hardware.model,
                "CPUs": summary.hardware.numCpuPkgs,
                "Cores": summary.hardware.numCpuCores,
                "Threads": summary.hardware.numCpuThreads,
                "Ghz": ghz,
                "Mhz": summary.hardware.cpuMhz,
                "Hz": hardware.cpuInfo.hz,
                "CPUType": summary.hardware.cpuModel,
                "CPUUsage": summary.quickStats.overallCpuUsage,
                "RAM": summary.hardware.memorySize,
                "RAMGB": ramgb,
                "RAMUsage": summary.quickStats.overallMemoryUsage,
                "ConnectionState": summary.runtime.connectionState,
                "PowerState": summary.runtime.powerState,
                "MaintMode": summary.runtime.inMaintenanceMode,
                "BootTime": str(summary.runtime.bootTime),
                "OverallStatus": summary.overallStatus,
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

    name = cluster.name
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

    cluster_obj = {}

    cluster_obj.update(
        {
            name: {
                "TotalCPU": summary.totalCpu,
                "TotalMem": summary.totalMemory,
                "TotalCores": summary.numCpuCores,
                "TotalThreads": summary.numCpuThreads,
                "EffectiveCPU": summary.effectiveCpu,
                "EffectiveMem": summary.effectiveMemory,
                "TotalHosts": summary.numHosts,
                "EffectiveHosts": summary.numEffectiveHosts,
                "OverallStatus": summary.overallStatus,
                "CPUFailover": cpufrp,
                "MemFailover": memfrp,
                "TotalCPUMhz": summary.usageSummary.totalCpuCapacityMhz,
                "TotalMemMB": summary.usageSummary.totalMemCapacityMB,
                "CPUDemand": summary.usageSummary.cpuDemandMhz,
                "MemDemand": summary.usageSummary.memDemandMB,
                "TotalVMCount": summary.usageSummary.totalVmCount
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

    ds_obj = {}

    ds_obj.update(
        {
            summary.name: {
                "Datacenter": parent.parent.name,
                "Capacity": summary.capacity,
                "FreeSpace": summary.freeSpace,
                "Type": summary.type
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

    net_obj = {}

    net_obj.update(
        {
            summary.name: {
                "vDSUUID": summary.uuid,
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

    pg_obj = {}

    pg_obj.update(
        {
            summary.name: {
                "vDS": config.distributedVirtualSwitch.name,
            }           
        }
    )

    return pg_obj