#!/usr/bin/env python
"""
Part 4: Explore YANG Models
Dit script haalt de YANG capabilities op van een IOS-XE device via NETCONF.
"""

from ncclient import manager
import datetime

print("=" * 60)
print("Part 4: YANG Models Explorer")
print("=" * 60)
print(f"Datum/Tijd: {datetime.datetime.now()}")
print()

# Router configuratie - PAS DIT AAN NAAR JOUW ROUTER
ROUTER_CONFIG = {
    "host": "192.168.56.107",  # IP adres van je CSR1000v
    "port": 830,
    "username": "cisco",
    "password": "cisco123!",
    "hostkey_verify": False
}

def get_yang_capabilities():
    """Haal alle YANG model capabilities op van de router."""
    
    print(f"Verbinden met {ROUTER_CONFIG['host']}:{ROUTER_CONFIG['port']}...")
    
    try:
        m = manager.connect(**ROUTER_CONFIG)
        print(f"Verbinding succesvol: {m.connected}")
        print()
        
        # Categoriseer capabilities
        ietf_models = []
        cisco_models = []
        openconfig_models = []
        other_models = []
        
        for capability in m.server_capabilities:
            if "ietf" in capability.lower():
                ietf_models.append(capability)
            elif "cisco" in capability.lower():
                cisco_models.append(capability)
            elif "openconfig" in capability.lower():
                openconfig_models.append(capability)
            else:
                other_models.append(capability)
        
        print("=" * 60)
        print(f"IETF YANG Models ({len(ietf_models)}):")
        print("=" * 60)
        for model in sorted(ietf_models)[:10]:  # Eerste 10
            print(f"  - {model}")
        if len(ietf_models) > 10:
            print(f"  ... en {len(ietf_models) - 10} meer")
        
        print()
        print("=" * 60)
        print(f"Cisco YANG Models ({len(cisco_models)}):")
        print("=" * 60)
        for model in sorted(cisco_models)[:10]:  # Eerste 10
            print(f"  - {model}")
        if len(cisco_models) > 10:
            print(f"  ... en {len(cisco_models) - 10} meer")
        
        print()
        print("=" * 60)
        print(f"OpenConfig Models ({len(openconfig_models)}):")
        print("=" * 60)
        for model in sorted(openconfig_models)[:5]:
            print(f"  - {model}")
        if len(openconfig_models) > 5:
            print(f"  ... en {len(openconfig_models) - 5} meer")
        
        print()
        print("=" * 60)
        print("SAMENVATTING:")
        print("=" * 60)
        total = len(ietf_models) + len(cisco_models) + len(openconfig_models) + len(other_models)
        print(f"Totaal aantal capabilities: {total}")
        print(f"  - IETF Models: {len(ietf_models)}")
        print(f"  - Cisco Models: {len(cisco_models)}")
        print(f"  - OpenConfig Models: {len(openconfig_models)}")
        print(f"  - Overige: {len(other_models)}")
        
        m.close_session()
        return True
        
    except Exception as e:
        print(f"FOUT: {e}")
        return False

if __name__ == "__main__":
    get_yang_capabilities()
