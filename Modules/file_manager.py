import os
import shutil
from pathlib import Path
import re
from typing import List, Tuple, Dict, Any
import threading
import json
import fnmatch
from datetime import datetime
import paramiko  # pre SSH
import subprocess

class FileManager:
    def __init__(self):
        self.supported_commands = [
            # Základné operácie
            "vytvor zložku", "vytvor priečinok", "create directory", "create folder",
            "zmaž zložku", "zmaž priečinok", "delete directory", "delete folder",
            "vypíš zložku", "zoznam súborov", "list files", "list directory",
            "premenuj súbor", "premenuj zložku", "rename file", "rename folder",
            "presuň súbor", "presuň zložku", "move file", "move folder",
            "kopíruj súbor", "kopíruj zložku", "copy file", "copy folder",
            "zmaž súbor", "delete file", "odstráň súbor",
            
            # Nové operácie so súbormi
            "vytvor súbor", "create file", "vytvor dokument",
            "zapisuj do súboru", "write to file", "zapisuj do dokumentu",
            "čítaj súbor", "read file", "čítaj dokument",
            "vytvor viac súborov", "create multiple files", "vytvor hromadne súbory",
            "zapisuj hromadne", "write multiple files", "hromadný zápis",
            
            # Pokročilé operácie
            "nájdi súbor", "find file", "hľadaj súbor",
            "vyhľadaj v súboroch", "search in files", "hľadaj v dokumentoch",
            "zoznam všetkých súborov", "manifest zložky", "folder manifest",
            "veľkosť zložky", "folder size", "veľkosť priečinka",
            "zjednoť zložky", "unite folders", "skombinuj zložky",
            "kompresuj zložku", "compress folder", "zip zložku",
            
            # Sieťové operácie
            "pripoj zariadenie", "connect device", "pridaj zariadenie",
            "zoznam zariadení", "list devices", "zobraz zariadenia",
            "synchronizuj zložky", "sync folders", "synchronizácia",
            
            # UI a vyhľadávanie
            "otvor file manager", "open file browser", "správca súborov"
        ]
        
        self.connected_devices = {}
        self.search_history = []
        self.file_cache = {}
        
        print("✅ Ultimate FileManager inicializovaný")
    
    def can_handle(self, command: str) -> bool:
        return any(cmd in command.lower() for cmd in self.supported_commands)
    
    async def handle(self, command: str) -> str:
        command_lower = command.lower()
        
        try:
            # ZÁKLADNÉ OPERÁCIE
            if "vytvor zložku" in command_lower or "vytvor priečinok" in command_lower:
                return await self.create_directory(command)
            elif "zmaž zložku" in command_lower or "delete directory" in command_lower:
                return await self.delete_directory(command)
            elif "vypíš zložku" in command_lower or "list files" in command_lower:
                return self.list_directory_detailed(command)
            elif "premenuj" in command_lower or "rename" in command_lower:
                return await self.rename_item(command)
            elif "presuň" in command_lower or "move" in command_lower:
                return await self.move_item(command)
            elif "kopíruj" in command_lower or "copy" in command_lower:
                return await self.copy_item(command)
            elif "zmaž súbor" in command_lower or "delete file" in command_lower:
                return await self.delete_file(command)
            
            # NOVÉ OPERÁCIE SO SÚBORMI
            elif "vytvor súbor" in command_lower or "create file" in command_lower:
                return await self.create_file(command)
            elif "zapisuj do súboru" in command_lower or "write to file" in command_lower:
                return await self.write_to_file(command)
            elif "čítaj súbor" in command_lower or "read file" in command_lower:
                return self.read_file(command)
            elif "vytvor viac súborov" in command_lower or "create multiple files" in command_lower:
                return await self.create_multiple_files(command)
            elif "zapisuj hromadne" in command_lower or "write multiple files" in command_lower:
                return await self.write_multiple_files(command)
            
            # POKROČILÉ OPERÁCIE
            elif "nájdi súbor" in command_lower or "find file" in command_lower:
                return self.advanced_file_search(command)
            elif "vyhľadaj v súboroch" in command_lower or "search in files" in command_lower:
                return self.search_in_files(command)
            elif "zoznam všetkých súborov" in command_lower or "manifest zložky" in command_lower:
                return self.generate_comprehensive_manifest(command)
            elif "veľkosť zložky" in command_lower or "folder size" in command_lower:
                return self.get_folder_size(command)
            elif "zjednoť zložky" in command_lower or "unite folders" in command_lower:
                return await self.unite_folders(command)
            elif "kompresuj zložku" in command_lower or "compress folder" in command_lower:
                return await self.compress_folder(command)
            
            # SIETOVÉ OPERÁCIE
            elif "pripoj zariadenie" in command_lower or "connect device" in command_lower:
                return await self.connect_device(command)
            elif "zoznam zariadení" in command_lower or "list devices" in command_lower:
                return self.list_devices()
            elif "synchronizuj zložky" in command_lower or "sync folders" in command_lower:
                return await self.sync_folders(command)
            
            # UI
            elif "otvor file manager" in command_lower or "open file browser" in command_lower:
                return self.open_file_browser()
                
            else:
                return f"ℹ️  Príkaz '{command}' nie je plne implementovaný v FileManager"
                
        except Exception as e:
            return f"❌ Chyba pri vykonávaní príkazu: {str(e)}"

    # ZÁKLADNÉ OPERÁCIE (vylepšené)
    def extract_paths(self, command: str) -> List[str]:
        """Vylepšená extrakcia ciest"""
        # Regex pre Windows a Unix cesty
        path_pattern = r'[a-zA-Z]:\\(?:[^\\]+\\)*[^\\]*|/(?:[^/]+/)*[^/]*|\./\S+|\w:/\S+'
        paths = re.findall(path_pattern, command)
        
        # Extrakcia z úvodzoviek
        if not paths:
            quoted_pattern = r'["\']([^"\']+)["\']'
            paths = re.findall(quoted_pattern, command)
        
        return paths

    async def create_directory(self, command: str) -> str:
        """Vytvorí zložku"""
        paths = self.extract_paths(command)
        if not paths:
            return "❌ Nezadali ste cestu pre zložku."
        
        path = paths[0]
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            return f"✅ Zložka úspešne vytvorená: {path}"
        except Exception as e:
            return f"❌ Chyba pri vytváraní zložky: {str(e)}"

    async def create_file(self, command: str) -> str:
        """Vytvorí súbor s možným obsahom"""
        paths = self.extract_paths(command)
        if not paths:
            return "❌ Nezadali ste cestu pre súbor."
        
        path = paths[0]
        content = self.extract_content(command)
        
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content if content else "")
            
            action = "s obsahom" if content else "prázdny"
            return f"✅ Súbor úspešne vytvorený ({action}): {path}"
        except Exception as e:
            return f"❌ Chyba pri vytváraní súboru: {str(e)}"

    async def create_multiple_files(self, command: str) -> str:
        """Vytvorí viacero súborov naraz"""
        paths = self.extract_paths(command)
        if not paths:
            return "❌ Nezadali ste cestu pre súbory."
        
        base_path = paths[0]
        
        # Extrahuj mená súborov
        file_pattern = r'(\w+\.\w+)'
        file_names = re.findall(file_pattern, command)
        
        if not file_names:
            return "❌ Nezadali ste mená súborov."
        
        created = []
        for file_name in file_names:
            try:
                file_path = os.path.join(base_path, file_name)
                with open(file_path, 'w') as f:
                    f.write("")
                created.append(file_name)
            except Exception as e:
                return f"❌ Chyba pri vytváraní {file_name}: {str(e)}"
        
        return f"✅ Vytvorených {len(created)} súborov: {', '.join(created)}"

    async def write_to_file(self, command: str) -> str:
        """Zapíše do súboru"""
        paths = self.extract_paths(command)
        if not paths:
            return "❌ Nezadali ste cestu k súboru."
        
        path = paths[0]
        content = self.extract_content(command)
        
        if not content:
            return "❌ Nezadali ste obsah pre zápis."
        
        try:
            mode = 'a' if 'append' in command.lower() else 'w'
            with open(path, mode, encoding='utf-8') as f:
                f.write(content + '\n')
            
            action = "pripojený" if mode == 'a' else "prepísaný"
            return f"✅ Súbor {action}: {path}"
        except Exception as e:
            return f"❌ Chyba pri zápise: {str(e)}"

    def read_file(self, command: str) -> str:
        """Prečíta obsah súboru"""
        paths = self.extract_paths(command)
        if not paths:
            return "❌ Nezadali ste cestu k súboru."
        
        path = paths[0]
        
        try:
            if not os.path.exists(path):
                return f"❌ Súbor neexistuje: {path}"
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return f"📖 Obsah súboru {path}:\n{content}"
        except Exception as e:
            return f"❌ Chyba pri čítaní: {str(e)}"

    # POKROČILÉ VYHĽADÁVANIE
    def advanced_file_search(self, command: str) -> str:
        """Pokročilé vyhľadávanie súborov"""
        search_pattern = r'["\']([^"\']+)["\']'
        matches = re.findall(search_pattern, command)
        
        if not matches:
            return "❌ Zadajte hľadaný výraz v úvodzovkách."
        
        search_term = matches[0]
        start_path = self.extract_paths(command)
        start_path = start_path[0] if start_path else "C:\\"
        
        results = []
        try:
            for root, dirs, files in os.walk(start_path):
                for file in files:
                    if search_term.lower() in file.lower():
                        full_path = os.path.join(root, file)
                        size = os.path.getsize(full_path)
                        modified = datetime.fromtimestamp(os.path.getmtime(full_path))
                        results.append({
                            'path': full_path,
                            'size': size,
                            'modified': modified
                        })
                
                if len(results) >= 50:  # Obmedzenie výsledkov
                    break
        except Exception as e:
            return f"❌ Chyba pri vyhľadávaní: {str(e)}"
        
        if not results:
            return f"🔍 Nenašiel sa žiadny súbor obsahujúci '{search_term}'"
        
        result_text = f"🔍 Nájdených {len(results)} súborov pre '{search_term}':\n"
        for i, result in enumerate(results[:10], 1):
            result_text += f"{i}. {result['path']} ({self._format_size(result['size'])})\n"
        
        if len(results) > 10:
            result_text += f"... a ďalších {len(results) - 10} súborov"
        
        # Ulož do histórie
        self.search_history.append({
            'term': search_term,
            'results': len(results),
            'timestamp': datetime.now()
        })
        
        return result_text

    def generate_comprehensive_manifest(self, command: str) -> str:
        """Komplexný manifest zložky"""
        paths = self.extract_paths(command)
        path = paths[0] if paths else "."
        
        try:
            if not os.path.exists(path):
                return f"❌ Zložka neexistuje: {path}"
            
            file_types = {}
            total_size = 0
            file_count = 0
            
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        size = os.path.getsize(file_path)
                        total_size += size
                        file_count += 1
                        
                        # Štatistika typov súborov
                        ext = os.path.splitext(file)[1].lower()
                        file_types[ext] = file_types.get(ext, 0) + 1
                    except:
                        continue
            
            result = f"📊 KOMPLETNÝ MANIFEST: {path}\n"
            result += f"📁 Celkový počet súborov: {file_count}\n"
            result += f"💾 Celková veľkosť: {self._format_size(total_size)}\n\n"
            
            result += "📈 Štatistika typov súborov:\n"
            for ext, count in sorted(file_types.items(), key=lambda x: x[1], reverse=True)[:10]:
                result += f"  {ext or 'žiadna'}: {count} súborov\n"
            
            return result
        except Exception as e:
            return f"❌ Chyba pri generovaní manifestu: {str(e)}"

    # SIETOVÉ ZARIADENIA
    async def connect_device(self, command: str) -> str:
        """Pripojí sieťové zariadenie"""
        device_info = self.extract_device_info(command)
        
        if not device_info:
            return "❌ Zadajte údaje zariadenia: 'pripoj zariadenie názov@ip'"
        
        name, hostname, username, password = device_info
        
        try:
            # SSH pripojenie
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname, username=username, password=password)
            
            self.connected_devices[name] = {
                'ssh': ssh,
                'hostname': hostname,
                'username': username,
                'type': 'ssh'
            }
            
            return f"✅ Zariadenie '{name}' úspešne pripojené"
        except Exception as e:
            return f"❌ Chyba pri pripájaní zariadenia: {str(e)}"

    def list_devices(self) -> str:
        """Zobrazí pripojené zariadenia"""
        if not self.connected_devices:
            return "🔌 Nie sú pripojené žiadne zariadenia"
        
        result = "🔌 PRIPOJENÉ ZARIADENIA:\n"
        for name, info in self.connected_devices.items():
            result += f"📱 {name} ({info['type']}) - {info['hostname']}\n"
        
        return result

    async def sync_folders(self, command: str) -> str:
        """Synchronizuje zložky medzi zariadeniami"""
        paths = self.extract_paths(command)
        if len(paths) < 2:
            return "❌ Zadajte zdrojovú a cieľovú zložku"
        
        source, target = paths[0], paths[1]
        
        try:
            # Jednoduchá synchronizácia
            if not os.path.exists(target):
                os.makedirs(target)
            
            copied = 0
            for root, dirs, files in os.walk(source):
                for file in files:
                    src_file = os.path.join(root, file)
                    rel_path = os.path.relpath(src_file, source)
                    dst_file = os.path.join(target, rel_path)
                    
                    # Vytvor podzložky
                    os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                    
                    # Kopíruj súbor
                    shutil.copy2(src_file, dst_file)
                    copied += 1
            
            return f"✅ Synchronizovaných {copied} súborov z {source} do {target}"
        except Exception as e:
            return f"❌ Chyba pri synchronizácii: {str(e)}"

    # POMOCNÉ METÓDY
    def extract_content(self, command: str) -> str:
        """Extrahuje obsah z príkazu"""
        content_match = re.search(r'["\']([^"\']+)["\']', command)
        return content_match.group(1) if content_match else ""

    def extract_device_info(self, command: str) -> tuple:
        """Extrahuje informácie o zariadení"""
        # Formát: "pripoj zariadenie moj_pc user@192.168.1.100"
        parts = command.split()
        if len(parts) < 4:
            return None
        
        name = parts[2]
        credentials = parts[3]
        
        if '@' in credentials:
            username, hostname = credentials.split('@', 1)
            password = parts[4] if len(parts) > 4 else ""  # Jednoduché riešenie
            return (name, hostname, username, password)
        
        return None

    def _format_size(self, size_bytes: int) -> str:
        """Formátuje veľkosť súboru"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"

    def list_directory_detailed(self, command: str) -> str:
        """Detailný výpis zložky"""
        paths = self.extract_paths(command)
        path = paths[0] if paths else "."
        
        try:
            if not os.path.exists(path):
                return f"❌ Zložka neexistuje: {path}"
            
            items = os.listdir(path)
            if not items:
                return f"📁 Zložka {path} je prázdna"
            
            result = f"📁 OBSAH ZLOŽKY: {path}\n"
            result += "─" * 50 + "\n"
            
            for item in sorted(items):
                item_path = os.path.join(path, item)
                try:
                    if os.path.isdir(item_path):
                        result += f"📁 {item}/\n"
                    else:
                        size = os.path.getsize(item_path)
                        modified = datetime.fromtimestamp(os.path.getmtime(item_path))
                        result += f"📄 {item} ({self._format_size(size)}) - {modified.strftime('%d.%m.%Y %H:%M')}\n"
                except:
                    result += f"❓ {item} (prístup odmietnutý)\n"
            
            return result
        except Exception as e:
            return f"❌ Chyba pri čítaní zložky: {str(e)}"

    async def compress_folder(self, command: str) -> str:
        """Komprimuje zložku"""
        paths = self.extract_paths(command)
        if not paths:
            return "❌ Zadajte cestu k zložke"
        
        folder_path = paths[0]
        zip_path = f"{folder_path}.zip"
        
        try:
            shutil.make_archive(folder_path, 'zip', folder_path)
            return f"✅ Zložka úspešne skomprimovaná: {zip_path}"
        except Exception as e:
            return f"❌ Chyba pri kompresii: {str(e)}"

    def open_file_browser(self) -> str:
        """Otvorí grafický file manager"""
        try:
            if os.name == 'nt':  # Windows
                os.system('explorer .')
            elif os.name == 'posix':  # Linux/Mac
                os.system('nautilus .' if shutil.which('nautilus') else 'dolphin .')
            
            return "✅ File Manager otvorený"
        except Exception as e:
            return f"❌ Chyba pri otváraní File Manageru: {str(e)}"

    # Zvyšok pôvodných metód (delete_directory, rename_item, move_item, copy_item, delete_file, unite_folders, search_in_files, get_folder_size)
    # ... (zachovať pôvodnú funkcionalitu)

# UI PRE FILE MANAGER
class FileManagerUI:
    def __init__(self, file_manager):
        self.file_manager = file_manager
        self.setup_ui()
    
    def setup_ui(self):
        """Vytvorí GUI pre File Manager"""
        import customtkinter as ctk
        
        self.window = ctk.CTkToplevel()
        self.window.title("Aura File Manager")
        self.window.geometry("1200x800")
        
        # Hlavný rám
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Panel zariadení
        devices_frame = ctk.CTkFrame(main_frame, width=200)
        devices_frame.pack(side="left", fill="y", padx=(0, 10))
        
        ctk.CTkLabel(devices_frame, text="🖥️ ZARIADENIA", font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        # Zoznam zariadení
        self.devices_list = ctk.CTkTextbox(devices_frame, height=150)
        self.devices_list.pack(fill="x", padx=10, pady=5)
        
        # Vyhľadávací panel
        search_frame = ctk.CTkFrame(main_frame)
        search_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(search_frame, text="🔍 Vyhľadávanie:").pack(side="left", padx=10)
        self.search_entry = ctk.CTkEntry(search_frame, width=300)
        self.search_entry.pack(side="left", padx=5)
        
        self.search_button = ctk.CTkButton(search_frame, text="Hľadať", command=self.search_files)
        self.search_button.pack(side="left", padx=5)
        
        # Zobrazenie súborov
        self.files_text = ctk.CTkTextbox(main_frame, wrap="none")
        self.files_text.pack(fill="both", expand=True)
        
        self.refresh_devices()
        self.refresh_files()
    
    def search_files(self):
        """Spustí vyhľadávanie"""
        search_term = self.search_entry.get()
        if search_term:
            result = self.file_manager.advanced_file_search(f'nájdi súbor "{search_term}"')
            self.files_text.delete("1.0", "end")
            self.files_text.insert("1.0", result)
    
    def refresh_devices(self):
        """Obnoví zoznam zariadení"""
        devices_text = self.file_manager.list_devices()
        self.devices_list.delete("1.0", "end")
        self.devices_list.insert("1.0", devices_text)
    
    def refresh_files(self, path="."):
        """Obnoví zoznam súborov"""
        files_text = self.file_manager.list_directory_detailed(f"vypíš zložku {path}")
        self.files_text.delete("1.0", "end")
        self.files_text.insert("1.0", files_text)