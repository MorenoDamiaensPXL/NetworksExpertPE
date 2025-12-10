#!/usr/bin/env python
"""
Part 3a: Connecting to an IOS-XE Device
Send show commands to multiple devices
"""

from netmiko import ConnectHandler
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# Meerdere devices - PAS DIT AAN NAAR JOUW DEVICES
devices = [
    {
        "device_type": "cisco_ios",
        "host": "192.168.56.107",
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

# Commands om uit te voeren op alle devices
commands = [
    "show version | include Version",
    "show ip interface brief",
    "show clock"
]


def execute_on_device(device):
    """Voer commands uit op een enkel device."""
    device_name = device.pop("device_name", device["host"])
    results = {"device": device_name, "host": device["host"], "commands": {}}
    
    try:
        print(f"[{device_name}] Verbinden...")
        net_connect = ConnectHandler(**device)
        
        for cmd in commands:
            output = net_connect.send_command(cmd)
            results["commands"][cmd] = output
        
        results["status"] = "success"
        net_connect.disconnect()
        print(f"[{device_name}] Voltooid!")
        
    except Exception as e:
        results["status"] = "failed"
        results["error"] = str(e)
        print(f"[{device_name}] FOUT: {e}")
    
    return results


def main():
    print("=" * 60)
    print("Part 3a: Show Commands on Multiple Devices")
    print("=" * 60)
    print(f"Datum: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Aantal devices: {len(devices)}")
    print(f"Commands per device: {len(commands)}")
    print()
    
    all_results = []
    
    # Sequentieel uitvoeren (voor kleine aantallen)
    for device in devices:
        device_copy = device.copy()  # Maak kopie om origineel niet te wijzigen
        result = execute_on_device(device_copy)
        all_results.append(result)
    
    # Of gebruik threading voor grotere aantallen:
    # with ThreadPoolExecutor(max_workers=5) as executor:
    #     all_results = list(executor.map(execute_on_device, devices))
    
    # Toon resultaten
    print("\n" + "=" * 60)
    print("RESULTATEN")
    print("=" * 60)
    
    for result in all_results:
        print(f"\n{'='*40}")
        print(f"Device: {result['device']} ({result['host']})")
        print(f"Status: {result['status'].upper()}")
        print(f"{'='*40}")
        
        if result["status"] == "success":
            for cmd, output in result["commands"].items():
                print(f"\n> {cmd}")
                print("-" * 40)
                print(output)
        else:
            print(f"Error: {result.get('error', 'Unknown')}")
    
    # Samenvatting
    success = sum(1 for r in all_results if r["status"] == "success")
    failed = len(all_results) - success
    
    print("\n" + "=" * 60)
    print("SAMENVATTING")
    print("=" * 60)
    print(f"Totaal devices: {len(all_results)}")
    print(f"Succesvol: {success}")
    print(f"Gefaald: {failed}")


if __name__ == "__main__":
    main()
