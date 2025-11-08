# ui/quantum_modules_tab.py - VYLEPŠENÁ VERZIA S PRÍKAZMI
import customtkinter as ctk
from .themes import theme_manager
import os
import importlib
import threading
import subprocess
import sys

class QuantumModulesTab(ctk.CTkFrame):
    def __init__(self, parent, assistant, config_manager):
        self.theme = theme_manager.get_theme("quantum_green")
        super().__init__(parent, fg_color=self.theme["bg"], corner_radius=0, border_width=0)
        
        self.assistant = assistant
        self.config_manager = config_manager
        self.available_modules = {}
        self.installed_modules = {}
        self.expanded_modules = {}  # Sleduje rozbalené moduly
        
        self.setup_quantum_modules_ui()
        self.load_installed_modules()
        self.load_available_modules()
        self.refresh_installed_modules()
    
    def setup_quantum_modules_ui(self):
        """Vytvorí quantum modules interface"""
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Hlavný kontajner
        main_container = ctk.CTkFrame(
            self,
            fg_color=self.theme["bg"],
            corner_radius=0,
            border_width=0
        )
        main_container.grid(row=0, column=0, sticky="nsew")
        main_container.grid_rowconfigure(1, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        
        # Header
        self.setup_modules_header(main_container)
        
        # Obsah
        self.setup_modules_content(main_container)
    
    def setup_modules_header(self, parent):
        """Vytvorí header modulov"""
        header = ctk.CTkFrame(
            parent,
            height=80,
            fg_color=self.theme["bg_secondary"],
            corner_radius=0,
            border_width=0
        )
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        
        # Názov a stav
        title_frame = ctk.CTkFrame(header, fg_color="transparent", border_width=0)
        title_frame.pack(side="left", padx=30, pady=20)
        
        ctk.CTkLabel(
            title_frame,
            text="🔮 QUANTUM MODULES",
            font=("Segoe UI", 20, "bold"),
            text_color=self.theme["accent_glow"]
        ).pack(anchor="w")
        
        self.modules_status = ctk.CTkLabel(
            title_frame,
            text="Načítavam moduly...",
            font=("Consolas", 10),
            text_color=self.theme["text_secondary"]
        )
        self.modules_status.pack(anchor="w")
        
        # Rýchle akcie
        action_frame = ctk.CTkFrame(header, fg_color="transparent", border_width=0)
        action_frame.pack(side="right", padx=30, pady=20)
        
        ctk.CTkButton(
            action_frame,
            text="🔄 Obnoviť",
            command=self.refresh_modules,
            width=100,
            height=35,
            fg_color=self.theme["accent_secondary"],
            hover_color=self.theme["accent_glow"],
            font=("Segoe UI", 11)
        ).pack(side="left", padx=5)
    
    def setup_modules_content(self, parent):
        """Vytvorí obsah modulov"""
        # Notebook pre rôzne sekcie
        self.modules_notebook = ctk.CTkTabview(
            parent,
            fg_color=self.theme["bg"],
            segmented_button_fg_color=self.theme["accent_secondary"],
            segmented_button_selected_color=self.theme["accent"],
            segmented_button_selected_hover_color=self.theme["accent_glow"],
            text_color=self.theme["text_primary"]
        )
        self.modules_notebook.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        
        # Pridaj záložky
        self.installed_tab = self.modules_notebook.add("📦 Nainštalované")
        self.commands_tab = self.modules_notebook.add("📚 Príkazová príručka")  # NOVÁ ZÁLOŽKA
        self.available_tab = self.modules_notebook.add("🛒 Marketplace")
        self.creator_tab = self.modules_notebook.add("🛠️ Tvorba")
        
        self.setup_installed_tab()
        self.setup_commands_tab()  # NOVÁ METÓDA
        self.setup_marketplace_tab()
        self.setup_creator_tab()
    
    def setup_installed_tab(self):
        """Nastaví záložku s nainštalovanými modulmi"""
        # Scrollovateľný rám
        self.installed_scroll = ctk.CTkScrollableFrame(
            self.installed_tab,
            fg_color=self.theme["bg_secondary"],
            scrollbar_button_color=self.theme["accent_secondary"],
            scrollbar_button_hover_color=self.theme["accent_glow"]
        )
        self.installed_scroll.pack(fill="both", expand=True, padx=10, pady=10)
    
    def setup_commands_tab(self):
        """Nastaví záložku s príkazovou príručkou"""
        # Scrollovateľný rám
        self.commands_scroll = ctk.CTkScrollableFrame(
            self.commands_tab,
            fg_color=self.theme["bg_secondary"],
            scrollbar_button_color=self.theme["accent_secondary"],
            scrollbar_button_hover_color=self.theme["accent_glow"]
        )
        self.commands_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.refresh_commands_guide()
    
    def refresh_commands_guide(self):
        """Obnoví príkazovú príručku"""
        # Vymaž starý obsah
        for widget in self.commands_scroll.winfo_children():
            widget.destroy()
        
        if not self.installed_modules:
            ctk.CTkLabel(
                self.commands_scroll,
                text="Žiadne nainštalované moduly...",
                font=("Segoe UI", 14),
                text_color=self.theme["text_secondary"]
            ).pack(pady=50)
            return
        
        # Vytvor príručku pre každý modul
        for module_name, module_info in self.installed_modules.items():
            self.create_command_guide_card(self.commands_scroll, module_name, module_info)
    
    def create_command_guide_card(self, parent, module_name, module_info):
        """Vytvorí kartu s príkazovou príručkou pre modul"""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.theme["bg_tertiary"],
            corner_radius=15,
            border_width=2,
            border_color=self.theme["accent_secondary"]
        )
        card.pack(fill="x", pady=8, padx=5)
        
        # Hlavička karty
        header_frame = ctk.CTkFrame(card, fg_color="transparent", border_width=0)
        header_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(
            header_frame,
            text=f"📚 {module_name.upper()} - PRÍKAZOVÁ PRÍRUČKA",
            font=("Segoe UI", 16, "bold"),
            text_color=self.theme["accent_glow"]
        ).pack(side="left")
        
        # Informácie o module
        info_frame = ctk.CTkFrame(card, fg_color="transparent", border_width=0)
        info_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        description = module_info.get('description', 'Bez popisu')
        ctk.CTkLabel(
            info_frame,
            text=description,
            font=("Segoe UI", 11),
            text_color=self.theme["text_secondary"],
            wraplength=500
        ).pack(anchor="w")
        
        # Zoznam príkazov
        commands_frame = ctk.CTkFrame(card, fg_color=self.theme["bg_secondary"], corner_radius=10)
        commands_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        module_instance = module_info.get('instance')
        if module_instance and hasattr(module_instance, 'supported_commands'):
            commands = module_instance.supported_commands
            
            ctk.CTkLabel(
                commands_frame,
                text=f"Dostupné príkazy ({len(commands)}):",
                font=("Segoe UI", 12, "bold"),
                text_color=self.theme["text_primary"]
            ).pack(anchor="w", padx=10, pady=(10, 5))
            
            # Zobrazenie príkazov v stĺpcoch
            commands_text = ""
            for i, command in enumerate(sorted(commands), 1):
                commands_text += f"{i:2d}. {command}\n"
            
            commands_display = ctk.CTkTextbox(
                commands_frame,
                height=min(200, len(commands) * 15 + 30),
                font=("Consolas", 10),
                fg_color=self.theme["bg_tertiary"],
                text_color=self.theme["text_secondary"],
                wrap="none"
            )
            commands_display.pack(fill="x", padx=10, pady=(0, 10))
            commands_display.insert("1.0", commands_text)
            commands_display.configure(state="disabled")
    
    def refresh_installed_modules(self):
        """Obnoví zoznam nainštalovaných modulov"""
        print(f"🔄 Obnovujem zoznam modulov. Počet modulov: {len(self.installed_modules)}")
        
        # Vymaž starý obsah
        for widget in self.installed_scroll.winfo_children():
            widget.destroy()
        
        if not self.installed_modules:
            ctk.CTkLabel(
                self.installed_scroll,
                text="Žiadne nainštalované moduly...",
                font=("Segoe UI", 14),
                text_color=self.theme["text_secondary"]
            ).pack(pady=50)
            return
        
        # Zobraz každý modul
        for module_name, module_info in self.installed_modules.items():
            self.create_module_card(self.installed_scroll, module_name, module_info)
    
    def create_module_card(self, parent, module_name, module_info):
        """Vytvorí kartu modulu s rozbaľovacími príkazmi"""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.theme["bg_tertiary"],
            corner_radius=15,
            border_width=2,
            border_color=self.theme["accent_secondary"]
        )
        card.pack(fill="x", pady=8, padx=5)
        
        # Hlavička karty
        header_frame = ctk.CTkFrame(card, fg_color="transparent", border_width=0)
        header_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(
            header_frame,
            text=f"🔧 {module_name.upper()}",
            font=("Segoe UI", 16, "bold"),
            text_color=self.theme["accent_glow"]
        ).pack(side="left")
        
        # Tlačidlo na rozbalenie príkazov
        expand_button = ctk.CTkButton(
            header_frame,
            text="📋 Príkazy",
            command=lambda m=module_name, c=card: self.toggle_commands(m, c),
            width=80,
            height=30,
            fg_color=self.theme["accent_secondary"],
            hover_color=self.theme["accent_glow"],
            font=("Segoe UI", 10)
        )
        expand_button.pack(side="right", padx=(10, 0))
        
        status_label = ctk.CTkLabel(
            header_frame,
            text="✅ AKTÍVNY",
            font=("Consolas", 10, "bold"),
            text_color=self.theme["success"]
        )
        status_label.pack(side="right")
        
        # Informácie o module
        info_frame = ctk.CTkFrame(card, fg_color="transparent", border_width=0)
        info_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        description = module_info.get('description', 'Bez popisu')
        ctk.CTkLabel(
            info_frame,
            text=description,
            font=("Segoe UI", 11),
            text_color=self.theme["text_secondary"],
            wraplength=500
        ).pack(anchor="w")
        
        # Rám pre príkazy (na začiatku skrytý)
        self.commands_frame = ctk.CTkFrame(card, fg_color=self.theme["bg_secondary"], corner_radius=10)
        # Na začiatku je skrytý
        
        # Tlačidlá akcií
        button_frame = ctk.CTkFrame(card, fg_color="transparent", border_width=0)
        button_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkButton(
            button_frame,
            text="⚙️ Nastavenia",
            command=lambda m=module_name: self.configure_module(m),
            width=100,
            height=35,
            fg_color=self.theme["accent_secondary"],
            hover_color=self.theme["accent_glow"],
            font=("Segoe UI", 11)
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame,
            text="🔄 Reštartovať",
            command=lambda m=module_name: self.restart_module(m),
            width=100,
            height=35,
            fg_color=self.theme["accent_secondary"],
            hover_color=self.theme["accent_glow"],
            font=("Segoe UI", 11)
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame,
            text="🗑️ Odstrániť",
            command=lambda m=module_name: self.remove_module(m),
            width=100,
            height=35,
            fg_color=self.theme["error"],
            hover_color="#FF6666",
            font=("Segoe UI", 11)
        ).pack(side="right", padx=5)
    
    def toggle_commands(self, module_name, card):
        """Prepína zobrazenie príkazov pre modul"""
        # Nájdeme commands_frame v karte
        commands_frame = None
        for widget in card.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and hasattr(widget, '_commands_frame'):
                commands_frame = widget
                break
        
        if commands_frame and commands_frame.winfo_ismapped():
            # Skryť príkazy
            commands_frame.pack_forget()
        else:
            # Zobraziť príkazy
            if not commands_frame:
                # Vytvoriť nový commands_frame
                commands_frame = ctk.CTkFrame(card, fg_color=self.theme["bg_secondary"], corner_radius=10)
                commands_frame._commands_frame = True
                
                module_info = self.installed_modules.get(module_name)
                if module_info:
                    module_instance = module_info.get('instance')
                    if module_instance and hasattr(module_instance, 'supported_commands'):
                        commands = module_instance.supported_commands
                        
                        ctk.CTkLabel(
                            commands_frame,
                            text="📋 Dostupné príkazy:",
                            font=("Segoe UI", 12, "bold"),
                            text_color=self.theme["text_primary"]
                        ).pack(anchor="w", padx=10, pady=(10, 5))
                        
                        # Zobrazenie príkazov
                        commands_text = ""
                        for i, command in enumerate(sorted(commands), 1):
                            commands_text += f"{i:2d}. {command}\n"
                        
                        commands_display = ctk.CTkTextbox(
                            commands_frame,
                            height=min(150, len(commands) * 15 + 10),
                            font=("Consolas", 10),
                            fg_color=self.theme["bg_tertiary"],
                            text_color=self.theme["text_secondary"],
                            wrap="none"
                        )
                        commands_display.pack(fill="x", padx=10, pady=(0, 10))
                        commands_display.insert("1.0", commands_text)
                        commands_display.configure(state="disabled")
            
            # Umiestniť commands_frame pred button_frame
            card.winfo_children()[-2].pack_forget()  # Skryť button_frame dočasne
            commands_frame.pack(fill="x", padx=15, pady=(0, 10))
            card.winfo_children()[-1].pack(fill="x", padx=15, pady=(0, 15))  # Znovu zobraziť button_frame
    
    def setup_marketplace_tab(self):
        """Nastaví záložku s dostupnými modulmi"""
        self.marketplace_scroll = ctk.CTkScrollableFrame(
            self.available_tab,
            fg_color=self.theme["bg_secondary"],
            scrollbar_button_color=self.theme["accent_secondary"],
            scrollbar_button_hover_color=self.theme["accent_glow"]
        )
        self.marketplace_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.refresh_marketplace_modules()
    
    def refresh_marketplace_modules(self):
        """Obnoví zoznam modulov v marketplace"""
        for widget in self.marketplace_scroll.winfo_children():
            widget.destroy()
        
        if not self.available_modules:
            ctk.CTkLabel(
                self.marketplace_scroll,
                text="Žiadne dostupné moduly...",
                font=("Segoe UI", 14),
                text_color=self.theme["text_secondary"]
            ).pack(pady=50)
            return
        
        for module_id, module_info in self.available_modules.items():
            self.create_marketplace_card(self.marketplace_scroll, module_id, module_info)
    
    def create_marketplace_card(self, parent, module_id, module_info):
        """Vytvorí kartu modulu v marketplace"""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.theme["bg_tertiary"],
            corner_radius=15,
            border_width=2,
            border_color=self.theme["accent_secondary"]
        )
        card.pack(fill="x", pady=8, padx=5)
        
        # Hlavička
        header_frame = ctk.CTkFrame(card, fg_color="transparent", border_width=0)
        header_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(
            header_frame,
            text=f"🛒 {module_info['name']}",
            font=("Segoe UI", 16, "bold"),
            text_color=self.theme["accent_glow"]
        ).pack(side="left")
        
        ctk.CTkLabel(
            header_frame,
            text=f"⭐ {module_info.get('rating', '5.0')}",
            font=("Consolas", 10),
            text_color=self.theme["warning"]
        ).pack(side="right")
        
        # Popis
        ctk.CTkLabel(
            card,
            text=module_info['description'],
            font=("Segoe UI", 11),
            text_color=self.theme["text_secondary"],
            wraplength=400
        ).pack(anchor="w", padx=15, pady=(0, 10))
        
        # Detaily
        details_frame = ctk.CTkFrame(card, fg_color="transparent", border_width=0)
        details_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkLabel(
            details_frame,
            text=f"👤 {module_info['author']} | 🏷️ {module_info['version']}",
            font=("Segoe UI", 9),
            text_color=self.theme["text_secondary"]
        ).pack(side="left")
        
        install_btn = ctk.CTkButton(
            details_frame,
            text="📥 Inštalovať" if module_id not in self.installed_modules else "✅ Nainštalované",
            command=lambda mid=module_id: self.install_module(mid),
            width=100,
            height=35,
            fg_color=self.theme["accent"] if module_id not in self.installed_modules else self.theme["success"],
            hover_color=self.theme["accent_glow"],
            font=("Segoe UI", 11, "bold")
        )
        install_btn.pack(side="right")
    
    def setup_creator_tab(self):
        """Nastaví záložku pre tvorbu modulov"""
        scroll_frame = ctk.CTkScrollableFrame(
            self.creator_tab,
            fg_color=self.theme["bg_secondary"],
            scrollbar_button_color=self.theme["accent_secondary"],
            scrollbar_button_hover_color=self.theme["accent_glow"]
        )
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            scroll_frame,
            text="🛠️ QUANTUM MODULE CREATOR",
            font=("Segoe UI", 18, "bold"),
            text_color=self.theme["accent_glow"]
        ).pack(pady=10)
        
        # Formulár pre vytvorenie modulu
        form_frame = ctk.CTkFrame(
            scroll_frame,
            fg_color=self.theme["bg_tertiary"],
            corner_radius=15
        )
        form_frame.pack(fill="x", pady=10, padx=5)
        
        # Názov modulu
        ctk.CTkLabel(
            form_frame,
            text="Názov modulu:",
            font=("Segoe UI", 12, "bold"),
            text_color=self.theme["text_primary"]
        ).pack(anchor="w", padx=20, pady=(15, 5))
        
        self.creator_name = ctk.CTkEntry(
            form_frame,
            placeholder_text="napr. quantum_analyzer",
            fg_color=self.theme["bg_secondary"],
            text_color=self.theme["text_primary"],
            border_color=self.theme["accent_secondary"]
        )
        self.creator_name.pack(fill="x", padx=20, pady=5)
        
        # Popis
        ctk.CTkLabel(
            form_frame,
            text="Popis:",
            font=("Segoe UI", 12, "bold"),
            text_color=self.theme["text_primary"]
        ).pack(anchor="w", padx=20, pady=(15, 5))
        
        self.creator_description = ctk.CTkEntry(
            form_frame,
            placeholder_text="Čo tento modul robí?",
            fg_color=self.theme["bg_secondary"],
            text_color=self.theme["text_primary"],
            border_color=self.theme["accent_secondary"]
        )
        self.creator_description.pack(fill="x", padx=20, pady=5)
        
        # Príklady príkazov
        ctk.CTkLabel(
            form_frame,
            text="Príklady príkazov (oddelené čiarkou):",
            font=("Segoe UI", 12, "bold"),
            text_color=self.theme["text_primary"]
        ).pack(anchor="w", padx=20, pady=(15, 5))
        
        self.creator_commands = ctk.CTkEntry(
            form_frame,
            placeholder_text="napr. analyzuj data, spusti analyzu, vytvor report",
            fg_color=self.theme["bg_secondary"],
            text_color=self.theme["text_primary"],
            border_color=self.theme["accent_secondary"]
        )
        self.creator_commands.pack(fill="x", padx=20, pady=5)
        
        # Tlačidlo vytvoriť
        ctk.CTkButton(
            form_frame,
            text="🛠️ VYTVORIŤ QUANTUM MODUL",
            command=self.create_quantum_module,
            height=50,
            fg_color=self.theme["accent"],
            hover_color=self.theme["accent_glow"],
            font=("Segoe UI", 14, "bold"),
            corner_radius=10
        ).pack(fill="x", padx=20, pady=20)
    
    def load_installed_modules(self):
        """Načíta nainštalované moduly z assistant - OPRAVENÁ VERZIA"""
        self.installed_modules = {}
        
        print(f"🔍 Načítavam moduly z assistant...")
        
        if hasattr(self.assistant, 'modules') and self.assistant.modules:
            print(f"✅ Assistant má {len(self.assistant.modules)} modulov")
            
            for module_name, module_instance in self.assistant.modules.items():
                print(f"🔧 Spracovávam modul: {module_name}")
                
                # Získaj popis modulu
                description = getattr(module_instance, '__doc__', None)
                if not description:
                    # Ak nemá docstring, skús získať z triedy
                    description = getattr(module_instance.__class__, '__doc__', 'Bez popisu')
                
                # Ak stále nemá popis, vytvoríme základný
                if not description or description.strip() == '':
                    description = f"Modul {module_name} pre AI asistenta"
                
                self.installed_modules[module_name] = {
                    'description': description.strip(),
                    'instance': module_instance
                }
                print(f"✅ Pridaný modul: {module_name} - {description[:50]}...")
        else:
            print("❌ Assistant nemá žiadne moduly alebo atribút 'modules'")
        
        # Aktualizuj status
        module_count = len(self.installed_modules)
        status_text = f"NAČÍTANÉ: {module_count} modulov"
        status_color = self.theme["success"] if module_count > 0 else self.theme["warning"]
        
        self.modules_status.configure(
            text=status_text,
            text_color=status_color
        )
        
        print(f"🎯 Celkovo načítaných modulov: {module_count}")
    
    def load_available_modules(self):
        """Načíta dostupné moduly z marketplace"""
        self.available_modules = {
            "quantum_analyzer": {
                "name": "Quantum Analyzer",
                "description": "Pokročilá AI analýza a spracovanie dát",
                "author": "Quantum Labs",
                "version": "1.0.0",
                "rating": "4.8"
            },
            "neural_vision": {
                "name": "Neurónové Videnie", 
                "description": "Počítačové videnie a rozpoznávanie obrazu",
                "author": "AI Research",
                "version": "1.2.0",
                "rating": "4.6"
            },
            "quantum_finance": {
                "name": "Quantum Finance",
                "description": "Finančná analýza a prediktívne algoritmy",
                "author": "FinTech AI",
                "version": "2.1.0",
                "rating": "4.9"
            },
            "smart_assistant": {
                "name": "Smart Assistant", 
                "description": "Inteligentný asistent pre každodenné úlohy",
                "author": "AI Assistants",
                "version": "3.0.0", 
                "rating": "4.7"
            }
        }
    
    def refresh_modules(self):
        """Obnoví všetky moduly"""
        print("🔄 Obnovujem všetky moduly...")
        self.load_installed_modules()
        self.refresh_installed_modules()
        self.refresh_commands_guide()  # NOVÉ - obnoví príručku
        self.refresh_marketplace_modules()
        
        module_count = len(self.installed_modules)
        status_text = f"🔄 OBnovENÉ: {module_count} modulov"
        status_color = self.theme["success"] if module_count > 0 else self.theme["warning"]
        
        self.modules_status.configure(
            text=status_text,
            text_color=status_color
        )
        
        print(f"✅ Obnova dokončená. Modulov: {module_count}")
    
    def restart_module(self, module_name):
        """Reštartuje modul"""
        print(f"🔄 Reštartujem modul: {module_name}")
        # Tu by sa reštartoval skutočný modul
    
    def configure_module(self, module_name):
        """Konfiguruje modul"""
        print(f"⚙️ Konfigurujem modul: {module_name}")
        # Otvoriť konfiguračné okno pre modul
    
    def remove_module(self, module_name):
        """Odstráni modul"""
        print(f"🗑️ Odstraňujem modul: {module_name}")
        # Odstrániť modul zo systému
    
    def install_module(self, module_id):
        """Inštaluje modul"""
        module_info = self.available_modules.get(module_id)
        if module_info:
            print(f"📥 Inštalujem modul: {module_info['name']}")
            # Simulácia inštalácie
            self.installed_modules[module_id] = {
                'description': module_info['description'],
                'instance': None
            }
            self.refresh_installed_modules()
            self.refresh_commands_guide()
            self.refresh_marketplace_modules()
            print(f"✅ Modul {module_info['name']} úspešne nainštalovaný")
    
    def create_quantum_module(self):
        """Vytvorí nový modul"""
        name = self.creator_name.get().strip()
        description = self.creator_description.get().strip()
        commands_text = self.creator_commands.get().strip()
        
        if name and description:
            # Spracovať príkazy
            commands_list = []
            if commands_text:
                commands_list = [cmd.strip() for cmd in commands_text.split(',') if cmd.strip()]
            
            # Vytvoriť základný modul
            module_template = f'''
import asyncio

class {name.title().replace('_', '')}:
    """{description}"""
    
    def __init__(self):
        self.supported_commands = {commands_list if commands_list else [f"{name.lower()} príkaz", "spusti {name.lower()}", "aktivuj {name.lower()}"]}
        print(f"✅ Modul {{self.__class__.__name__}} inicializovaný")
    
    def can_handle(self, command: str) -> bool:
        return any(cmd in command.lower() for cmd in self.supported_commands)
    
    async def handle(self, command: str) -> str:
        """Spracuje príkaz pre tento modul"""
        try:
            return f"🔧 Modul {name} spracováva: {{command}}"
        except Exception as e:
            return f"❌ Chyba: {{str(e)}}"
'''
            
            # Uložiť modul
            modules_dir = "modules"
            os.makedirs(modules_dir, exist_ok=True)
            
            module_file = os.path.join(modules_dir, f"{name}.py")
            try:
                with open(module_file, 'w', encoding='utf-8') as f:
                    f.write(module_template)
                
                print(f"✅ Modul {name} bol úspešne vytvorený!")
                
                # Pridať do nainštalovaných
                self.installed_modules[name] = {
                    'description': description,
                    'file': module_file
                }
                
                self.refresh_installed_modules()
                self.refresh_commands_guide()
                
                # Vymazať formulár
                self.creator_name.delete(0, "end")
                self.creator_description.delete(0, "end")
                self.creator_commands.delete(0, "end")
                
            except Exception as e:
                print(f"❌ Chyba pri vytváraní modulu: {e}")
        else:
            print("⚠️ Prosím vyplňte aspoň názov a popis modulu")