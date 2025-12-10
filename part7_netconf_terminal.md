# Part 7: Getting Started with NETCONF/YANG – Part 1

## NETCONF via Terminal (zonder Python)

### Stap 1: SSH NETCONF Verbinding

Open een terminal en maak verbinding met de router via NETCONF:

```bash
ssh -p 830 cisco@192.168.56.107 -s netconf
```

**Let op:** 
- Poort 830 is de standaard NETCONF poort
- `-s netconf` specificeert de NETCONF subsystem

### Stap 2: Hello Message

Na het inloggen ontvang je automatisch een `<hello>` bericht van de server met alle capabilities.

Je moet een hello bericht terugsturen:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
```

**Belangrijk:** Eindig altijd met `]]>]]>` als message delimiter!

### Stap 3: RPC Get Running Config

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

### Stap 4: RPC met Filter (alleen interfaces)

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

### Stap 5: RPC Get (Operational Data)

```xml
<?xml version="1.0"?>
<rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="103">
  <get>
    <filter type="subtree">
      <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
    </filter>
  </get>
</rpc>
]]>]]>
```

### Stap 6: Close Session

```xml
<?xml version="1.0"?>
<rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="999">
  <close-session/>
</rpc>
]]>]]>
```

## Belangrijke Concepten

| Concept | Beschrijving |
|---------|-------------|
| Transport | NETCONF gebruikt SSH over poort 830 |
| Hello Exchange | Client en server wisselen capabilities uit |
| RPC | Remote Procedure Call - vraag-antwoord model |
| Message-ID | Unieke identifier om responses te matchen |
| Delimiter | `]]>]]>` markeert einde van bericht |
| Filter | Beperkt de response tot specifieke data |
| get-config | Haalt configuratie data op |
| get | Haalt operationele (runtime) data op |

## Troubleshooting

### NETCONF niet beschikbaar
```
Router(config)# netconf-yang
Router(config)# netconf ssh
```

### SSH timeout
- Controleer firewall regels voor poort 830
- Controleer of SSH enabled is op de router

### Geen response na hello
- Vergeet niet de `]]>]]>` delimiter
- Controleer XML syntax
