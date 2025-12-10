#!/usr/bin/env python
"""
Part 3a: Connecting to an IOS-XE Device
Basic script - Send show commands to a single device
"""

from netmiko import ConnectHandler
from pprint import pprint

# Router configuratie - PAS DIT AAN NAAR JOUW ROUTER
router = {
    "device_type": "cisco_ios",
    "host": "192.168.56.107",
    "port": 22,
    "username": "cisco",
    "password": "cisco123!"
}

print("=" * 60)
print("Part 3a: Send Show Commands to Single Device")
print("=" * 60)

# Maak verbinding
print(f"\nVerbinden met {router['host']}...")
net_connect = ConnectHandler(**router)
print("Verbinding succesvol!")

# Stuur show commands
commands = ["show version", "show ip interface brief", "show running-config | section interface"]

for cmd in commands:
    print(f"\n{'='*60}")
    print(f"Command: {cmd}")
    print("=" * 60)
    output = net_connect.send_command(cmd)
    print(output)

# Sluit verbinding
net_connect.disconnect()
print("\nVerbinding afgesloten.")
