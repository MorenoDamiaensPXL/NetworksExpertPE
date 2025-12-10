#!/usr/bin/env python
"""
Part 3a: Connecting to an IOS-XE Device
Execute a script with conditional statements (if, else)
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

print("=" * 60)
print("Part 3a: Script with Conditional Statements")
print("=" * 60)

print(f"\nVerbinden met {router['host']}...")
net_connect = ConnectHandler(**router)
hostname = net_connect.find_prompt().replace("#", "").replace(">", "")
print(f"Verbonden met: {hostname}")

# Voorbeeld 1: Controleer of een interface bestaat
interface_to_check = "Loopback100"
print(f"\n--- Check 1: Bestaat {interface_to_check}? ---")

output = net_connect.send_command(f"show run interface {interface_to_check}")

if "Invalid input" in output or "not found" in output.lower():
    print(f"{interface_to_check} bestaat NIET.")
    print("Interface wordt aangemaakt...")
    
    commands = [
        f"interface {interface_to_check}",
        "description Auto-created by conditional script",
        "ip address 10.100.100.1 255.255.255.0",
        "no shutdown"
    ]
    net_connect.send_config_set(commands)
    print(f"{interface_to_check} is aangemaakt!")
else:
    print(f"{interface_to_check} bestaat al:")
    print(output)


# Voorbeeld 2: Controleer interface status
print("\n--- Check 2: Interface Status Check ---")
interfaces_output = net_connect.send_command("show ip interface brief")

# Parse de output
lines = interfaces_output.strip().split("\n")
down_interfaces = []
up_interfaces = []

for line in lines[1:]:  # Skip header
    parts = line.split()
    if len(parts) >= 5:
        interface_name = parts[0]
        status = parts[4]  # Status kolom
        
        if status == "down":
            down_interfaces.append(interface_name)
        elif status == "up":
            up_interfaces.append(interface_name)

print(f"Interfaces UP: {len(up_interfaces)}")
print(f"Interfaces DOWN: {len(down_interfaces)}")

if down_interfaces:
    print("\nWaarschuwing! De volgende interfaces zijn down:")
    for iface in down_interfaces:
        print(f"  - {iface}")
else:
    print("\nAlle interfaces zijn operationeel!")


# Voorbeeld 3: Controleer software versie
print("\n--- Check 3: Software Versie Check ---")
version_output = net_connect.send_command("show version | include Version")

if "17." in version_output:
    print("Router draait IOS-XE 17.x (nieuwste)")
    ios_version = "17.x"
elif "16." in version_output:
    print("Router draait IOS-XE 16.x")
    ios_version = "16.x"
elif "15." in version_output:
    print("Router draait IOS 15.x (legacy)")
    ios_version = "15.x"
else:
    print("Onbekende versie")
    ios_version = "unknown"

print(f"Gedetecteerde versie: {ios_version}")


# Voorbeeld 4: CDP neighbors check
print("\n--- Check 4: CDP Neighbors ---")
cdp_output = net_connect.send_command("show cdp neighbors")

if "not enabled" in cdp_output.lower():
    print("CDP is uitgeschakeld op dit device.")
    enable_cdp = input("Wil je CDP inschakelen? (ja/nee): ")
    
    if enable_cdp.lower() == "ja":
        net_connect.send_config_set(["cdp run"])
        print("CDP is ingeschakeld!")
    else:
        print("CDP blijft uitgeschakeld.")
elif "Device" in cdp_output:
    # Tel neighbors
    neighbor_lines = [l for l in cdp_output.split("\n") if l.strip() and not l.startswith("Device") and not l.startswith("Capability")]
    neighbor_count = len(neighbor_lines) - 2  # Minus header lines
    
    if neighbor_count > 0:
        print(f"Gevonden: {neighbor_count} CDP neighbor(s)")
        print(cdp_output)
    else:
        print("Geen CDP neighbors gevonden.")
else:
    print("Geen CDP neighbors gevonden.")


# Voorbeeld 5: Configuratie compliance check
print("\n--- Check 5: Configuratie Compliance ---")
running_config = net_connect.send_command("show running-config")

compliance_checks = {
    "SSH enabled": "ip ssh version 2" in running_config or "transport input ssh" in running_config,
    "Banner configured": "banner" in running_config.lower(),
    "Enable secret set": "enable secret" in running_config,
    "HTTPS server": "ip http secure-server" in running_config,
    "Logging enabled": "logging" in running_config
}

print("\nCompliance Resultaten:")
all_compliant = True
for check, passed in compliance_checks.items():
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"  {check}: {status}")
    if not passed:
        all_compliant = False

if all_compliant:
    print("\n✓ Device is volledig compliant!")
else:
    print("\n✗ Device heeft compliance issues.")

# Sla eventuele wijzigingen op
net_connect.save_config()
net_connect.disconnect()
print("\nScript voltooid. Verbinding afgesloten.")
