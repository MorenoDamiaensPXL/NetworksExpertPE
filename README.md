# NetworksExpertPE

**Student:** [Jouw Naam en Voornaam]  
**Repository:** Network Programmability Expert PE  
**Datum:** December 2025

---

## Inhoudsopgave
- [Part 1: Install the Virtual Lab Environment](#part-1-install-the-virtual-lab-environment)
- [Part 2: Install the CSR1000v VM](#part-2-install-the-csr1000v-vm)
- [Part 3: Python Network Automation with NETMIKO](#part-3-python-network-automation-with-netmiko)
- [Part 4: Explore YANG Models](#part-4-explore-yang-models)
- [Part 5: Use NETCONF to Access an IOS XE Device](#part-5-use-netconf-to-access-an-ios-xe-device)
- [Part 6: Use RESTCONF to Access an IOS XE Device](#part-6-use-restconf-to-access-an-ios-xe-device)
- [Part 7: Getting Started with NETCONF/YANG – Part 1](#part-7-getting-started-with-netconfyang--part-1)
- [Part 8: Getting Started with NETCONF/YANG – Part 2](#part-8-getting-started-with-netconfyang--part-2)

---

## Part 1: Install the Virtual Lab Environment

### Task Preparation and Implementation
*[Jouw documentatie voor Part 1]*

### Task Troubleshooting
*[Eventuele problemen en oplossingen]*

### Task Verification
*[Hoe je hebt geverifieerd dat de installatie succesvol was]*

---

## Part 2: Install the CSR1000v VM

### Task Preparation and Implementation
*[Jouw documentatie voor Part 2]*

### Task Troubleshooting
*[Eventuele problemen en oplossingen]*

### Task Verification
*[Hoe je hebt geverifieerd dat de CSR1000v correct werkt]*

---

## Part 3: Python Network Automation with NETMIKO

### Task Preparation and Implementation

**Doel:** Netwerk automatisering met Python en de Netmiko library.

#### Vereisten
```bash
pip install netmiko
```

#### 3a: Connecting to an IOS-XE Device

| Script | Beschrijving |
|--------|-------------|
| `part3a_show_commands.py` | Send show commands to a single device |
| `part3a_config_commands.py` | Send configuration commands to a single device |
| `part3a_save_output.py` | Run show commands and save the output |
| `part3a_backup_config.py` | Backup device configurations to external file |
| `part3a_config_from_file.py` | Send device configuration using external file |
| `part3a_configure_interfaces.py` | Configure a subset of interfaces |
| `part3a_connect_dictionary.py` | Connect using a Python Dictionary |
| `part3a_functions_classes.py` | Script with functions and classes |
| `part3a_conditionals.py` | Script with conditional statements (if/else) |
| `part3a_multiple_devices_show.py` | Send show commands to multiple devices |
| `part3a_multiple_devices_config.py` | Send configuration commands to multiple devices |

#### Basis voorbeeld - Show Commands
```python
from netmiko import ConnectHandler

router = {
    "device_type": "cisco_ios",
    "host": "192.168.56.107",
    "username": "cisco",
    "password": "cisco123!"
}

net_connect = ConnectHandler(**router)
output = net_connect.send_command("show ip interface brief")
print(output)
net_connect.disconnect()
```

#### Configuratie voorbeeld
```python
config_commands = [
    "interface Loopback99",
    "description Created by Netmiko",
    "ip address 10.99.99.1 255.255.255.0"
]
output = net_connect.send_config_set(config_commands)
net_connect.save_config()
```

#### 3b: Challenging Script - Network Health Monitor

Zie: `part3b_network_health_monitor.py`

Dit uitgebreide script biedt:
- ✅ Real-time monitoring van interface status
- ✅ CPU en memory usage controle
- ✅ Configuratie backup met vergelijking
- ✅ Automatische remediatie van problemen
- ✅ Security compliance checks
- ✅ HTML rapportage generatie
- ✅ Alert systeem met severity levels

**Features:**
- Controleert meerdere devices tegelijk
- Detecteert down interfaces en hoge resource usage
- Kan automatisch interfaces resetten (auto-remediation)
- Genereert professionele HTML rapporten
- Slaat config backups op

### Task Troubleshooting
*[Noteer hier eventuele problemen en oplossingen]*

Veelvoorkomende problemen:
- **Connection timeout**: Controleer IP adres en SSH configuratie op router
- **Authentication failed**: Controleer username/password
- **Module not found**: Voer `pip install netmiko` uit

### Task Verification
- [ ] Netmiko geïnstalleerd (`pip install netmiko`)
- [ ] Show commands succesvol uitgevoerd
- [ ] Configuratie commands toegepast
- [ ] Output opgeslagen naar bestand
- [ ] Config backup gemaakt
- [ ] Meerdere devices geconfigureerd
- [ ] Health monitor script getest

---

## Part 4: Explore YANG Models

### Task Preparation and Implementation

**Doel:** YANG data models verkennen en begrijpen hoe ze netwerk configuratie structureren.

#### Stap 1: Installeer pyang
```bash
pip install pyang
```

#### Stap 2: Clone de YANG models repository
```bash
git clone https://github.com/YangModels/yang.git
```

#### Stap 3: Bekijk YANG model capabilities op CSR1000v
Via NETCONF kun je de ondersteunde YANG models opvragen:
```python
# Zie script: part4_yang_explorer.py
```

#### Stap 4: Converteer YANG naar tree format
```bash
pyang -f tree ietf-interfaces.yang
```

#### Belangrijke YANG concepten:
- **Container**: Groepeert gerelateerde data
- **Leaf**: Enkelvoudige waarde (string, integer, etc.)
- **List**: Verzameling van entries met een key
- **Module**: Top-level YANG bestand

### Task Troubleshooting
*[Noteer hier eventuele problemen en oplossingen]*

### Task Verification
- [ ] YANG models repository gecloned
- [ ] pyang geïnstalleerd en werkend
- [ ] Capabilities opgevraagd via NETCONF
- [ ] Tree output gegenereerd voor een YANG model

---

## Part 5: Use NETCONF to Access an IOS XE Device

### Task Preparation and Implementation

**Doel:** NETCONF gebruiken om configuratie op te halen en te wijzigen op een IOS XE device.

#### Vereisten
```bash
pip install ncclient
```

#### Script 1: NETCONF Capabilities ophalen
Zie: `part5_netconf_capabilities.py`

```python
from ncclient import manager

# Verbinding maken met router
m = manager.connect(
    host="192.168.56.107",
    port=830,
    username="cisco",
    password="cisco123!",
    hostkey_verify=False
)

# Capabilities tonen
for capability in m.server_capabilities:
    print(capability)
```

#### Script 2: Running config ophalen
Zie: `part5_netconf_get_config.py`

#### Script 3: Loopback interface toevoegen
Zie: `part5_netconf_add_loopback.py`

#### Belangrijke NETCONF operaties:
| Operatie | Beschrijving |
|----------|-------------|
| `<get>` | Haal operationele data op |
| `<get-config>` | Haal configuratie op |
| `<edit-config>` | Wijzig configuratie |
| `<copy-config>` | Kopieer configuratie |
| `<delete-config>` | Verwijder configuratie |

### Task Troubleshooting
*[Noteer hier eventuele problemen en oplossingen]*

### Task Verification
- [ ] Succesvolle NETCONF verbinding (port 830)
- [ ] Capabilities lijst ontvangen
- [ ] Running config opgehaald
- [ ] Loopback interface succesvol aangemaakt
- [ ] Configuratie geverifieerd via `show run`

---

## Part 6: Use RESTCONF to Access an IOS XE Device

### Task Preparation and Implementation

**Doel:** RESTCONF API gebruiken voor netwerk configuratie via HTTP/HTTPS.

#### Vereisten
```bash
pip install requests
```

#### RESTCONF moet enabled zijn op de router:
```
Router# configure terminal
Router(config)# restconf
Router(config)# ip http secure-server
```

#### Script 1: GET interfaces
Zie: `part6_restconf_get_interfaces.py`

```python
import requests
import json
requests.packages.urllib3.disable_warnings()

IP_ADDRESS = "192.168.56.107"
basicauth = ("cisco", "cisco123!")
headers = {
    "Accept": "application/yang-data+json",
    "Content-type": "application/yang-data+json"
}

url = f"https://{IP_ADDRESS}/restconf/data/ietf-interfaces:interfaces"
resp = requests.get(url, auth=basicauth, headers=headers, verify=False)
print(json.dumps(resp.json(), indent=4))
```

#### Script 2: PUT nieuwe loopback interface
Zie: `part6_restconf_create_loopback.py`

#### Belangrijke RESTCONF methods:
| Method | Beschrijving |
|--------|-------------|
| GET | Haal data op |
| POST | Maak nieuwe resource aan |
| PUT | Maak of vervang resource |
| PATCH | Update bestaande resource |
| DELETE | Verwijder resource |

### Task Troubleshooting
*[Noteer hier eventuele problemen en oplossingen]*

### Task Verification
- [ ] RESTCONF enabled op router
- [ ] GET request succesvol (status 200)
- [ ] Interfaces data ontvangen in JSON
- [ ] PUT request om loopback te maken (status 201/204)
- [ ] Configuratie geverifieerd via CLI

---

## Part 7: Getting Started with NETCONF/YANG – Part 1

### Task Preparation and Implementation

**Doel:** NETCONF/YANG basics begrijpen zonder Python, direct via terminal.

#### Stap 1: SSH NETCONF verbinding via terminal
```bash
ssh -p 830 cisco@192.168.56.107 -s netconf
```

Na inloggen ontvang je de `<hello>` message met capabilities.

#### Stap 2: Stuur hello bericht terug
```xml
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
```

#### Stap 3: RPC Call - Get Running Config
```xml
<?xml version="1.0"?>
<rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="101">
  <get-config>
    <source>
      <running/>
    </source>
  </get-config>
</rpc>
]]>]]>
```

#### Stap 4: RPC Call met filter
```xml
<?xml version="1.0"?>
<rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="102">
  <get-config>
    <source>
      <running/>
    </source>
    <filter type="subtree">
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
    </filter>
  </get-config>
</rpc>
]]>]]>
```

#### Belangrijke concepten:
- **Transport**: NETCONF gebruikt SSH (poort 830)
- **RPC (Remote Procedure Call)**: Vraag-antwoord communicatie
- **Capabilities**: Ondersteunde features uitgewisseld bij verbinding
- **Structured Data**: XML gebaseerde data representatie

### Task Troubleshooting
*[Noteer hier eventuele problemen en oplossingen]*

### Task Verification
- [ ] SSH NETCONF sessie geopend op poort 830
- [ ] Hello message ontvangen met capabilities
- [ ] Hello message teruggestuurd
- [ ] RPC get-config succesvol uitgevoerd
- [ ] Gefilterde response ontvangen

---

## Part 8: Getting Started with NETCONF/YANG – Part 2

### Task Preparation and Implementation

**Doel:** Werken met NCC (NETCONF Client) en Python virtual environment.

#### Stap 1: Maak Python virtual environment
```bash
python -m venv netconf-env
# Windows:
netconf-env\Scripts\activate
# Linux/Mac:
source netconf-env/bin/activate
```

#### Stap 2: Installeer ncclient
```bash
pip install ncclient lxml
```

#### Stap 3: Werken met filters
Zie: `part8_netconf_filters.py`

```python
from ncclient import manager
import xml.dom.minidom

# Filter voor alleen interfaces
INTERFACE_FILTER = """
<filter>
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
      <name/>
      <type/>
      <enabled/>
    </interface>
  </interfaces>
</filter>
"""

m = manager.connect(
    host="192.168.56.107",
    port=830,
    username="cisco",
    password="cisco123!",
    hostkey_verify=False
)

response = m.get_config(source="running", filter=INTERFACE_FILTER)
print(xml.dom.minidom.parseString(response.xml).toprettyxml())
```

#### Stap 4: Operationele data vs Configuratie data
| Type | Beschrijving | Voorbeeld |
|------|-------------|-----------|
| Configuration | Wat je configureert | Interface IP, hostname |
| Operational | Runtime statistieken | Packet counters, uptime |

```python
# Operationele data ophalen
response = m.get(filter=INTERFACE_FILTER)
```

#### Stap 5: Configuratie wijzigen
Zie: `part8_netconf_edit_config.py`

### Task Troubleshooting
*[Noteer hier eventuele problemen en oplossingen]*

### Task Verification
- [ ] Virtual environment aangemaakt en geactiveerd
- [ ] ncclient correct geïnstalleerd
- [ ] Gefilterde data opgevraagd
- [ ] Verschil begrepen tussen operational en config data
- [ ] Configuratie succesvol gewijzigd via ncclient

---

## Handige Commands Reference

### Router CLI Commands
```
show netconf-yang status
show restconf status
show running-config | section netconf
show interfaces description
```

### NETCONF SSH verbinding
```bash
ssh -p 830 username@router-ip -s netconf
```

### Python dependencies
```bash
pip install netmiko ncclient requests lxml pyang
```