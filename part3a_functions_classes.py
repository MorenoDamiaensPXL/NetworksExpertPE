#!/usr/bin/env python
"""
Part 3a: Connecting to an IOS-XE Device
Execute a script with functions and classes
"""

from netmiko import ConnectHandler
from datetime import datetime
import os


class CiscoRouter:
    """Klasse om een Cisco router te beheren via Netmiko."""
    
    def __init__(self, host, username, password, port=22, device_type="cisco_ios"):
        """Initialiseer router verbinding parameters."""
        self.device_params = {
            "device_type": device_type,
            "host": host,
            "port": port,
            "username": username,
            "password": password
        }
        self.connection = None
        self.hostname = None
    
    def connect(self):
        """Maak verbinding met de router."""
        try:
            print(f"Verbinden met {self.device_params['host']}...")
            self.connection = ConnectHandler(**self.device_params)
            self.hostname = self.connection.find_prompt().replace("#", "").replace(">", "")
            print(f"Verbonden met: {self.hostname}")
            return True
        except Exception as e:
            print(f"Verbindingsfout: {e}")
            return False
    
    def disconnect(self):
        """Sluit de verbinding."""
        if self.connection:
            self.connection.disconnect()
            print(f"Verbinding met {self.hostname} afgesloten.")
    
    def send_show_command(self, command):
        """Voer een show command uit en return de output."""
        if not self.connection:
            print("Niet verbonden!")
            return None
        return self.connection.send_command(command)
    
    def send_config_commands(self, commands):
        """Voer configuratie commands uit."""
        if not self.connection:
            print("Niet verbonden!")
            return None
        return self.connection.send_config_set(commands)
    
    def save_config(self):
        """Sla de running config op naar startup."""
        if not self.connection:
            print("Niet verbonden!")
            return False
        self.connection.save_config()
        print("Configuratie opgeslagen.")
        return True
    
    def backup_config(self, backup_dir="backups"):
        """Maak een backup van de running config."""
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        config = self.send_show_command("show running-config")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{backup_dir}/{self.hostname}_{timestamp}.cfg"
        
        with open(filename, "w") as f:
            f.write(config)
        
        print(f"Backup opgeslagen: {filename}")
        return filename
    
    def get_interfaces(self):
        """Haal interface informatie op."""
        output = self.send_show_command("show ip interface brief")
        return output
    
    def create_loopback(self, number, ip_address, mask, description=""):
        """Maak een loopback interface aan."""
        commands = [
            f"interface Loopback{number}",
            f"description {description}" if description else "description Created by script",
            f"ip address {ip_address} {mask}",
            "no shutdown"
        ]
        return self.send_config_commands(commands)


def get_device_info(router):
    """Functie om device informatie op te halen."""
    info = {
        "hostname": router.hostname,
        "version": router.send_show_command("show version | include Version"),
        "uptime": router.send_show_command("show version | include uptime"),
        "interfaces": router.get_interfaces()
    }
    return info


def display_info(info):
    """Functie om device info weer te geven."""
    print("\n" + "=" * 60)
    print(f"Device Informatie: {info['hostname']}")
    print("=" * 60)
    print(f"Version: {info['version'].strip()}")
    print(f"Uptime: {info['uptime'].strip()}")
    print("\nInterfaces:")
    print(info['interfaces'])


# Main execution
if __name__ == "__main__":
    print("=" * 60)
    print("Part 3a: Script with Functions and Classes")
    print("=" * 60)
    
    # Maak router object - PAS DIT AAN NAAR JOUW ROUTER
    router = CiscoRouter(
        host="10.176.161.43",
        username="cisco",
        password="cisco123!"
    )
    
    # Verbind
    if router.connect():
        # Haal en toon info
        info = get_device_info(router)
        display_info(info)
        
        # Maak backup
        router.backup_config()
        
        # Maak een loopback
        print("\nAanmaken Loopback interface...")
        router.create_loopback(200, "10.200.200.1", "255.255.255.0", "Created by class")
        
        # Sla op en sluit af
        router.save_config()
        router.disconnect()
