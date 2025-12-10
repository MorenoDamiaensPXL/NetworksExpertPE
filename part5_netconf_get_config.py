#!/usr/bin/env python
"""
Part 5: Use NETCONF to Access an IOS XE Device
Script 2: Running configuratie ophalen
"""

from ncclient import manager
import xml.dom.minidom
import datetime

print("=" * 60)
print("Part 5: NETCONF Get Running Config")
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
    
    print(f"Verbinding succesvol: {m.connected}")
    print()
    
    # Haal running config op
    print("Ophalen van running-config...")
    netconf_reply = m.get_config(source="running")
    
    # Parse en print de XML mooi geformatteerd
    print("=" * 60)
    print("Running Configuration (XML):")
    print("=" * 60)
    pretty_xml = xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml()
    print(pretty_xml)
    
    # Optioneel: sla op naar bestand
    with open("running_config_backup.xml", "w") as f:
        f.write(pretty_xml)
    print("\nConfig opgeslagen naar: running_config_backup.xml")
    
    m.close_session()
    
except Exception as e:
    print(f"FOUT: {e}")
