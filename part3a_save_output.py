#!/usr/bin/env python
"""
Part 3a: Connecting to an IOS-XE Device
Run show commands and save the output to a file
"""

from netmiko import ConnectHandler
from datetime import datetime

# Router configuratie - PAS DIT AAN NAAR JOUW ROUTER
router = {
    "device_type": "cisco_ios",
    "host": "192.168.56.107",
    "port": 22,
    "username": "cisco",
    "password": "cisco123!"
}

print("=" * 60)
print("Part 3a: Save Show Command Output to File")
print("=" * 60)

# Commands om uit te voeren
commands = [
    "show version",
    "show ip interface brief",
    "show interfaces status",
    "show cdp neighbors",
    "show ip route"
]

print(f"\nVerbinden met {router['host']}...")
net_connect = ConnectHandler(**router)
hostname = net_connect.find_prompt().replace("#", "").replace(">", "")
print(f"Verbonden met: {hostname}")

# Maak output bestand
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"{hostname}_show_output_{timestamp}.txt"

with open(filename, "w") as f:
    f.write(f"{'='*60}\n")
    f.write(f"Device: {hostname} ({router['host']})\n")
    f.write(f"Datum: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"{'='*60}\n\n")
    
    for cmd in commands:
        print(f"Uitvoeren: {cmd}")
        output = net_connect.send_command(cmd)
        
        f.write(f"\n{'='*60}\n")
        f.write(f"Command: {cmd}\n")
        f.write(f"{'='*60}\n")
        f.write(output)
        f.write("\n")

net_connect.disconnect()

print(f"\nOutput opgeslagen naar: {filename}")
print("Verbinding afgesloten.")
