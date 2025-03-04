import base64
import os

MOCK_HOST = "f01-h01-000-r630.host.io"
MOCK_USER = "mock_user"
MOCK_PASS = "mock_pass"
JOB_ID = "JID_498218641680"
BAD_DEVICE_NAME = "BadIF.Slot.x-y-z"
DEVICE_NIC_I = "NIC.Integrated.1"
DEVICE_NIC_S = "NIC.Slot.1"
MAC_ADDRESS = "40:A6:B7:0C:01:A0"


def render_device_dict(index, device):
    device_dict = {
        "Index": index,
        "Enabled": "True",
        "Id": "BIOS.Setup.1-1#BootSeq#{name}#{hash}".format(**device),
        "Name": device["name"],
    }
    return device_dict


DEVICE_HDD_1 = {"name": "HardDisk.List.1-1", "hash": "c9203080df84781e2ca3d512883dee6f"}
DEVICE_NIC_1 = {
    "name": "NIC.Integrated.1-2-1",
    "hash": "bfa8fe2210d216298c7c53aedfc7e21b",
}
DEVICE_NIC_2 = {"name": "NIC.Slot.2-1-1", "hash": "135ac45c488549c04a21f1c199c2044a"}

BOOT_SEQ_RESPONSE_DIRECTOR = [
    render_device_dict(0, DEVICE_NIC_1),
    render_device_dict(1, DEVICE_HDD_1),
    render_device_dict(2, DEVICE_NIC_2),
]
BOOT_SEQ_RESPONSE_FOREMAN = [
    render_device_dict(0, DEVICE_NIC_2),
    render_device_dict(1, DEVICE_HDD_1),
    render_device_dict(2, DEVICE_NIC_1),
]
BOOT_SEQ_RESPONSE_NO_MATCH = [
    render_device_dict(0, DEVICE_HDD_1),
    render_device_dict(1, DEVICE_NIC_1),
    render_device_dict(2, DEVICE_NIC_2),
]

RESPONSE_WITHOUT = (
    "- INFO     - Current boot order:\n"
    "- INFO     - 1: NIC.Integrated.1-2-1\n"
    "- INFO     - 2: HardDisk.List.1-1\n"
    "- INFO     - 3: NIC.Slot.2-1-1\n"
)
RESPONSE_NO_MATCH = (
    "- INFO     - Current boot order:\n"
    "- INFO     - 1: HardDisk.List.1-1\n"
    "- INFO     - 2: NIC.Integrated.1-2-1\n"
    "- INFO     - 3: NIC.Slot.2-1-1\n"
)
WARN_NO_MATCH = (
    "- WARNING  - Current boot order does not match any of the given.\n%s"
    % RESPONSE_NO_MATCH
)
RESPONSE_DIRECTOR = "- WARNING  - Current boot order is set to: director.\n"

RESPONSE_FOREMAN = "- WARNING  - Current boot order is set to: foreman.\n"
INTERFACES_PATH = os.path.join(
    os.path.dirname(__file__), "../config/idrac_interfaces.yml"
)

# test_boot_to constants
ERROR_DEV_NO_MATCH = (
    "- ERROR    - Device %s does not match any of the available boot devices for host %s\n"
    % (BAD_DEVICE_NAME, MOCK_HOST)
)
TOGGLE_DEV_OK = (
    "- INFO     - %s has now been disabled\n"
    "- INFO     - Command passed to ForceOff server, code return is 200.\n"
    "- INFO     - Polling for host state: Not Down\n"
    "- INFO     - Command passed to On server, code return is 200.\n"
    % DEVICE_NIC_2["name"]
)
TOGGLE_DEV_NO_MATCH = (
    "- WARNING  - Accepted device names:\n"
    "- WARNING  - NIC.Integrated.1-2-1\n"
    "- WARNING  - HardDisk.List.1-1\n"
    "- WARNING  - NIC.Slot.2-1-1\n"
    "- ERROR    - Boot device name not found\n"
)
RESPONSE_BOOT_TO = (
    f"- WARNING  - Job queue already cleared for iDRAC {MOCK_HOST}, DELETE command will not execute.\n"
    "- INFO     - Command passed to set BIOS attribute pending values.\n"
)
RESPONSE_BOOT_TO_BAD_TYPE = (
    "- ERROR    - Expected values for -t argument are: ['director', 'foreman']\n"
)
RESPONSE_BOOT_TO_BAD_FILE = "- ERROR    - No such file or directory: bad/bad/file.\n"
RESPONSE_BOOT_TO_NO_FILE = "- ERROR    - You must provide a path to the interfaces yaml via `-i` optional argument.\n"
RESPONSE_BOOT_TO_BAD_MAC = (
    "- ERROR    - MAC Address does not match any of the existing\n"
)

