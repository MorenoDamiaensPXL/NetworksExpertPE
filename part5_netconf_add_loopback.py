#!/usr/bin/env python
"""
Part 5: Use NETCONF to Access an IOS XE Device
Script 3: Loopback interface toevoegen via NETCONF
"""

from ncclient import manager
import datetime

print("=" * 60)
print("Part 5: NETCONF Add Loopback Interface")
print("=" * 60)
print(f"Datum/Tijd: {datetime.datetime.now()}")
print()

# Router configuratie - PAS DIT AAN NAAR JOUW ROUTER
ROUTER_IP = "192.168.56.107"
ROUTER_PORT = 830
ROUTER_USER = "cisco"
ROUTER_PASS = "cisco123!"

# IETF Interface Types
IETF_INTERFACE_TYPES = {
    "loopback": "ianaift:softwareLoopback",
    "ethernet": "ianaift:ethernetCsmacd"
}

# XML template voor interface configuratie
NETCONF_INTERFACE_TEMPLATE = """
<config>
    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
            <name>{if_name}</name>
            <description>{if_desc}</description>
            <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">
                {if_type}
            </type>
            <enabled>{if_status}</enabled>
            <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                <address>
                    <ip>{ip_address}</ip>
                    <netmask>{subnet_mask}</netmask>
                </address>
            </ipv4>
        </interface>
    </interfaces>
</config>
"""

def add_loopback():
    """Voeg een nieuwe loopback interface toe."""
    
    print("Loopback Interface Configuratie")
    print("-" * 40)
    
    # Vraag om interface details
    loopback_num = input("Loopback nummer (bijv. 100): ") or "100"
    description = input("Beschrijving (bijv. NETCONF Test): ") or "Created via NETCONF"
    ip_address = input("IP adres (bijv. 10.10.10.1): ") or "10.10.10.1"
    subnet_mask = input("Subnet mask (bijv. 255.255.255.0): ") or "255.255.255.0"
    
    # Bouw configuratie
    new_loopback = {
        "if_name": f"Loopback{loopback_num}",
        "if_desc": description,
        "if_type": IETF_INTERFACE_TYPES["loopback"],
        "if_status": "true",
        "ip_address": ip_address,
        "subnet_mask": subnet_mask
    }
    
    netconf_data = NETCONF_INTERFACE_TEMPLATE.format(**new_loopback)
    
    print()
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
        print(f"Aanmaken van {new_loopback['if_name']}...")
        
        # Stuur de configuratie
        netconf_reply = m.edit_config(netconf_data, target='running')
        
        if netconf_reply.ok:
            print("=" * 60)
            print("SUCCES! Loopback interface aangemaakt:")
            print("=" * 60)
            print(f"  Interface: {new_loopback['if_name']}")
            print(f"  Beschrijving: {new_loopback['if_desc']}")
            print(f"  IP Adres: {new_loopback['ip_address']}")
            print(f"  Subnet Mask: {new_loopback['subnet_mask']}")
        else:
            print(f"FOUT: {netconf_reply.errors}")
        
        m.close_session()
        
    except Exception as e:
        print(f"FOUT: {e}")

if __name__ == "__main__":
    add_loopback()
