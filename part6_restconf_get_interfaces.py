#!/usr/bin/env python
"""
Part 6: Use RESTCONF to Access an IOS XE Device
Script 1: GET interfaces via RESTCONF
"""

import requests
import json
import datetime

# Disable SSL warnings voor self-signed certificates
requests.packages.urllib3.disable_warnings()

print("=" * 60)
print("Part 6: RESTCONF GET Interfaces")
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

# API endpoints
endpoints = {
    "interfaces": f"https://{IP_ADDRESS}/restconf/data/ietf-interfaces:interfaces",
    "hostname": f"https://{IP_ADDRESS}/restconf/data/Cisco-IOS-XE-native:native/hostname",
    "version": f"https://{IP_ADDRESS}/restconf/data/Cisco-IOS-XE-native:native/version"
}

def get_interfaces():
    """Haal alle interfaces op via RESTCONF."""
    
    url = endpoints["interfaces"]
    print(f"Request URL: {url}")
    print()
    
    try:
        resp = requests.get(url, auth=basicauth, headers=headers, verify=False)
        
        print(f"Status Code: {resp.status_code}")
        print()
        
        if resp.status_code == 200:
            print("=" * 60)
            print("Interfaces Data (JSON):")
            print("=" * 60)
            response_json = resp.json()
            print(json.dumps(response_json, indent=4))
            
            # Tel interfaces
            if "ietf-interfaces:interfaces" in response_json:
                interfaces = response_json["ietf-interfaces:interfaces"].get("interface", [])
                print()
                print("=" * 60)
                print(f"Samenvatting: {len(interfaces)} interface(s) gevonden")
                print("=" * 60)
                for iface in interfaces:
                    print(f"  - {iface.get('name', 'Unknown')}: {iface.get('description', 'No description')}")
        else:
            print(f"FOUT: {resp.status_code}")
            print(resp.text)
            
    except Exception as e:
        print(f"FOUT: {e}")

def get_hostname():
    """Haal hostname op via RESTCONF."""
    
    url = endpoints["hostname"]
    print(f"\nRequest URL: {url}")
    
    try:
        resp = requests.get(url, auth=basicauth, headers=headers, verify=False)
        
        if resp.status_code == 200:
            print(f"Hostname: {resp.json()}")
        else:
            print(f"Status: {resp.status_code}")
            
    except Exception as e:
        print(f"FOUT: {e}")

if __name__ == "__main__":
    get_interfaces()
    get_hostname()