# test_reboot_only
RESPONSE_REBOOT_ONLY_SUCCESS = (
    "- INFO     - Command passed to GracefulRestart server, code return is 204.\n"
    "- INFO     - Polling for host state: Not Down\n"
    "- INFO     - Command passed to On server, code return is 204.\n"
)

# test_power
RESPONSE_POWER_ON_OK = "- INFO     - Command passed to On server, code return is 204.\n"
RESPONSE_POWER_OFF_OK = (
    "- INFO     - Command passed to ForceOff server, code return is 204.\n"
)
RESPONSE_POWER_OFF_NO_STATE = "- ERROR    - Couldn't get power state.\n"
RESPONSE_POWER_OFF_ALREADY = "- WARNING  - Command failed to ForceOff server, host appears to be already in that state.\n"
RESPONSE_POWER_OFF_MISS_STATE = "- ERROR    - Power state not found. Try to racreset.\n"
RESPONSE_POWER_ON_NOT = "- WARNING  - Command failed to On server, host appears to be already in that state.\n"

# test_reset_%s
RESPONSE_RESET = (
    "- INFO     - Status code 204 returned for POST command to reset %s.\n"
    "- INFO     - %s will now reset and be back online within a few minutes.\n"
)
RESPONSE_RESET_FAIL = "- ERROR    - Status code 400 returned, error is: \nnot_ok.\n"

# test_change_boot
RESPONSE_CHANGE_BOOT = (
    f"- WARNING  - Job queue already cleared for iDRAC {MOCK_HOST}, DELETE command will not "
    "execute.\n"
    "- INFO     - Command passed to ForceOff server, code return is 200.\n"
    "- INFO     - Polling for host state: Not Down\n"
    "- INFO     - Command passed to On server, code return is 200.\n"
)
RESPONSE_CHANGE_BAD_TYPE = (
    "- ERROR    - Expected values for -t argument are: ['director', 'foreman']\n"
)
RESPONSE_CHANGE_TO_SAME = "- WARNING  - No changes were made since the boot order already matches the requested.\n"
RESPONSE_CHANGE_NO_INT = "- ERROR    - You must provide a path to the interfaces yaml via `-i` optional argument.\n"

ROOT_RESP = '{"Managers":{"@odata.id":"/redfish/v1/Managers"},"Systems":{"@odata.id":"/redfish/v1/Systems"}}'
SYS_RESP = '{"Members":[{"@odata.id":"/redfish/v1/Systems/System.Embedded.1"}]}'
MAN_RESP = '{"Members":[{"@odata.id":"/redfish/v1/Managers/iDRAC.Embedded.1"}]}'
RESET_TYPE_RESP = (
    '{"Actions":{"#Manager.Reset":{"ResetType@Redfish.AllowableValues":["GracefulRestart"],'
    '"target":"/redfish/v1/Managers/iDRAC.Embedded.1/Actions/Manager.Reset"}}} '
)
INIT_RESP = [ROOT_RESP, SYS_RESP, ROOT_RESP, MAN_RESP]

STATE_OFF_RESP = '{"PowerState": "Off"}'
STATE_ON_RESP = '{"PowerState": "On"}'

BOOT_MODE_RESP = '{"Attributes": {"BootMode": "Bios"}}'
BOOT_SEQ_RESP = '{"Attributes": {"BootSeq": %s}}'

ETHERNET_INTERFACES_RESP = (
    '{"Members":['
    '{"@odata.id":"/redfish/v1/Systems/System.Embedded.1/EthernetInterfaces/NIC.Slot.1-1-1"},'
    '{"@odata.id":"/redfish/v1/Systems/System.Embedded.1/EthernetInterfaces/NIC.Integrated.1-1-1"}'
    "]}"
)


