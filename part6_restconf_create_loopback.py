#!/usr/bin/env python
"""
Part 6: Use RESTCONF to Access an IOS XE Device
Script 2: PUT/POST om loopback interface aan te maken via RESTCONF
"""

import requests
import json
import datetime

# Disable SSL warnings voor self-signed certificates
requests.packages.urllib3.disable_warnings()

print("=" * 60)
print("Part 6: RESTCONF Create Loopback Interface")
print("=" * 60)
print(f"Datum/Tijd: {datetime.datetime.now()}")
print()

# Router configuratie - PAS DIT AAN NAAR JOUW ROUTER
IP_ADDRESS = "192.168.56.107"
RESTCONF_USERNAME = "cisco"
RESTCONF_PASSWORD = "cisco123!"

# RESTCONF setup
basicauth = (RESTCONF_USERNAME, RESTCONF_PASSWORD)
headers = {
    "Accept": "application/yang-data+json",
    "Content-type": "application/yang-data+json"
}

def create_loopback(loopback_num, ip_address, netmask, description):
    """Maak een nieuwe loopback interface via RESTCONF PUT."""
    
    # API URL voor specifieke interface
    api_url = f"https://{IP_ADDRESS}/restconf/data/ietf-interfaces:interfaces/interface=Loopback{loopback_num}"
    
    # YANG configuratie data
    yang_config = {
        "ietf-interfaces:interface": {
            "name": f"Loopback{loopback_num}",
            "description": description,
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": ip_address,
                        "netmask": netmask
                    }
                ]
            },
            "ietf-ip:ipv6": {}
        }
    }
    
    print(f"Request URL: {api_url}")
    print()
    print("Configuratie data:")
    print(json.dumps(yang_config, indent=4))
    print()
    
    try:
        # PUT request om interface aan te maken/vervangen
        resp = requests.put(
            api_url,
            data=json.dumps(yang_config),
            auth=basicauth,
            headers=headers,
            verify=False
        )
        
        print(f"Status Code: {resp.status_code}")
        
        if resp.status_code >= 200 and resp.status_code <= 299:
            print("=" * 60)
            print("SUCCES! Interface aangemaakt/bijgewerkt:")
            print("=" * 60)
            print(f"  Interface: Loopback{loopback_num}")
            print(f"  IP Adres: {ip_address}")
            print(f"  Netmask: {netmask}")
            print(f"  Beschrijving: {description}")
            return True
        else:
            print("=" * 60)
            print("FOUT bij aanmaken interface:")
            print("=" * 60)
            print(f"Status: {resp.status_code}")
            if resp.text:
                print(f"Response: {resp.text}")
            return False
            
    except Exception as e:
        print(f"FOUT: {e}")
        return False

def delete_loopback(loopback_num):
    """Verwijder een loopback interface via RESTCONF DELETE."""
    
    api_url = f"https://{IP_ADDRESS}/restconf/data/ietf-interfaces:interfaces/interface=Loopback{loopback_num}"
    
    print(f"Verwijderen van Loopback{loopback_num}...")
    
    try:
        resp = requests.delete(api_url, auth=basicauth, headers=headers, verify=False)
        
        if resp.status_code == 204:
            print(f"SUCCES! Loopback{loopback_num} verwijderd.")
            return True
        else:
            print(f"FOUT: Status {resp.status_code}")
            return False
            
    except Exception as e:
        print(f"FOUT: {e}")
        return False

if __name__ == "__main__":
    print("Loopback Interface Configuratie via RESTCONF")
    print("-" * 40)
    
    # Vraag om interface details
    loopback_num = input("Loopback nummer (bijv. 101): ") or "101"
    ip_address = input("IP adres (bijv. 10.1.0.1): ") or "10.1.0.1"
    netmask = input("Netmask (bijv. 255.255.255.0): ") or "255.255.255.0"
    description = input("Beschrijving: ") or "Created via RESTCONF"
    
    print()
    create_loopback(loopback_num, ip_address, netmask, description)
