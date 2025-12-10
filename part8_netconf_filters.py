#!/usr/bin/env python
"""
Part 8: Getting Started with NETCONF/YANG – Part 2
Script 1: Werken met NETCONF filters
"""

from ncclient import manager
import xml.dom.minidom
import datetime

print("=" * 60)
print("Part 8: NETCONF Filters en Structured Data")
print("=" * 60)
print(f"Datum/Tijd: {datetime.datetime.now()}")
print()

# Router configuratie - PAS DIT AAN NAAR JOUW ROUTER
ROUTER_CONFIG = {
    "host": "10.176.161.43",
    "port": 830,
    "username": "cisco",
    "password": "cisco123!",
    "hostkey_verify": False
}

# Filter templates
FILTERS = {
    # Filter voor interfaces (configuratie)
    "interfaces_config": """
        <filter>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface>
                    <name/>
                    <type/>
                    <enabled/>
                    <description/>
                </interface>
            </interfaces>
        </filter>
    """,
    
    # Filter voor interface statistieken (operational)
    "interfaces_state": """
        <filter>
            <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface>
                    <name/>
                    <oper-status/>
                    <statistics/>
                </interface>
            </interfaces-state>
        </filter>
    """,
    
    # Filter voor hostname
    "hostname": """
        <filter>
            <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                <hostname/>
            </native>
        </filter>
    """,
    
    # Filter voor specifieke interface
    "specific_interface": """
        <filter>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface>
                    <name>GigabitEthernet1</name>
                </interface>
            </interfaces>
        </filter>
    """
}

def pretty_print_xml(xml_data):
    """Format XML netjes voor output."""
    return xml.dom.minidom.parseString(xml_data).toprettyxml(indent="  ")

def get_config_with_filter(m, filter_name):
    """Haal configuratie op met een specifiek filter."""
    print(f"\n{'='*60}")
    print(f"Filter: {filter_name}")
    print(f"{'='*60}")
    
    try:
        response = m.get_config(source="running", filter=FILTERS[filter_name])
        print(pretty_print_xml(response.xml))
    except Exception as e:
        print(f"FOUT: {e}")

def get_operational_with_filter(m, filter_name):
    """Haal operationele data op met een specifiek filter."""
    print(f"\n{'='*60}")
    print(f"Operational Data - Filter: {filter_name}")
    print(f"{'='*60}")
    
    try:
        response = m.get(filter=FILTERS[filter_name])
        print(pretty_print_xml(response.xml))
    except Exception as e:
        print(f"FOUT: {e}")

def main():
    print(f"Verbinden met {ROUTER_CONFIG['host']}...")
    
    try:
        m = manager.connect(**ROUTER_CONFIG)
        print(f"Verbinding succesvol: {m.connected}")
        
        # Demonstreer verschillende filters
        
        # 1. Configuratie data - interfaces
        get_config_with_filter(m, "interfaces_config")
        
        # 2. Configuratie data - hostname
        get_config_with_filter(m, "hostname")
        
        # 3. Operationele data - interface statistieken
        get_operational_with_filter(m, "interfaces_state")
        
        # 4. Specifieke interface configuratie
        get_config_with_filter(m, "specific_interface")
        
        m.close_session()
        print("\n" + "="*60)
        print("Sessie afgesloten.")
        
    except Exception as e:
        print(f"FOUT bij verbinden: {e}")

if __name__ == "__main__":
    main()
