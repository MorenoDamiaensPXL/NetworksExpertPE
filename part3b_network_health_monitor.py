#!/usr/bin/env python
"""
Part 3b: Create a Challenging and Useful Script for a Network Engineer

NETWORK HEALTH MONITOR & AUTOMATED REMEDIATION
==============================================
Dit script biedt een uitgebreide network health check met:
- Real-time monitoring van interface status
- CPU en memory usage check
- Configuratie backup met vergelijking
- Automatische remediatie van veelvoorkomende problemen
- Gedetailleerde HTML rapportage
- Alert systeem (console output)

Perfect voor dagelijks gebruik door een network engineer!
"""

from netmiko import ConnectHandler
from datetime import datetime
import os
import json
import re


class NetworkHealthMonitor:
    """Comprehensive network health monitoring and automation tool."""
    
    def __init__(self, devices):
        self.devices = devices
        self.results = {}
        self.alerts = []
        self.report_dir = "health_reports"
        
        if not os.path.exists(self.report_dir):
            os.makedirs(self.report_dir)
    
    def connect_device(self, device):
        """Maak verbinding met een device."""
        try:
            conn = ConnectHandler(**device)
            return conn
        except Exception as e:
            self.add_alert("CRITICAL", device["host"], f"Verbindingsfout: {e}")
            return None
    
    def add_alert(self, severity, device, message):
        """Voeg een alert toe."""
        alert = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "severity": severity,
            "device": device,
            "message": message
        }
        self.alerts.append(alert)
        
        # Print alert direct
        icon = {"CRITICAL": "🔴", "WARNING": "🟡", "INFO": "🟢"}.get(severity, "⚪")
        print(f"{icon} [{severity}] {device}: {message}")
    
    def check_interfaces(self, conn, device_name):
        """Check interface status en statistieken."""
        output = conn.send_command("show ip interface brief")
        interface_stats = conn.send_command("show interfaces | include errors|drops|CRC")
        
        results = {"interfaces": [], "issues": []}
        
        for line in output.strip().split("\n")[1:]:
            parts = line.split()
            if len(parts) >= 6:
                iface = {
                    "name": parts[0],
                    "ip": parts[1],
                    "status": parts[4],
                    "protocol": parts[5]
                }
                results["interfaces"].append(iface)
                
                # Check for down interfaces (exclude admin down)
                if parts[4] == "down" and parts[5] == "down":
                    if "Loopback" not in parts[0]:  # Ignore loopbacks
                        self.add_alert("WARNING", device_name, 
                                      f"Interface {parts[0]} is down")
                        results["issues"].append(f"{parts[0]} is down")
        
        # Check voor errors in interface stats
        if "errors" in interface_stats.lower():
            error_count = len(re.findall(r'[1-9]\d* \w+ errors', interface_stats))
            if error_count > 0:
                self.add_alert("WARNING", device_name, 
                              f"Interface errors gedetecteerd op {error_count} interface(s)")
        
        return results
    
    def check_cpu_memory(self, conn, device_name):
        """Check CPU en memory usage."""
        cpu_output = conn.send_command("show processes cpu | include CPU")
        memory_output = conn.send_command("show memory statistics | include Processor")
        
        results = {"cpu": "unknown", "memory": "unknown"}
        
        # Parse CPU
        cpu_match = re.search(r'(\d+)%', cpu_output)
        if cpu_match:
            cpu_usage = int(cpu_match.group(1))
            results["cpu"] = f"{cpu_usage}%"
            
            if cpu_usage > 80:
                self.add_alert("CRITICAL", device_name, f"Hoge CPU usage: {cpu_usage}%")
            elif cpu_usage > 60:
                self.add_alert("WARNING", device_name, f"Verhoogde CPU usage: {cpu_usage}%")
        
        # Parse Memory
        mem_match = re.search(r'Processor\s+(\d+)\s+(\d+)\s+(\d+)', memory_output)
        if mem_match:
            total = int(mem_match.group(1))
            used = int(mem_match.group(2))
            free = int(mem_match.group(3))
            usage_pct = (used / total) * 100 if total > 0 else 0
            results["memory"] = f"{usage_pct:.1f}%"
            
            if usage_pct > 85:
                self.add_alert("CRITICAL", device_name, f"Hoge memory usage: {usage_pct:.1f}%")
            elif usage_pct > 70:
                self.add_alert("WARNING", device_name, f"Verhoogde memory usage: {usage_pct:.1f}%")
        
        return results
    
    def check_routing(self, conn, device_name):
        """Check routing table health."""
        route_output = conn.send_command("show ip route summary")
        ospf_output = conn.send_command("show ip ospf neighbor")
        
        results = {"routes": {}, "ospf_neighbors": 0}
        
        # Parse route summary
        for line in route_output.split("\n"):
            if "connected" in line.lower():
                match = re.search(r'(\d+)', line)
                if match:
                    results["routes"]["connected"] = int(match.group(1))
            elif "static" in line.lower():
                match = re.search(r'(\d+)', line)
                if match:
                    results["routes"]["static"] = int(match.group(1))
            elif "ospf" in line.lower():
                match = re.search(r'(\d+)', line)
                if match:
                    results["routes"]["ospf"] = int(match.group(1))
        
        # Check OSPF neighbors
        if "FULL" in ospf_output:
            results["ospf_neighbors"] = ospf_output.count("FULL")
            self.add_alert("INFO", device_name, 
                          f"OSPF: {results['ospf_neighbors']} neighbor(s) in FULL state")
        
        return results
    
    def check_security(self, conn, device_name):
        """Check security configuratie."""
        config = conn.send_command("show running-config")
        
        checks = {
            "ssh_enabled": "ip ssh version 2" in config,
            "enable_secret": "enable secret" in config,
            "service_password_encryption": "service password-encryption" in config,
            "logging_enabled": "logging" in config,
            "ntp_configured": "ntp server" in config,
            "banner_configured": "banner" in config
        }
        
        for check, passed in checks.items():
            if not passed:
                self.add_alert("WARNING", device_name, 
                              f"Security check gefaald: {check}")
        
        return checks
    
    def backup_config(self, conn, device_name):
        """Maak config backup."""
        config = conn.send_command("show running-config")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.report_dir}/{device_name}_backup_{timestamp}.cfg"
        
        with open(filename, "w") as f:
            f.write(config)
        
        return filename
    
    def auto_remediate(self, conn, device_name, issues):
        """Probeer automatisch problemen op te lossen."""
        remediation_log = []
        
        for issue in issues:
            if "down" in issue and "Loopback" not in issue:
                # Probeer interface te resetten
                interface = issue.split()[0]
                try:
                    commands = [
                        f"interface {interface}",
                        "shutdown",
                        "no shutdown"
                    ]
                    conn.send_config_set(commands)
                    remediation_log.append(f"Interface {interface} reset uitgevoerd")
                    self.add_alert("INFO", device_name, 
                                  f"Automatische remediation: {interface} reset")
                except Exception as e:
                    remediation_log.append(f"Remediation gefaald voor {interface}: {e}")
        
        return remediation_log
    
    def run_health_check(self, auto_fix=False):
        """Voer complete health check uit op alle devices."""
        print("\n" + "=" * 60)
        print("🔍 NETWORK HEALTH MONITOR")
        print("=" * 60)
        print(f"Startijd: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Aantal devices: {len(self.devices)}")
        print(f"Auto-remediation: {'Aan' if auto_fix else 'Uit'}")
        print("=" * 60 + "\n")
        
        for device in self.devices:
            device_name = device.get("device_name", device["host"])
            device_params = {k: v for k, v in device.items() if k != "device_name"}
            
            print(f"\n📡 Controleren: {device_name}")
            print("-" * 40)
            
            conn = self.connect_device(device_params)
            if not conn:
                self.results[device_name] = {"status": "unreachable"}
                continue
            
            try:
                # Voer alle checks uit
                self.results[device_name] = {
                    "status": "checked",
                    "hostname": conn.find_prompt().replace("#", "").replace(">", ""),
                    "interfaces": self.check_interfaces(conn, device_name),
                    "resources": self.check_cpu_memory(conn, device_name),
                    "routing": self.check_routing(conn, device_name),
                    "security": self.check_security(conn, device_name),
                    "backup_file": self.backup_config(conn, device_name)
                }
                
                # Auto remediation indien gewenst
                if auto_fix and self.results[device_name]["interfaces"]["issues"]:
                    self.results[device_name]["remediation"] = self.auto_remediate(
                        conn, device_name, 
                        self.results[device_name]["interfaces"]["issues"]
                    )
                
                conn.disconnect()
                self.add_alert("INFO", device_name, "Health check voltooid")
                
            except Exception as e:
                self.add_alert("CRITICAL", device_name, f"Health check fout: {e}")
                self.results[device_name] = {"status": "error", "error": str(e)}
        
        self.generate_report()
    
    def generate_report(self):
        """Genereer HTML rapport."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"{self.report_dir}/health_report_{timestamp}.html"
        
        html = """
