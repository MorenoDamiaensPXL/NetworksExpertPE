#!/usr/bin/env python
"""
Part 3a: Connecting to an IOS-XE Device
Backup device configuration to an external file
"""

from netmiko import ConnectHandler
from datetime import datetime
import os

# Router configuratie - PAS DIT AAN NAAR JOUW ROUTER
router = {
    "device_type": "cisco_ios",
    "host": "10.176.161.43",
    "port": 22,
    "username": "cisco",
    "password": "cisco123!"
}

print("=" * 60)
print("Part 3a: Backup Device Configuration")
print("=" * 60)

# Maak backup directory als die niet bestaat
backup_dir = "backups"
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)
    print(f"Backup directory aangemaakt: {backup_dir}/")

print(f"\nVerbinden met {router['host']}...")
net_connect = ConnectHandler(**router)
hostname = net_connect.find_prompt().replace("#", "").replace(">", "")
print(f"Verbonden met: {hostname}")

# Haal running-config op
print("Ophalen van running-config...")
running_config = net_connect.send_command("show running-config")

# Haal startup-config op
print("Ophalen van startup-config...")
startup_config = net_connect.send_command("show startup-config")

# Maak backup bestanden
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Running config backup
running_filename = f"{backup_dir}/{hostname}_running_{timestamp}.cfg"
with open(running_filename, "w") as f:
    f.write(f"! Backup van {hostname}\n")
    f.write(f"! Datum: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"! Type: Running Configuration\n")
    f.write("!\n")
    f.write(running_config)

print(f"Running config opgeslagen: {running_filename}")

# Startup config backup
startup_filename = f"{backup_dir}/{hostname}_startup_{timestamp}.cfg"
with open(startup_filename, "w") as f:
    f.write(f"! Backup van {hostname}\n")
    f.write(f"! Datum: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"! Type: Startup Configuration\n")
    f.write("!\n")
    f.write(startup_config)

print(f"Startup config opgeslagen: {startup_filename}")

net_connect.disconnect()
print("\nBackup voltooid! Verbinding afgesloten.")
