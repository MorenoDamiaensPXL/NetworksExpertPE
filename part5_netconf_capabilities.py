#!/usr/bin/env python
"""
Part 5: Use NETCONF to Access an IOS XE Device
Script 1: NETCONF Capabilities ophalen
"""

from ncclient import manager
import datetime

print("=" * 60)
print("Part 5: NETCONF Capabilities")
print("=" * 60)
print(f"Datum/Tijd: {datetime.datetime.now()}")
print()

# Router configuratie - PAS DIT AAN NAAR JOUW ROUTER
ROUTER_IP = "192.168.56.107"
ROUTER_PORT = 830
ROUTER_USER = "cisco"
ROUTER_PASS = "cisco123!"

print(f"Verbinden met {ROUTER_IP}:{ROUTER_PORT}...")

try:
    m = manager.connect(
        host=ROUTER_IP,
        port=ROUTER_PORT,
        username=ROUTER_USER,
        password=ROUTER_PASS,
        hostkey_verify=False
    )
    
    print(f"Verbinding status: {m.connected}")
    print(f"Session ID: {m.session_id}")
    print()
    
    print("=" * 60)
    print("Server Capabilities:")
    print("=" * 60)
    
    count = 0
    for capability in m.server_capabilities:
        count += 1
        print(f"{count}. {capability}")
    
    print()
    print(f"Totaal: {count} capabilities")
    
    m.close_session()
    print("\nSessie afgesloten.")
    
except Exception as e:
    print(f"FOUT bij verbinden: {e}")