NETWORK_ADAPTERS_RESP = (
    '{"Members": ['
    f'{{"@odata.id": "/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/{DEVICE_NIC_I}"}},'
    f'{{"@odata.id": "/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/{DEVICE_NIC_S}"}}'
    "]}"
)
NETWORK_PORTS_ROOT_RESP = (
    '{"Members": ['
    '{"@odata.id": "/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/%s/NetworkPorts/%s-1"} '
    "]}"
)
NETWORK_DEV_FUNC_RESP = (
    '{"Members": ['
    '{"@odata.id": "/redfish/v1/Chassis/System.Embedded.1/NetworkAdapters/%s/NetworkDeviceFunctions/%s-1"}'
    "]}"
)
NETWORK_DEV_FUNC_DET_RESP = (
    '{"Ethernet": {"MACAddress": "B0:26:28:D8:68:C0"},'
    '"Oem": {"Dell": {"DellNIC": {"VendorName": "Intel"}}}}'
)
NETWORK_PORTS_RESP = '{"Id": "%s-1", "LinkStatus": "Down", "SupportedLinkCapabilities": [{"LinkSpeedMbps": 1000}]}'
RESPONSE_LS_INTERFACES = (
    "- INFO     - NIC.Integrated.1-1:\n"
    "- INFO     -     Id: NIC.Integrated.1-1\n"
    "- INFO     -     LinkStatus: Down\n"
    "- INFO     -     LinkSpeedMbps: 1000\n"
    "- INFO     -     MACAddress: B0:26:28:D8:68:C0\n"
    "- INFO     -     Vendor: Intel\n"
    "- INFO     - NIC.Slot.1-1:\n"
    "- INFO     -     Id: NIC.Slot.1-1\n"
    "- INFO     -     LinkStatus: Down\n"
    "- INFO     -     LinkSpeedMbps: 1000\n"
    "- INFO     -     MACAddress: B0:26:28:D8:68:C0\n"
    "- INFO     -     Vendor: Intel\n"
)

INTERFACES_RESP = f'{{"Id":"NIC.Integrated.1-2-1","MACAddress":"{MAC_ADDRESS}"}}'

RESPONSE_LS_JOBS = "- INFO     - Found active jobs:\n" f"- INFO     - {JOB_ID}\n"
RESPONSE_LS_JOBS_EMPTY = "- INFO     - No active jobs found.\n"
RESPONSE_CLEAR_JOBS = (
    f"- INFO     - Job queue for iDRAC {MOCK_HOST} successfully cleared.\n"
)
DELLJOBSERVICE_UNSUPPORTED = (
    "- WARNING  - iDRAC version installed does not support DellJobService\n"
)
RESPONSE_CLEAR_JOBS_UNSUPPORTED = f"{DELLJOBSERVICE_UNSUPPORTED}{RESPONSE_CLEAR_JOBS}"
RESPONSE_CLEAR_JOBS_LIST = f"{DELLJOBSERVICE_UNSUPPORTED}- WARNING  - Clearing job queue for job IDs: ['{JOB_ID}'].\n{RESPONSE_CLEAR_JOBS}"

FIRMWARE_INVENTORY_RESP = (
    '{"Members": ['
    '{"@odata.id": "/redfish/v1/UpdateService/FirmwareInventory/Installed-0-16.25.40.62"},'
    '{"@odata.id": "/redfish/v1/UpdateService/FirmwareInventory/Installed-0-19.5.12"}'
    "]} "
)
FIRMWARE_INVENTORY_1_RESP = (
    "{"
    '"Id": "Installed-0-16.25.40.62",'
    '"Name": "Mellanox ConnectX-5",'
    '"ReleaseDate": "00:00:00Z",'
    '"SoftwareId": "0",'
    '"Status": {"Health": "OK","State": "Enabled"},'
    '"Updateable": "True",'
    '"Version": "16.25.40.62"}'
)
FIRMWARE_INVENTORY_2_RESP = (
    "{"
    '"Id": "Installed-0-19.5.12",'
    '"Name": "Intel(R) Ethernet Network Adapter",'
    '"ReleaseDate": "00:00:00Z",'
    '"SoftwareId": "0",'
    '"Status": {"Health": "OK","State": "Enabled"},'
    '"Updateable": "True",'
    '"Version": "19.5.12"}'
)
RESPONSE_FIRMWARE_INVENTORY = (
    "- INFO     - Id: Installed-0-16.25.40.62\n"
    "- INFO     - Name: Mellanox ConnectX-5\n"
    "- INFO     - ReleaseDate: 00:00:00Z\n"
    "- INFO     - SoftwareId: 0\n"
    "- INFO     - Status: {'Health': 'OK', 'State': 'Enabled'}\n"
    "- INFO     - Updateable: True\n"
    "- INFO     - Version: 16.25.40.62\n"
    "- INFO     - ************************************************\n"
    "- INFO     - Id: Installed-0-19.5.12\n"
    "- INFO     - Name: Intel(R) Ethernet Network Adapter\n"
    "- INFO     - ReleaseDate: 00:00:00Z\n"
    "- INFO     - SoftwareId: 0\n"
    "- INFO     - Status: {'Health': 'OK', 'State': 'Enabled'}\n"
    "- INFO     - Updateable: True\n"
    "- INFO     - Version: 19.5.12\n"
    "- INFO     - ************************************************\n"
)

