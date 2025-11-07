import os
import platform
import psutil
import socket

class SystemTools:
    def __init__(self):
        self.supported_commands = [
            "systémové info", "informácie o systéme", "stav batérie",
            "voľné miesto", "pamäť ram", "cpu používanie", "sieťové pripojenie",
            "otvorené porty", "bežiace procesy", "systém"
        ]
        print("✅ SystemTools inicializovaný")
    
    def can_handle(self, command: str) -> bool:
        return any(cmd in command.lower() for cmd in self.supported_commands)
    
    async def handle(self, command: str) -> str:
        command_lower = command.lower()
        
        if "systémové info" in command_lower or "informácie o systéme" in command_lower:
            return self.get_system_info()
        elif "stav batérie" in command_lower:
            return self.get_battery_info()
        elif "voľné miesto" in command_lower:
            return self.get_disk_usage()
        elif "pamäť ram" in command_lower:
            return self.get_memory_info()
        elif "cpu používanie" in command_lower:
            return self.get_cpu_info()
        elif "sieťové pripojenie" in command_lower:
            return self.get_network_info()
        elif "bežiace procesy" in command_lower:
            return self.get_running_processes()
        elif "rýchlosť internetu" in command_lower:
            return "🔧 Test rýchlosti internetu momentálne nie je dostupný. Nainštalujte balík 'speedtest-cli'."
        else:
            return f"ℹ️  Príkaz '{command}' ešte nie je implementovaný v SystemTools"
    
    def get_system_info(self) -> str:
        try:
            info = f"""
🖥️ **Systémové informácie:**
- **Systém:** {platform.system()} {platform.release()}
- **Architektúra:** {platform.architecture()[0]}
- **Procesor:** {platform.processor() or 'Neznámy'}
- **Python:** {platform.python_version()}
- **Užívateľ:** {os.getlogin()}
- **Pracovný priečinok:** {os.getcwd()}
"""
            return info
        except Exception as e:
            return f"❌ Chyba pri získavaní systémových informácií: {str(e)}"
    
    def get_battery_info(self) -> str:
        try:
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                plugged = "Áno" if battery.power_plugged else "Nie"
                time_left = f"{battery.secsleft // 3600}h {(battery.secsleft % 3600) // 60}m" if battery.secsleft > 0 else "Neznámy"
                return f"🔋 **Stav batérie:** {percent}% | Zapojená: {plugged} | Zostáva: {time_left}"
            else:
                return "ℹ️  Informácie o batérii nie sú dostupné"
        except Exception as e:
            return f"❌ Chyba pri získavaní informácií o batérii: {str(e)}"
    
    def get_disk_usage(self) -> str:
        try:
            disk = psutil.disk_usage('/')
            total_gb = disk.total // (1024**3)
            used_gb = disk.used // (1024**3)
            free_gb = disk.free // (1024**3)
            percent_used = (disk.used / disk.total) * 100
            
            return f"💾 **Úložisko:**
- Celkom: {total_gb} GB
- Použité: {used_gb} GB ({percent_used:.1f}%)
- Voľné: {free_gb} GB"
        except Exception as e:
            return f"❌ Chyba pri získavaní informácií o úložisku: {str(e)}"
    
    def get_memory_info(self) -> str:
        try:
            memory = psutil.virtual_memory()
            total_gb = memory.total // (1024**3)
            used_gb = memory.used // (1024**3)
            available_gb = memory.available // (1024**3)
            percent_used = memory.percent
            
            return f"🧠 **Pamäť RAM:**
- Celkom: {total_gb} GB
- Použité: {used_gb} GB ({percent_used}%)
- Dostupné: {available_gb} GB"
        except Exception as e:
            return f"❌ Chyba pri získavaní informácií o pamäti: {str(e)}"
    
    def get_cpu_info(self) -> str:
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            info = f"⚡ **CPU:**
- Použitie: {cpu_percent}%
- Jadrá: {cpu_count}"
            if cpu_freq:
                info += f"
- Frekvencia: {cpu_freq.current:.0f} MHz"
            return info
        except Exception as e:
            return f"❌ Chyba pri získavaní informácií o CPU: {str(e)}"
    
    def get_network_info(self) -> str:
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            interfaces = psutil.net_if_addrs()
            info = f"🔌 **Sieťové informácie:**
- Hostname: {hostname}
- Lokálna IP: {local_ip}

**Aktívne rozhrania:**"
            
            for interface_name, interface_addresses in interfaces.items():
                for address in interface_addresses:
                    if str(address.family) == 'AddressFamily.AF_INET':
                        info += f"
- {interface_name}: {address.address}"
            
            return info
        except Exception as e:
            return f"❌ Chyba pri získavaní sieťových informácií: {str(e)}"
    
    def get_running_processes(self) -> str:
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Zoradiť podľa využitia pamäte
            processes.sort(key=lambda x: x['memory_percent'] or 0, reverse=True)
            
            info = "📊 **Top 5 procesov podľa pamäte:**
"
            for i, proc in enumerate(processes[:5]):
                memory = proc['memory_percent'] or 0
                info += f"{i+1}. {proc['name']} (PID: {proc['pid']}) - {memory:.1f}% RAM
"
            
            info += f"
Celkový počet procesov: {len(processes)}"
            return info
        except Exception as e:
            return f"❌ Chyba pri získavaní zoznamu procesov: {str(e)}"
