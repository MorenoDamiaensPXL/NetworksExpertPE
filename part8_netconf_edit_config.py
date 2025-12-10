#!/usr/bin/env python
"""
Part 8: Getting Started with NETCONF/YANG – Part 2
Script 2: Configuratie wijzigen met NETCONF
"""

from ncclient import manager
import xml.dom.minidom
import datetime

print("=" * 60)
print("Part 8: NETCONF Edit Configuration")
print("=" * 60)
print(f"Datum/Tijd: {datetime.datetime.now()}")
print()

# Router configuratie - PAS DIT AAN NAAR JOUW ROUTER
ROUTER_CONFIG = {
    "host": "192.168.56.107",
    "port": 830,
    "username": "cisco",
    "password": "cisco123!",
    "hostkey_verify": False
}

# Configuratie templates

# Template om hostname te wijzigen
HOSTNAME_CONFIG = """
<config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <hostname>{hostname}</hostname>
    </native>
</config>
"""

# Template om interface beschrijving te wijzigen
INTERFACE_DESC_CONFIG = """
<config>
    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
            <name>{interface_name}</name>
            <description>{description}</description>
        </interface>
    </interfaces>
</config>
"""

# Template om loopback aan te maken
LOOPBACK_CONFIG = """
<config>
    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
            <name>Loopback{loopback_num}</name>
            <description>{description}</description>
            <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">
                ianaift:softwareLoopback
            </type>
            <enabled>true</enabled>
            <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                <address>
                    <ip>{ip_address}</ip>
                    <netmask>{netmask}</netmask>
                </address>
            </ipv4>
        </interface>
    </interfaces>
</config>
"""

# Template om interface te verwijderen
DELETE_INTERFACE_CONFIG = """
<config>
    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface operation="delete">
            <name>{interface_name}</name>
        </interface>
    </interfaces>
</config>
"""

def change_hostname(m, new_hostname):
    """Wijzig de hostname van de router."""
    print(f"\nWijzigen hostname naar: {new_hostname}")
    
    config = HOSTNAME_CONFIG.format(hostname=new_hostname)
    
    try:
        reply = m.edit_config(config, target='running')
        if reply.ok:
            print(f"SUCCES! Hostname gewijzigd naar: {new_hostname}")
            return True
        else:
            print(f"FOUT: {reply.errors}")
            return False
    except Exception as e:
        print(f"FOUT: {e}")
        return False

def change_interface_description(m, interface_name, description):
    """Wijzig de beschrijving van een interface."""
    print(f"\nWijzigen beschrijving van {interface_name}...")
    
    config = INTERFACE_DESC_CONFIG.format(
        interface_name=interface_name,
        description=description
    )
    
    try:
        reply = m.edit_config(config, target='running')
        if reply.ok:
            print(f"SUCCES! Beschrijving gewijzigd: {description}")
            return True
        else:
            print(f"FOUT: {reply.errors}")
            return False
    except Exception as e:
        print(f"FOUT: {e}")
        return False

def create_loopback(m, loopback_num, ip_address, netmask, description):
    """Maak een nieuwe loopback interface aan."""
    print(f"\nAanmaken Loopback{loopback_num}...")
    
    config = LOOPBACK_CONFIG.format(
        loopback_num=loopback_num,
        ip_address=ip_address,
        netmask=netmask,
        description=description
    )
    
    try:
        reply = m.edit_config(config, target='running')
        if reply.ok:
            print(f"SUCCES! Loopback{loopback_num} aangemaakt met IP {ip_address}")
            return True
        else:
            print(f"FOUT: {reply.errors}")
            return False
    except Exception as e:
        print(f"FOUT: {e}")
        return False

def delete_interface(m, interface_name):
    """Verwijder een interface."""
    print(f"\nVerwijderen {interface_name}...")
    
    config = DELETE_INTERFACE_CONFIG.format(interface_name=interface_name)
    
    try:
        reply = m.edit_config(config, target='running')
        if reply.ok:
            print(f"SUCCES! {interface_name} verwijderd")
            return True
        else:
            print(f"FOUT: {reply.errors}")
            return False
    except Exception as e:
        print(f"FOUT: {e}")
        return False

def show_menu():
    """Toon het hoofdmenu."""
    print("\n" + "="*60)
    print("NETCONF Configuration Menu")
    print("="*60)
    print("1. Wijzig hostname")
    print("2. Wijzig interface beschrijving")
    print("3. Maak loopback interface")
    print("4. Verwijder interface")
    print("5. Exit")
    print("-"*60)
    return input("Kies een optie (1-5): ")

def main():
    print(f"Verbinden met {ROUTER_CONFIG['host']}...")
    
    try:
        m = manager.connect(**ROUTER_CONFIG)
        print(f"Verbinding succesvol: {m.connected}")
        
        while True:
            choice = show_menu()
            
            if choice == "1":
                hostname = input("Nieuwe hostname: ")
                change_hostname(m, hostname)
                
            elif choice == "2":
                interface = input("Interface naam (bijv. GigabitEthernet1): ")
                desc = input("Nieuwe beschrijving: ")
                change_interface_description(m, interface, desc)
                
            elif choice == "3":
                num = input("Loopback nummer: ")
                ip = input("IP adres: ")
                mask = input("Netmask (bijv. 255.255.255.0): ")
                desc = input("Beschrijving: ")
                create_loopback(m, num, ip, mask, desc)
                
            elif choice == "4":
                interface = input("Interface naam om te verwijderen (bijv. Loopback100): ")
                confirm = input(f"Weet je zeker dat je {interface} wilt verwijderen? (ja/nee): ")
                if confirm.lower() == "ja":
                    delete_interface(m, interface)
                    
            elif choice == "5":
                print("\nAfsluiten...")
                break
            else:
                print("Ongeldige keuze, probeer opnieuw.")
        
        m.close_session()
        print("Sessie afgesloten.")
        
    except Exception as e:
        print(f"FOUT bij verbinden: {e}")

if __name__ == "__main__":
    main()