MEMORY_MEMBERS_RESP = (
    '{"Members": ['
    '{"@odata.id": "/redfish/v1/Systems/System.Embedded.1/Memory/DIMM.Socket.A5"},'
    '{"@odata.id": "/redfish/v1/Systems/System.Embedded.1/Memory/DIMM.Socket.B2"}]}'
)
MEMORY_SUMMARY_RESP = (
    '{"MemorySummary": {'
    '"MemoryMirroring": "System",'
    '"Status": {"Health": "Unknown","HealthRollup": "Unknown","State": "Enabled"},'
    '"TotalSystemMemoryGiB": 384}}'
)
MEMORY_A5_RESP = (
    '{"CapacityMiB": 32768,'
    '"Description": "DIMM A5",'
    '"Manufacturer": "Hynix Semiconductor",'
    '"MemoryDeviceType": "DDR4",'
    '"Name": "DIMM A5",'
    '"OperatingSpeedMhz": 2933}'
)
MEMORY_B2_RESP = (
    '{"CapacityMiB": 32768,'
    '"Description": "DIMM B2",'
    '"Manufacturer": "Hynix Semiconductor",'
    '"MemoryDeviceType": "DDR4",'
    '"Name": "DIMM B2",'
    '"OperatingSpeedMhz": 2933}'
)
RESPONSE_LS_MEMORY = (
    "- INFO     - Memory Summary:\n"
    "- INFO     -     MemoryMirroring: System\n"
    "- INFO     -     TotalSystemMemoryGiB: 384\n"
    "- INFO     - DIMM A5:\n"
    "- INFO     -     CapacityMiB: 32768\n"
    "- INFO     -     Description: DIMM A5\n"
    "- INFO     -     Manufacturer: Hynix Semiconductor\n"
    "- INFO     -     MemoryDeviceType: DDR4\n"
    "- INFO     -     OperatingSpeedMhz: 2933\n"
    "- INFO     - DIMM B2:\n"
    "- INFO     -     CapacityMiB: 32768\n"
    "- INFO     -     Description: DIMM B2\n"
    "- INFO     -     Manufacturer: Hynix Semiconductor\n"
    "- INFO     -     MemoryDeviceType: DDR4\n"
    "- INFO     -     OperatingSpeedMhz: 2933\n"
)

PROCESSOR_SUMMARY_RESP = (
    '{"ProcessorSummary": {'
    '"Count": 2,'
    '"LogicalProcessorCount": 80,'
    '"Model": "Intel(R) Xeon(R) Gold 6230 CPU @ 2.10GHz",'
    '"Status": {"Health": "Unknown","HealthRollup": "Unknown","State": "Enabled"}}}'
)
PROCESSOR_MEMBERS_RESP = (
    '{"Members": ['
    '{"@odata.id": "/redfish/v1/Systems/System.Embedded.1/Processors/CPU.Socket.1"},'
    '{"@odata.id": "/redfish/v1/Systems/System.Embedded.1/Processors/CPU.Socket.2"}]}'
)
PROCESSOR_CPU_RESP = (
    '{"InstructionSet": "x86-64",'
    '"Id": "CPU.Socket.%s",'
    '"Manufacturer": "Intel",'
    '"MaxSpeedMHz": 4000,'
    '"Model": "Intel(R) Xeon(R) Gold 6230 CPU @ 2.10GHz",'
    '"Name": "CPU %s",'
    '"TotalCores": 20,'
    '"TotalThreads": 40}'
)
RESPONSE_LS_PROCESSORS = (
    "- INFO     - Processor Summary:\n"
    "- INFO     -     Count: 2\n"
    "- INFO     -     LogicalProcessorCount: 80\n"
    "- INFO     -     Model: Intel(R) Xeon(R) Gold 6230 CPU @ 2.10GHz\n"
    "- INFO     - CPU.Socket.1:\n"
    "- INFO     -     Name: CPU 1\n"
    "- INFO     -     InstructionSet: x86-64\n"
    "- INFO     -     Manufacturer: Intel\n"
    "- INFO     -     MaxSpeedMHz: 4000\n"
    "- INFO     -     Model: Intel(R) Xeon(R) Gold 6230 CPU @ 2.10GHz\n"
    "- INFO     -     TotalCores: 20\n"
    "- INFO     -     TotalThreads: 40\n"
    "- INFO     - CPU.Socket.2:\n"
    "- INFO     -     Name: CPU 2\n"
    "- INFO     -     InstructionSet: x86-64\n"
    "- INFO     -     Manufacturer: Intel\n"
    "- INFO     -     MaxSpeedMHz: 4000\n"
    "- INFO     -     Model: Intel(R) Xeon(R) Gold 6230 CPU @ 2.10GHz\n"
    "- INFO     -     TotalCores: 20\n"
    "- INFO     -     TotalThreads: 40\n"
)

