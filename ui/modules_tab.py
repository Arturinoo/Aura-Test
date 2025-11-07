import customtkinter as ctk
import os
import importlib
import requests
import json
from typing import Dict, List
import threading
from .styles import AppStyles
from .themes import ThemeManager

class ModulesTab(ctk.CTkFrame):
    def __init__(self, parent, assistant, config_manager):
        super().__init__(parent)
        self.parent = parent
        self.assistant = assistant
        self.config_manager = config_manager
        self.current_theme = "dark"
        self.available_plugins = {}
        
        self.setup_ui()
        self.load_available_plugins()
        
    def setup_ui(self):
        """Nastaví pokročilé používateľské rozhranie pre správu modulov"""
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Hlavný notebook pre moduly
        self.notebook = ctk.CTkTabview(self)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Pridaj záložky
        self.installed_tab = self.notebook.add("📦 Nainštalované")
        self.marketplace_tab = self.notebook.add("🛒 Obchod")
        self.creator_tab = self.notebook.add("🛠️ Tvůrce")
        self.settings_tab = self.notebook.add("⚙️ Nastavenia Modulov")
        
        self.setup_installed_tab()
        self.setup_marketplace_tab()
        self.setup_creator_tab()
        self.setup_module_settings_tab()
        
    def setup_installed_tab(self):
        """Nastaví záložku s nainštalovanými modulmi"""
        # Hlavný frame
        main_frame = ctk.CTkFrame(self.installed_tab)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Nadpis
        title_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            title_frame,
            text="📦 Nainštalované Moduly",
            font=("Segoe UI", 18, "bold")
        ).pack(side="left")
        
        # Tlačidlá akcií
        button_frame = ctk.CTkFrame(title_frame, fg_color="transparent")
        button_frame.pack(side="right")
        
        refresh_btn = ctk.CTkButton(
            button_frame,
            text="🔄 Obnoviť",
            command=self.refresh_modules,
            width=100
        )
        refresh_btn.pack(side="left", padx=5)
        
        # Zoznam modulov
        self.modules_scrollable = ctk.CTkScrollableFrame(main_frame)
        self.modules_scrollable.pack(fill="both", expand=True)
        
        self.refresh_installed_modules_list()
    
    def setup_marketplace_tab(self):
        """Nastaví záložku obchodu s modulmi"""
        main_frame = ctk.CTkFrame(self.marketplace_tab)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            main_frame,
            text="🛒 Obchod s Modulmi",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=10)
        
        # Vyhľadávanie
        search_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        search_frame.pack(fill="x", pady=10)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Hľadať moduly...",
            width=300
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self.search_modules)
        
        search_btn = ctk.CTkButton(
            search_frame,
            text="🔍 Hľadať",
            command=self.search_modules
        )
        search_btn.pack(side="left")
        
        # Zoznam dostupných modulov
        self.marketplace_scrollable = ctk.CTkScrollableFrame(main_frame)
        self.marketplace_scrollable.pack(fill="both", expand=True)
        
        self.load_marketplace_modules()
    
    def setup_creator_tab(self):
        """Nastaví záložku pre tvorbu modulov"""
        main_frame = ctk.CTkScrollableFrame(self.creator_tab)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            main_frame,
            text="🛠️ Generátor Vlastných Modulov",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=10)
        
        # Formulár pre vytvorenie modulu
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(fill="x", pady=10)
        
        # Názov modulu
        ctk.CTkLabel(form_frame, text="Názov Modulu:", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.creator_name = ctk.CTkEntry(form_frame, placeholder_text="napr. weather_manager", width=300)
        self.creator_name.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        
        # Popis
        ctk.CTkLabel(form_frame, text="Popis:", font=("Segoe UI", 12, "bold")).grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.creator_description = ctk.CTkEntry(form_frame, placeholder_text="Čo tento modul robí?", width=300)
        self.creator_description.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        
        # Verzia
        ctk.CTkLabel(form_frame, text="Verzia:", font=("Segoe UI", 12, "bold")).grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.creator_version = ctk.CTkEntry(form_frame, placeholder_text="1.0.0", width=150)
        self.creator_version.insert(0, "1.0.0")
        self.creator_version.grid(row=2, column=1, sticky="w", padx=10, pady=5)
        
        # Príkazy
        ctk.CTkLabel(form_frame, text="Podporované Príkazy (jeden na riadok):", font=("Segoe UI", 12, "bold")).grid(row=3, column=0, sticky="nw", padx=10, pady=5)
        self.creator_commands = ctk.CTkTextbox(form_frame, height=100, width=300)
        self.creator_commands.grid(row=3, column=1, sticky="w", padx=10, pady=5)
        self.creator_commands.insert("1.0", "počasie\npredpoveď počasia\nteplota")
        
        # Kód modulu
        ctk.CTkLabel(form_frame, text="Python Kód Modulu:", font=("Segoe UI", 12, "bold")).grid(row=4, column=0, sticky="nw", padx=10, pady=5)
        self.creator_code = ctk.CTkTextbox(form_frame, height=200, width=300)
        self.creator_code.grid(row=4, column=1, sticky="w", padx=10, pady=5)
        
        # Ukážkový kód
        sample_code = '''import asyncio

class {class_name}:
    def __init__(self):
        self.supported_commands = {commands}
        print(f"✅ Modul {module_name} inicializovaný")
    
    def can_handle(self, command: str) -> bool:
        return any(cmd in command.lower() for cmd in self.supported_commands)
    
    async def handle(self, command: str) -> str:
        """Spracuje príkaz pre tento modul"""
        try:
            # Tu implementuj funkcionalitu
            return f"🔧 Modul {module_name} spracováva: {{command}}"
            
        except Exception as e:
            return f"❌ Chyba: {{str(e)}}"
'''
        self.creator_code.insert("1.0", sample_code)
        
        # Tlačidlá
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.grid(row=5, column=1, sticky="w", padx=10, pady=10)
        
        create_btn = ctk.CTkButton(
            button_frame,
            text="🛠️ Vytvoriť Modul",
            command=self.create_custom_module,
            height=40
        )
        create_btn.pack(side="left", padx=5)
        
        template_btn = ctk.CTkButton(
            button_frame,
            text="📝 Naplniť Šablónu",
            command=self.fill_template,
            height=40
        )
        template_btn.pack(side="left", padx=5)
    
    def setup_module_settings_tab(self):
        """Nastaví záložku nastavení modulov"""
        main_frame = ctk.CTkFrame(self.settings_tab)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            main_frame,
            text="⚙️ Nastavenia Modulov",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=10)
        
        # Globálne nastavenia modulov
        settings_frame = ctk.CTkFrame(main_frame)
        settings_frame.pack(fill="x", pady=10)
        
        self.auto_load_modules = ctk.CTkSwitch(
            settings_frame,
            text="Automaticky načítať moduly pri štarte"
        )
        self.auto_load_modules.pack(pady=5)
        self.auto_load_modules.select()
        
        self.auto_update_modules = ctk.CTkSwitch(
            settings_frame,
            text="Automaticky kontrolovať aktualizácie modulov"
        )
        self.auto_update_modules.pack(pady=5)
        
        # Uložiť nastavenia
        save_btn = ctk.CTkButton(
            main_frame,
            text="💾 Uložiť Nastavenia",
            command=self.save_module_settings,
            height=40
        )
        save_btn.pack(pady=10)
    
    def load_available_plugins(self):
        """Načíta dostupné pluginy z online repozitára"""
        # TODO: Implementovať načítanie z reálneho API
        self.available_plugins = {
            "pdf_reader": {
                "name": "PDF Čítačka",
                "description": "Čítanie a analýza PDF súborov",
                "version": "1.0.0",
                "author": "AI Assistant Team",
                "dependencies": ["PyPDF2"],
                "size": "2.1 MB",
                "rating": 4.5,
                "downloads": 150
            },
            "image_analyzer": {
                "name": "Analyzátor Obrázkov", 
                "description": "Analýza a úprava obrázkov",
                "version": "1.0.0",
                "author": "AI Assistant Team",
                "dependencies": ["Pillow"],
                "size": "1.8 MB",
                "rating": 4.2,
                "downloads": 89
            },
            "web_scraper": {
                "name": "Web Scraper",
                "description": "Sťahovanie a analýza webových stránok",
                "version": "1.0.0", 
                "author": "AI Assistant Team",
                "dependencies": ["beautifulsoup4", "requests"],
                "size": "3.2 MB",
                "rating": 4.7,
                "downloads": 210
            }
        }
    
    def refresh_installed_modules_list(self):
        """Obnoví zoznam nainštalovaných modulov"""
        # Vymaž starý zoznam
        for widget in self.modules_scrollable.winfo_children():
            widget.destroy()
        
        if not self.assistant.modules:
            ctk.CTkLabel(
                self.modules_scrollable,
                text="Žiadne moduly nie sú načítané.",
                font=("Segoe UI", 12)
            ).pack(pady=20)
            return
        
        # Pridaj každý modul do zoznamu
        for i, (module_name, module_instance) in enumerate(self.assistant.modules.items()):
            self.create_module_card(self.modules_scrollable, module_name, module_instance, i)
    
    def create_module_card(self, parent, module_name, module_instance, index):
        """Vytvorí kartu modulu pre zobrazenie"""
        card = AppStyles.create_card(parent)
        card.pack(fill="x", pady=5, padx=5)
        
        # Hlavička karty
        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=5)
        
        # Názov a stav
        ctk.CTkLabel(
            header_frame,
            text=f"📦 {module_name}",
            font=("Segoe UI", 14, "bold")
        ).pack(side="left")
        
        # Stavový indikátor
        status_label = ctk.CTkLabel(
            header_frame,
            text="✅ Aktívny",
            text_color="green",
            font=("Segoe UI", 10, "bold")
        )
        status_label.pack(side="right")
        
        # Informácie o moduly
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(fill="x", padx=10, pady=(0, 5))
        
        try:
            commands = getattr(module_instance, 'supported_commands', ["Neznáme príkazy"])
            commands_text = ", ".join(commands[:3]) + ("..." if len(commands) > 3 else "")
            ctk.CTkLabel(
                info_frame,
                text=f"Príkazy: {commands_text}",
                font=("Segoe UI", 11)
            ).pack(anchor="w")
        except:
            pass
        
        # Tlačidlá akcií
        button_frame = ctk.CTkFrame(card, fg_color="transparent")
        button_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # ctk.CTkButton(
        #     button_frame,
        #     text="⚙️ Nastavenia",
        #     width=80,
        #     command=lambda m=module_name: self.configure_module(m)
        # ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            button_frame,
            text="🔁 Reštartovať",
            width=80,
            command=lambda m=module_name: self.restart_module(m)
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            button_frame,
            text="🗑️ Odstrániť",
            width=80,
            fg_color="#e81123",
            hover_color="#a00d19",
            command=lambda m=module_name: self.remove_module(m)
        ).pack(side="left", padx=2)
    
    def load_marketplace_modules(self):
        """Načíta moduly z obchodu"""
        for widget in self.marketplace_scrollable.winfo_children():
            widget.destroy()
        
        if not self.available_plugins:
            ctk.CTkLabel(
                self.marketplace_scrollable,
                text="Žiadne moduly nie sú dostupné.",
                font=("Segoe UI", 12)
            ).pack(pady=20)
            return
        
        for plugin_id, plugin_info in self.available_plugins.items():
            self.create_marketplace_card(plugin_id, plugin_info)
    
    def create_marketplace_card(self, plugin_id, plugin_info):
        """Vytvorí kartu modulu v obchode"""
        card = AppStyles.create_card(self.marketplace_scrollable)
        card.pack(fill="x", pady=5, padx=5)
        
        # Hlavička
        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            header_frame,
            text=f"🛒 {plugin_info['name']}",
            font=("Segoe UI", 14, "bold")
        ).pack(side="left")
        
        # Hodnotenie
        rating_text = "⭐" * int(plugin_info['rating']) + "☆" * (5 - int(plugin_info['rating']))
        ctk.CTkLabel(
            header_frame,
            text=f"{rating_text} ({plugin_info['rating']})",
            font=("Segoe UI", 10)
        ).pack(side="right")
        
        # Popis
        ctk.CTkLabel(
            card,
            text=plugin_info['description'],
            font=("Segoe UI", 11),
            wraplength=600
        ).pack(anchor="w", padx=10, pady=2)
        
        # Detaily
        details_frame = ctk.CTkFrame(card, fg_color="transparent")
        details_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            details_frame,
            text=f"👤 {plugin_info['author']} | 🏷️ {plugin_info['version']} | 📦 {plugin_info['size']} | 📥 {plugin_info['downloads']}",
            font=("Segoe UI", 9)
        ).pack(side="left")
        
        # Tlačidlo inštalácie
        install_btn = ctk.CTkButton(
            details_frame,
            text="📥 Inštalovať",
            width=100,
            command=lambda pid=plugin_id: self.install_plugin(pid)
        )
        install_btn.pack(side="right")
    
    def search_modules(self, event=None):
        """Vyhľadá moduly v obchode"""
        search_term = self.search_entry.get().lower()
        
        for widget in self.marketplace_scrollable.winfo_children():
            widget.destroy()
        
        if not search_term:
            self.load_marketplace_modules()
            return
        
        filtered_plugins = {
            pid: info for pid, info in self.available_plugins.items()
            if (search_term in pid.lower() or 
                search_term in info['name'].lower() or 
                search_term in info['description'].lower())
        }
        
        if not filtered_plugins:
            ctk.CTkLabel(
                self.marketplace_scrollable,
                text="Nenašli sa žiadne moduly pre dané vyhľadávanie.",
                font=("Segoe UI", 12)
            ).pack(pady=20)
            return
        
        for plugin_id, plugin_info in filtered_plugins.items():
            self.create_marketplace_card(plugin_id, plugin_info)
    
    def create_custom_module(self):
        """Vytvorí vlastný modul"""
        name = self.creator_name.get().strip()
        description = self.creator_description.get().strip()
        version = self.creator_version.get().strip()
        commands_text = self.creator_commands.get("1.0", "end").strip()
        code = self.creator_code.get("1.0", "end").strip()
        
        if not name:
            self.show_message("❌ Zadajte názov modulu", "error")
            return
        
        if not code:
            self.show_message("❌ Zadajte kód modulu", "error")
            return
        
        # Spracuj príkazy
        commands = [cmd.strip() for cmd in commands_text.split('\n') if cmd.strip()]
        
        # Vytvor kód modulu
        class_name = name.title().replace('_', '').replace(' ', '')
        final_code = code.format(
            class_name=class_name,
            module_name=name,
            commands=commands
        )
        
        # Ulož modul
        modules_dir = "modules"
        os.makedirs(modules_dir, exist_ok=True)
        
        module_file = os.path.join(modules_dir, f"{name}.py")
        try:
            with open(module_file, 'w', encoding='utf-8') as f:
                f.write(final_code)
            
            # Skús načítať modul
            try:
                spec = importlib.util.spec_from_file_location(name, module_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Pridaj modul do asistenta
                module_class = getattr(module, class_name)
                self.assistant.modules[name] = module_class()
                
                self.show_message(f"✅ Modul '{name}' bol úspešne vytvorený a načítaný!", "success")
                self.refresh_installed_modules_list()
                
            except Exception as e:
                self.show_message(f"❌ Chyba pri načítaní modulu: {e}", "error")
                
        except Exception as e:
            self.show_message(f"❌ Chyba pri vytváraní modulu: {e}", "error")
    
    def fill_template(self):
        """Naplní šablónu kódu podľa zadaných údajov"""
        name = self.creator_name.get().strip()
        commands_text = self.creator_commands.get("1.0", "end").strip()
        
        if not name:
            self.show_message("❌ Najprv zadajte názov modulu", "error")
            return
        
        commands = [cmd.strip() for cmd in commands_text.split('\n') if cmd.strip()]
        class_name = name.title().replace('_', '').replace(' ', '')
        
        template = f'''import asyncio

class {class_name}:
    def __init__(self):
        self.supported_commands = {commands}
        print(f"✅ Modul {{self.__class__.__name__}} inicializovaný")
    
    def can_handle(self, command: str) -> bool:
        return any(cmd in command.lower() for cmd in self.supported_commands)
    
    async def handle(self, command: str) -> str:
        """Spracuje príkaz pre modul {name}"""
        try:
            # TODO: Implementuj funkcionalitu tu
            # Príklad: reaguj na špecifické príkazy
            
            if "počasie" in command.lower():
                return await self.get_weather()
            elif "teplota" in command.lower():
                return "🌡️ Teplota je 20°C"
            else:
                return f"🔧 Modul {name} spracováva príkaz: {{command}}"
            
        except Exception as e:
            return f"❌ Chyba v module {name}: {{str(e)}}"
    
    async def get_weather(self) -> str:
        """Príklad metódy pre počasie"""
        return "🌤️ Dnes je pekne, teplota 20°C"
'''
        
        self.creator_code.delete("1.0", "end")
        self.creator_code.insert("1.0", template)
        self.show_message("✅ Šablóna naplnená", "success")
    
    def install_plugin(self, plugin_id):
        """Inštaluje plugin z obchodu"""
        plugin_info = self.available_plugins.get(plugin_id)
        if not plugin_info:
            self.show_message("❌ Plugin nebol nájdený", "error")
            return
        
        self.show_message(f"📥 Inštalácia {plugin_info['name']}...", "info")
        
        # TODO: Implementovať reálnu inštaláciu
        # Momentálne len ukážka
        threading.Timer(2.0, lambda: self.show_message(
            f"✅ {plugin_info['name']} úspešne nainštalovaný!", "success"
        )).start()
    
    def remove_module(self, module_name):
        """Odstráni modul"""
        if module_name in self.assistant.modules:
            del self.assistant.modules[module_name]
            
            # Pokús sa odstrániť súbor
            module_file = f"modules/{module_name}.py"
            if os.path.exists(module_file):
                try:
                    os.remove(module_file)
                except:
                    pass
            
            self.show_message(f"✅ Modul '{module_name}' bol odstránený", "success")
            self.refresh_installed_modules_list()
        else:
            self.show_message(f"❌ Modul '{module_name}' nebol nájdený", "error")
    
    def restart_module(self, module_name):
        """Reštartuje modul"""
        if module_name in self.assistant.modules:
            module_file = f"modules/{module_name}.py"
            if os.path.exists(module_file):
                try:
                    # Znova načítaj modul
                    spec = importlib.util.spec_from_file_location(module_name, module_file)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    class_name = module_name.title().replace('_', '')
                    module_class = getattr(module, class_name)
                    self.assistant.modules[module_name] = module_class()
                    
                    self.show_message(f"✅ Modul '{module_name}' bol reštartovaný", "success")
                    self.refresh_installed_modules_list()
                    
                except Exception as e:
                    self.show_message(f"❌ Chyba pri reštartovaní modulu: {e}", "error")
            else:
                self.show_message(f"❌ Súbor modulu '{module_name}' neexistuje", "error")
        else:
            self.show_message(f"❌ Modul '{module_name}' nebol nájdený", "error")
    
    def refresh_modules(self):
        """Obnoví všetky moduly"""
        self.assistant.load_modules()
        self.refresh_installed_modules_list()
        self.show_message("✅ Všetky moduly boli obnovené", "success")
    
    def save_module_settings(self):
        """Uloží nastavenia modulov"""
        # TODO: Implementovať ukladanie nastavení
        self.show_message("✅ Nastavenia modulov uložené", "success")
    
    def show_message(self, message, message_type="info"):
        """Zobrazí správu používateľovi"""
        # Dočasné riešenie - v budúcnosti notifikácie
        print(f"{message_type.upper()}: {message}")
        
        # Mohli by sme pridať do status baru alebo vytvoriť toast notifikácie
        if hasattr(self.parent, 'parent') and hasattr(self.parent.parent, 'show_status_message'):
            self.parent.parent.show_status_message(message)

# Nová funkcia pre status messages v MainWindow