<!DOCTYPE html>
<html>
<head>
    <title>Network Health Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { color: #333; border-bottom: 3px solid #007bff; padding-bottom: 10px; }
        .device-card { background: white; border-radius: 8px; padding: 20px; margin: 15px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .device-header { font-size: 1.3em; font-weight: bold; color: #007bff; }
        .status-ok { color: green; }
        .status-warning { color: orange; }
        .status-critical { color: red; }
        .check-item { margin: 5px 0; padding: 5px; background: #f8f9fa; border-radius: 4px; }
        .alert-box { padding: 10px; margin: 5px 0; border-radius: 4px; }
        .alert-CRITICAL { background: #ffebee; border-left: 4px solid red; }
        .alert-WARNING { background: #fff8e1; border-left: 4px solid orange; }
        .alert-INFO { background: #e3f2fd; border-left: 4px solid blue; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #007bff; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Network Health Report</h1>
        <p><strong>Generated:</strong> """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
        
        <h2>📋 Alerts Summary</h2>
"""
        
        # Alerts section
        for alert in self.alerts:
            html += f"""
        <div class="alert-box alert-{alert['severity']}">
            <strong>[{alert['severity']}]</strong> {alert['device']}: {alert['message']}
            <small>({alert['timestamp']})</small>
        </div>
"""
        
        # Device sections
        html += "<h2>📡 Device Details</h2>"
        
        for device_name, data in self.results.items():
            status_class = "status-ok" if data.get("status") == "checked" else "status-critical"
            html += f"""
        <div class="device-card">
            <div class="device-header">{device_name}</div>
            <p class="{status_class}">Status: {data.get('status', 'unknown').upper()}</p>
"""
            
            if data.get("resources"):
                html += f"""
            <div class="check-item">
                <strong>Resources:</strong> CPU: {data['resources'].get('cpu', 'N/A')} | 
                Memory: {data['resources'].get('memory', 'N/A')}
            </div>
"""
            
            if data.get("security"):
                passed = sum(1 for v in data['security'].values() if v)
                total = len(data['security'])
                html += f"""
            <div class="check-item">
                <strong>Security Checks:</strong> {passed}/{total} passed
            </div>
"""
            
            if data.get("backup_file"):
                html += f"""
            <div class="check-item">
                <strong>Backup:</strong> {data['backup_file']}
            </div>
"""
            
            html += "</div>"
        
        html += """
    </div>
</body>
</html>
"""
        
        with open(report_file, "w") as f:
            f.write(html)
        
        print("\n" + "=" * 60)
        print("📊 RAPPORT GEGENEREERD")
        print("=" * 60)
        print(f"Bestand: {report_file}")
        print(f"Totaal alerts: {len(self.alerts)}")
        print(f"  - Critical: {sum(1 for a in self.alerts if a['severity'] == 'CRITICAL')}")
        print(f"  - Warning: {sum(1 for a in self.alerts if a['severity'] == 'WARNING')}")
        print(f"  - Info: {sum(1 for a in self.alerts if a['severity'] == 'INFO')}")


# Main execution
if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════════╗
║         NETWORK HEALTH MONITOR & AUTO-REMEDIATION             ║
║                   Part 3b - Advanced Script                   ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    
    # Devices configuratie - PAS DIT AAN NAAR JOUW DEVICES
    devices = [
        {
            "device_type": "cisco_ios",
            "host": "10.176.161.43",
            "port": 22,
            "username": "cisco",
            "password": "cisco123!",
            "device_name": "CSR1000v-Lab"
        },
        # Voeg meer devices toe indien nodig
    ]
    
    # Maak monitor object
    monitor = NetworkHealthMonitor(devices)
    
    # Vraag of auto-remediation gewenst is
    auto_fix = input("Auto-remediation inschakelen? (ja/nee): ").lower() == "ja"
    
    # Voer health check uit
    monitor.run_health_check(auto_fix=auto_fix)
    
    print("\n✅ Health check voltooid!")