BLANK_RESP = '"OK"'
TASK_OK_RESP = (
    '{"Message": "Job completed successfully.","Id": "%s","Name": "Task","PercentComplete": "100"}'
    % JOB_ID
)
JOB_OK_RESP = '{"JobID": "%s"}' % JOB_ID
SCREENSHOT_64 = base64.b64encode(bytes("ultimate_screenshot", "utf-8"))
SCREENSHOT_RESP = '{"ServerScreenShotFile": "%s"}' % str(SCREENSHOT_64)
SCREENSHOT_NAME = "screenshot_now.png"

VMEDIA_GET_VM_RESP = '{"VirtualMedia": {"@odata.id": "/redfish/v1/Managers/1/VM1"}}'
VMEDIA_GET_MEMBERS_RESP = """
{"Members": [
    {"@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/VirtualMedia/RemovableDisk"},
    {"@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1/VirtualMedia/CD"}
  ]
}
"""
VMEDIA_MEMBER_RM_DISK_RESP = """
{
  "Id":"RemovableDisk",
  "ImageName":null,
  "Inserted":false,
  "Name":"Virtual Removable Disk"
}
"""
VMEDIA_MEMBER_CD_RESP = """
{
  "Id":"CD",
  "ImageName":"TestImage",
  "Inserted":true,
  "Name":"Virtual CD"
}
"""
VMEDIA_CHECK_GOOD = """\
- INFO     - ID: RemovableDisk - Name: Virtual Removable Disk - ImageName: None - Inserted: False
- INFO     - ID: CD - Name: Virtual CD - ImageName: TestImage - Inserted: True\n\
"""
VMEDIA_CHECK_EMPTY = """\
- WARNING  - No active VirtualMedia found\n\
"""
VMEDIA_GET_CONF_RESP = """
{"Oem":{
    "Supermicro":{
      "@odata.type": "#SmcVirtualMediaExtensions.v1_0_0.VirtualMediaCollection",
      "VirtualMediaConfig": {"@odata.id": "/redfish/v1/Managers/1/VM1/CfgCD"}
    }
  }
}
"""
VMEDIA_UNMOUNT_OK = "- INFO     - Successfully unmounted all VirtualMedia\n"
VMEDIA_UNMOUNT_UNSUPPORTED = (
    "- WARNING  - OOB management does not support Virtual Media unmount\n"
)

BIOS_PASS_SET_GOOD = f"""\
- INFO     - Command passed to set BIOS password.
- WARNING  - Host will now be rebooted for changes to take place.
- INFO     - Command passed to On server, code return is 200.
- INFO     - JobID = {JOB_ID}
- INFO     - Name = Task
- INFO     - Message = Job completed successfully.
- INFO     - PercentComplete = 100
"""
BIOS_PASS_SET_MISS_ARG = """\
- ERROR    - Missing argument: `--new-password`
"""
BIOS_PASS_RM_GOOD = (
    """\
- INFO     - Command passed to set BIOS password.
- WARNING  - Host will now be rebooted for changes to take place.
- INFO     - Command passed to On server, code return is 200.
- INFO     - JobID = %s
- INFO     - Name = Task
- INFO     - Message = Job completed successfully.
- INFO     - PercentComplete = 100
"""
    % JOB_ID
)
BIOS_PASS_RM_MISS_ARG = """\
- ERROR    - Missing argument: `--old-password`
"""

