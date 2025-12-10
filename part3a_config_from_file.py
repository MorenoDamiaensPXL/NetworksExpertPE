#!/usr/bin/env python
"""
Part 3a: Connecting to an IOS-XE Device
Send device configuration using an external file
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

# Configuratie bestand
CONFIG_FILE = "device_config.txt"

print("=" * 60)
print("Part 3a: Configure Device from External File")
print("=" * 60)

# Maak een voorbeeld configuratie bestand als het niet bestaat
try:
    with open(CONFIG_FILE, "r") as f:
        config_lines = f.read().splitlines()
        print(f"Configuratie bestand gevonden: {CONFIG_FILE}")
except FileNotFoundError:
    print(f"Configuratie bestand niet gevonden. Aanmaken: {CONFIG_FILE}")
    example_config = """! Voorbeeld configuratie bestand
! Pas dit aan naar je eigen wensen
!
interface Loopback50
 description Configured from file
 ip address 10.50.50.1 255.255.255.0
!
interface Loopback51
 description Also from file
 ip address 10.51.51.1 255.255.255.0
!
banner motd # Configured by Netmiko from file #
"""
    with open(CONFIG_FILE, "w") as f:
        f.write(example_config)
    config_lines = example_config.splitlines()
    print(f"Voorbeeld bestand aangemaakt: {CONFIG_FILE}")

# Filter lege regels en comments
config_commands = [line for line in config_lines if line.strip() and not line.strip().startswith("!")]

print(f"\nTe configureren commands ({len(config_commands)}):")
for cmd in config_commands:
    print(f"  > {cmd}")

print(f"\nVerbinden met {router['host']}...")
net_connect = ConnectHandler(**router)
print("Verbinding succesvol!")

# Stuur configuratie
print("\nToepassen van configuratie...")
output = net_connect.send_config_set(config_commands)
print(output)

# Sla op
print("\nOpslaan van configuratie...")
net_connect.save_config()
print("Configuratie opgeslagen!")

net_connect.disconnect()
print("\nVerbinding afgesloten.")
