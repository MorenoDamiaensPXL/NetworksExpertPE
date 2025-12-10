# CSR1000v Router Configuratie Commands

## Kopieer en plak deze commands in de router console

---

## Stap 1: Basis SSH Configuratie

```
enable
configure terminal
hostname CSR1kv
ip domain-name lab.local
crypto key generate rsa modulus 2048
username cisco privilege 15 secret cisco123!
enable secret cisco123!
line vty 0 4
transport input ssh
login local
exit
ip ssh version 2
```

---

## Stap 2: NETCONF Configuratie (voor Part 4, 5, 7, 8)

```
netconf-yang
netconf ssh
```

---

## Stap 3: RESTCONF Configuratie (voor Part 6)

```
restconf
ip http secure-server
ip http authentication local
```

---

## Stap 4: Opslaan en Verifiëren

```
end
write memory
```

### Verificatie commands:

```
show ip ssh
show netconf-yang status
show running-config | section restconf
show running-config | section http
```

---

## Alle Commands in Één Blok (Copy-Paste Friendly)

```
enable
configure terminal
hostname CSR1kv
ip domain-name lab.local
crypto key generate rsa modulus 2048
username cisco privilege 15 secret cisco123!
enable secret cisco123!
line vty 0 4
transport input ssh
login local
exit
ip ssh version 2
netconf-yang
netconf ssh
restconf
ip http secure-server
ip http authentication local
end
write memory
```

---

## Inloggegevens voor Scripts

| Parameter | Waarde |
|-----------|--------|
| IP Adres | 10.176.161.43 |
| Username | cisco |
| Password | cisco123! |
| SSH Port | 22 |
| NETCONF Port | 830 |
| RESTCONF Port | 443 (HTTPS) |

---

## Test Verbindingen

### Test SSH (vanuit PowerShell):
```powershell
ssh cisco@10.176.161.43
```

### Test NETCONF (vanuit PowerShell):
```powershell
ssh -p 830 cisco@10.176.161.43 -s netconf
```

### Test RESTCONF (vanuit browser):
```
https://10.176.161.43/restconf/data/ietf-interfaces:interfaces
```
(Login met cisco / cisco123!)