ATTRIBUTE_OK = "ProcC1E"
ATTRIBUTE_BAD = "NotThere"
ATTR_VALUE_OK = "Enabled"
ATTR_VALUE_BAD = "NotAllowed"
ATTR_VALUE_DIS = "Disabled"

BIOS_RESPONSE_OK = '{"Attributes":{"%s": "%s"}}' % (ATTRIBUTE_OK, ATTR_VALUE_OK)
BIOS_RESPONSE_DIS = '{"Attributes":{"%s": "%s"}}' % (ATTRIBUTE_OK, ATTR_VALUE_DIS)
BIOS_REGISTRY_BASE = '{"RegistryEntries": {"Attributes": %s}}'
BIOS_RESPONSE_SRIOV = '{"Attributes":{"SriovGlobalEnable": "%s"}}'
BIOS_REGISTRY_1 = {
    "AttributeName": "SystemModelName",
    "CurrentValue": "None",
    "DisplayName": "System Model Name",
    "DisplayOrder": 200,
    "HelpText": "Indicates the product name of the system.",
    "Hidden": "False",
    "Immutable": "True",
    "MaxLength": 40,
    "MenuPath": "./SysInformationRef",
    "MinLength": 0,
    "ReadOnly": "True",
    "ResetRequired": "True",
    "Type": "String",
    "ValueExpression": "None",
    "WriteOnly": "False",
}
BIOS_REGISTRY_2 = {
    "AttributeName": "ProcC1E",
    "CurrentValue": "None",
    "DisplayName": "C1E",
    "DisplayOrder": 9604,
    "HelpText": "When set to Enabled, the processor is allowed to switch to minimum performance state when idle.",
    "Hidden": "False",
    "Immutable": "False",
    "MenuPath": "./SysProfileSettingsRef",
    "ReadOnly": "False",
    "ResetRequired": "True",
    "Type": "Enumeration",
    "Value": [
        {"ValueDisplayName": "Enabled", "ValueName": "Enabled"},
        {"ValueDisplayName": "Disabled", "ValueName": "Disabled"},
    ],
    "WarningText": "None",
    "WriteOnly": "False",
}
BIOS_REGISTRY_OK = BIOS_REGISTRY_BASE % str([BIOS_REGISTRY_1, BIOS_REGISTRY_2])
BIOS_SET_OK = """\
- INFO     - Command passed to set BIOS attribute pending values.
- INFO     - Command passed to GracefulRestart server, code return is 200.
- INFO     - Polling for host state: Not Down
- INFO     - Command passed to On server, code return is 200.
"""
BIOS_SET_BAD_VALUE = (
    """\
- WARNING  - List of accepted values for '%s': ['Enabled', 'Disabled']
- ERROR    - Value not accepted
"""
    % ATTRIBUTE_OK
)
BIOS_SET_BAD_ATTR = """\
- WARNING  - Could not retrieve Bios Attributes.
- ERROR    - Attribute not found. Please check attribute name.
"""
BIOS_GET_ALL_OK = f"""- INFO     - {ATTRIBUTE_OK}: {ATTR_VALUE_OK}\n"""
BIOS_GET_ONE_OK = """\
- INFO     - AttributeName: ProcC1E
- INFO     - CurrentValue: Enabled
- INFO     - DisplayName: C1E
- INFO     - DisplayOrder: 9604
- INFO     - HelpText: When set to Enabled, the processor is allowed to switch to minimum performance state when idle.
- INFO     - Hidden: False
- INFO     - Immutable: False
- INFO     - MenuPath: ./SysProfileSettingsRef
- INFO     - ReadOnly: False
- INFO     - ResetRequired: True
- INFO     - Type: Enumeration
- INFO     - Value: [{'ValueDisplayName': 'Enabled', 'ValueName': 'Enabled'}, {'ValueDisplayName': 'Disabled', 'ValueName': 'Disabled'}]
- INFO     - WarningText: None
- INFO     - WriteOnly: False
"""
BIOS_GET_ONE_BAD = (
    """\
- WARNING  - Could not retrieve Bios Attributes.
- ERROR    - Unable to locate the Bios attribute: %s
"""
    % ATTRIBUTE_BAD
)

SRIOV_ALREADY = "- WARNING  - SRIOV mode is already in that state. IGNORING.\n"
SRIOV_STATE = "- INFO     - Enabled\n"

SCREENSHOT_OK = (
    """\
- INFO     - Image saved: %s
"""
    % SCREENSHOT_NAME
)
