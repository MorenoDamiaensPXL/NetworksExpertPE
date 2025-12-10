#!/usr/bin/env python
"""
Part 3a: Connecting to an IOS-XE Device
Send configuration commands to multiple devices
"""

from netmiko import ConnectHandler
from datetime import datetime

# Meerdere devices - PAS DIT AAN NAAR JOUW DEVICES
devices = [
    {
        "device_type": "cisco_ios",
        "host": "10.176.161.43",
        "port": 22,
        "username": "cisco",
        "password": "cisco123!",
        "device_name": "Router1"
    },
    # Voeg meer devices toe:
    # {
    #     "device_type": "cisco_ios",
    #     "host": "192.168.56.108",
    #     "port": 22,
    #     "username": "cisco",
    #     "password": "cisco123!",
    #     "device_name": "Router2"
    # },
]

# Configuratie om toe te passen op alle devices
config_commands = [
    "ntp server 0.pool.ntp.org",
    "ntp server 1.pool.ntp.org",
    "logging buffered 16384",
    "logging console warnings",
    "banner motd # Configured by automated script #",
    "ip domain-name lab.local"
]


def configure_device(device, commands):
    """Configureer een enkel device."""
    device_name = device.pop("device_name", device["host"])
    result = {
        "device": device_name,
        "host": device["host"],
        "status": "unknown"
    }
    
    try:
        print(f"[{device_name}] Verbinden...")
        net_connect = ConnectHandler(**device)
        hostname = net_connect.find_prompt().replace("#", "").replace(">", "")
        
        print(f"[{device_name}] Toepassen configuratie...")
        output = net_connect.send_config_set(commands)
        
        print(f"[{device_name}] Opslaan configuratie...")
        net_connect.save_config()
        
        result["status"] = "success"
        result["hostname"] = hostname
        result["output"] = output
        
        net_connect.disconnect()
        print(f"[{device_name}] ✓ Voltooid!")
        
    except Exception as e:
        result["status"] = "failed"
        result["error"] = str(e)
        print(f"[{device_name}] ✗ FOUT: {e}")
    
    return result


def main():
    print("=" * 60)
    print("Part 3a: Configuration on Multiple Devices")
    print("=" * 60)
    print(f"Datum: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Aantal devices: {len(devices)}")
    print()
    
    print("Configuratie die wordt toegepast:")
    for cmd in config_commands:
        print(f"  > {cmd}")
    print()
    
    # Bevestiging vragen
    confirm = input("Doorgaan met configuratie? (ja/nee): ")
    if confirm.lower() != "ja":
        print("Geannuleerd.")
        return
    
    print("\nStarten met configuratie...\n")
    
    all_results = []
    
    for device in devices:
        device_copy = device.copy()
        result = configure_device(device_copy, config_commands)
        all_results.append(result)
    
    # Rapport genereren
    print("\n" + "=" * 60)
    print("CONFIGURATIE RAPPORT")
    print("=" * 60)
    print(f"Tijdstip: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    for result in all_results:
        status_icon = "✓" if result["status"] == "success" else "✗"
        print(f"{status_icon} {result['device']} ({result['host']}): {result['status'].upper()}")
        
        if result["status"] == "failed":
            print(f"   Error: {result.get('error', 'Unknown')}")
    
    # Samenvatting
    success = sum(1 for r in all_results if r["status"] == "success")
    failed = len(all_results) - success
    
    print("\n" + "-" * 40)
    print(f"Succesvol: {success}/{len(all_results)}")
    print(f"Gefaald: {failed}/{len(all_results)}")
    
    if failed == 0:
        print("\n✓ Alle devices succesvol geconfigureerd!")
    else:
        print(f"\n⚠ {failed} device(s) gefaald - controleer de errors hierboven.")


if __name__ == "__main__":
    main()
