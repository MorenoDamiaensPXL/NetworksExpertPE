#!/usr/bin/env python
"""
Part 3a: Connecting to an IOS-XE Device
Configure a subset of interfaces
"""

from netmiko import ConnectHandler

# Router configuratie - PAS DIT AAN NAAR JOUW ROUTER
router = {
    "device_type": "cisco_ios",
    "host": "192.168.56.107",
    "port": 22,
    "username": "cisco",
    "password": "cisco123!"
}

# Interfaces om te configureren
interfaces_config = {
    "Loopback10": {
        "description": "Management Loopback",
        "ip": "10.10.10.1",
        "mask": "255.255.255.0"
    },
    "Loopback20": {
        "description": "Data Loopback",
        "ip": "10.20.20.1",
        "mask": "255.255.255.0"
    },
    "Loopback30": {
        "description": "Voice Loopback",
        "ip": "10.30.30.1",
        "mask": "255.255.255.0"
    }
}

print("=" * 60)
print("Part 3a: Configure Subset of Interfaces")
print("=" * 60)

print(f"\nVerbinden met {router['host']}...")
net_connect = ConnectHandler(**router)
hostname = net_connect.find_prompt().replace("#", "").replace(">", "")
print(f"Verbonden met: {hostname}")

# Configureer elke interface
for interface, config in interfaces_config.items():
    print(f"\nConfigureren van {interface}...")
    
    commands = [
        f"interface {interface}",
        f"description {config['description']}",
        f"ip address {config['ip']} {config['mask']}",
        "no shutdown"
    ]
    
    output = net_connect.send_config_set(commands)
    print(f"  Beschrijving: {config['description']}")
    print(f"  IP: {config['ip']}/{config['mask']}")

# Verificatie
print("\n" + "=" * 60)
print("Verificatie - Geconfigureerde interfaces:")
print("=" * 60)

for interface in interfaces_config.keys():
    output = net_connect.send_command(f"show run interface {interface}")
    print(f"\n{interface}:")
    print(output)

# Sla op
net_connect.save_config()
print("\nConfiguratie opgeslagen!")

net_connect.disconnect()
print("Verbinding afgesloten.")
