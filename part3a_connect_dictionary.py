#!/usr/bin/env python
"""
Part 3a: Connecting to an IOS-XE Device
Connect using a Python Dictionary (expanded example)
"""

from netmiko import ConnectHandler
from pprint import pprint

# Meerdere devices in een dictionary
devices = {
    "router1": {
        "device_type": "cisco_ios",
        "host": "10.176.161.43",
        "port": 22,
        "username": "cisco",
        "password": "cisco123!",
        "secret": "cisco123!"  # Enable password indien nodig
    },
    # Voeg meer devices toe indien nodig
    # "router2": {
    #     "device_type": "cisco_ios",
    #     "host": "192.168.56.108",
    #     "port": 22,
    #     "username": "cisco",
    #     "password": "cisco123!"
    # }
}

print("=" * 60)
print("Part 3a: Connect Using Python Dictionary")
print("=" * 60)

# Resultaten opslaan in dictionary
results = {}

for device_name, device_params in devices.items():
    print(f"\n{'='*40}")
    print(f"Device: {device_name}")
    print(f"{'='*40}")
    
    try:
        print(f"Verbinden met {device_params['host']}...")
        net_connect = ConnectHandler(**device_params)
        
        # Haal informatie op
        hostname = net_connect.find_prompt().replace("#", "").replace(">", "")
        version_output = net_connect.send_command("show version | include Version")
        interfaces = net_connect.send_command("show ip interface brief")
        
        # Sla op in results dictionary
        results[device_name] = {
            "hostname": hostname,
            "ip": device_params["host"],
            "version": version_output.strip(),
            "status": "success",
            "interfaces": interfaces
        }
        
        print(f"Hostname: {hostname}")
        print(f"Version: {version_output.strip()}")
        
        net_connect.disconnect()
        
    except Exception as e:
        results[device_name] = {
            "ip": device_params["host"],
            "status": "failed",
            "error": str(e)
        }
        print(f"FOUT: {e}")

# Toon samenvatting
print("\n" + "=" * 60)
print("SAMENVATTING")
print("=" * 60)
pprint(results)
