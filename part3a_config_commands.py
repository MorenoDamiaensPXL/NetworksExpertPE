#!/usr/bin/env python
"""
Part 3a: Connecting to an IOS-XE Device
Send configuration commands to a single device
"""

from netmiko import ConnectHandler

# Router configuratie - PAS DIT AAN NAAR JOUW ROUTER
router = {
    "device_type": "cisco_ios",
    "host": "10.176.161.43",
    "port": 22,
    "username": "cisco",
    "password": "cisco123!"
}

print("=" * 60)
print("Part 3a: Send Configuration Commands")
print("=" * 60)

# Configuratie commands
config_commands = [
    "interface Loopback99",
    "description Created by Netmiko Script",
    "ip address 10.99.99.1 255.255.255.0",
    "no shutdown"
]

print(f"\nVerbinden met {router['host']}...")
net_connect = ConnectHandler(**router)
print("Verbinding succesvol!")

print("\nSturen van configuratie commands:")
for cmd in config_commands:
    print(f"  > {cmd}")

# Stuur config commands
output = net_connect.send_config_set(config_commands)
print("\nOutput:")
print(output)

# Verifieer de configuratie
print("\n" + "=" * 60)
print("Verificatie - show run interface Loopback99:")
print("=" * 60)
verify = net_connect.send_command("show run interface Loopback99")
print(verify)

# Sla configuratie op
print("\nOpslaan van configuratie...")
net_connect.save_config()
print("Configuratie opgeslagen!")

net_connect.disconnect()
print("\nVerbinding afgesloten.")
