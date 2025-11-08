# ui/main_window.py - OPRAVENÁ VERZIA
import customtkinter as ctk
from .themes import theme_manager
import time
import math
import threading
import traceback

class QuantumMainWindow(ctk.CTk):
    def __init__(self, assistant, config_manager):
        # Najprv nastavíme tému pre CustomTkinter
        self.setup_ctk_theme()
        
        super().__init__()
        
        self.assistant = assistant
        self.config_manager = config_manager
        self.theme = theme_manager.get_theme("quantum_green")
        self.animation_engine = theme_manager.animation_engine
        
        # Setup quantum window
        self.setup_quantum_window()
        self.setup_quantum_ui()
        self.start_background_animations()
        
    def setup_ctk_theme(self):
        """Nastaví CustomTkinter tému aby sa predišlo chybám"""
        try:
            ctk.set_appearance_mode("dark")
            # Použijeme built-in theme aby sme sa vyhli chýbajúcim kľúčom
            ctk.set_default_color_theme("green")
        except Exception as e:
            print(f"⚠️ Chyba pri nastavovaní CTk témy: {e}")
    
    def setup_quantum_window(self):
        """Nastaví kvantové hlavné okno"""
        self.title("🌀 Aura AI - Quantum Edition")
        self.geometry("1600x1000")
        self.minsize(1400, 900)
        
        # Centrovanie
        self.center_quantum_window()
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
    def center_quantum_window(self):
        """Centruje okno s kvantovým efektom"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")
    
    def setup_quantum_ui(self):
        """Vytvorí kvantové používateľské rozhranie"""
        # Hlavný kvantový kontajner
        self.quantum_container = ctk.CTkFrame(
            self,
            fg_color=self.theme["bg"],
            corner_radius=0,
            border_width=0
        )
        self.quantum_container.grid(row=0, column=0, sticky="nsew")
        self.quantum_container.grid_rowconfigure(0, weight=1)
        self.quantum_container.grid_columnconfigure(1, weight=1)
        
        # Kvantový sidebar
        self.setup_quantum_sidebar()
        
        # Hlavný obsah
        self.setup_quantum_main_content()
        
        # Kvantový status bar
        self.setup_quantum_status_bar()
        
    def setup_quantum_sidebar(self):
        """Vytvorí kvantový sidebar s pokročilými efektmi"""
        self.sidebar = ctk.CTkFrame(
            self.quantum_container,
            width=280,
            fg_color=self.theme["bg_secondary"],
            corner_radius=0,
            border_width=0
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew", rowspan=2)
        self.sidebar.grid_propagate(False)
        
        # Kvantové logo
        self.setup_quantum_logo()
        
        # Navigačné tlačidlá s efektmi
        self.setup_quantum_navigation()
        
        # Kvantové informácie
        self.setup_quantum_info()
    
    def setup_quantum_logo(self):
        """Vytvorí animované kvantové logo"""
        logo_frame = ctk.CTkFrame(
            self.sidebar,
            height=140,
            fg_color=self.theme["bg_tertiary"],
            corner_radius=20,
            border_width=2,
            border_color=self.theme["accent_glow"]
        )
        logo_frame.pack(fill="x", padx=20, pady=20)
        logo_frame.pack_propagate(False)
        
        # Animovaný nápis
        self.quantum_logo = ctk.CTkLabel(
            logo_frame,
            text="🌀 AURA AI",
            font=("Segoe UI", 24, "bold"),
            text_color=self.theme["accent_glow"]
        )
        self.quantum_logo.pack(expand=True)
        
        self.quantum_subtitle = ctk.CTkLabel(
            logo_frame,
            text="QUANTUM EDITION",
            font=("Segoe UI", 12),
            text_color=self.theme["text_secondary"]
        )
        self.quantum_subtitle.pack(pady=(0, 20))
    
    def setup_quantum_navigation(self):
        """Vytvorí kvantovú navigáciu"""
        nav_buttons = [
            ("📊 DASHBOARD", self.show_quantum_dashboard, "quantum_dashboard"),
            ("🌌 CHAT", self.show_quantum_chat, "quantum_chat"),
            ("🔮 MODULES", self.show_quantum_modules, "quantum_modules"),
            ("⚙️ SETTINGS", self.show_quantum_settings, "quantum_settings"),
        ]
        
        for text, command, anim_id in nav_buttons:
            btn = QuantumButton(
                self.sidebar,
                text=text,
                command=command,
                height=60,
                corner_radius=15
            )
            btn.pack(fill="x", padx=20, pady=8)
    
    def setup_quantum_info(self):
        """Vytvorí kvantové informácie"""
        info_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color=self.theme["bg_tertiary"],
            corner_radius=15,
            border_width=1,
            border_color=self.theme["border"]
        )
        info_frame.pack(side="bottom", fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            info_frame,
            text="⚡ QUANTUM MODE",
            font=("Segoe UI", 12, "bold"),
            text_color=self.theme["accent_glow"]
        ).pack(pady=(10, 5))
        
        self.quantum_status = ctk.CTkLabel(
            info_frame,
            text="• SYSTEM OPTIMAL",
            font=("Consolas", 10),
            text_color=self.theme["success"]
        )
        self.quantum_status.pack(pady=(0, 10))
    
    def setup_quantum_main_content(self):
        """Vytvorí kvantový hlavný obsah"""
        self.main_content = ctk.CTkFrame(
            self.quantum_container,
            fg_color=self.theme["bg"],
            corner_radius=0,
            border_width=0
        )
        self.main_content.grid(row=0, column=1, sticky="nsew")
        
        # Inicializácia kvantových záložiek
        self.setup_quantum_tabs()
        
        # Začiatočná záložka
        self.show_quantum_dashboard()
    
    def setup_quantum_tabs(self):
        """Inicializuje kvantové záložky s podrobným error handlingom"""
        print("🔄 Inicializujem quantum tabs...")
        try:
            # Skús importovať quantum záložky s podrobným logovaním
            print("🔍 Importujem QuantumDashboardTab...")
            from .quantum_dashboard_tab import QuantumDashboardTab
            print("✅ QuantumDashboardTab importovaný")
            
            print("🔍 Importujem QuantumChatTab...")
            from .quantum_chat_tab import QuantumChatTab
            print("✅ QuantumChatTab importovaný")
            
            print("🔍 Importujem QuantumModulesTab...")
            from .quantum_modules_tab import QuantumModulesTab
            print("✅ QuantumModulesTab importovaný")
            
            print("🔍 Importujem QuantumSettingsTab...")
            from .quantum_settings_tab import QuantumSettingsTab
            print("✅ QuantumSettingsTab importovaný")
            
            print("🔄 Vytváram inštancie quantum tabov...")
            self.quantum_dashboard_tab = QuantumDashboardTab(self.main_content, self.assistant, self.config_manager)
            print("✅ QuantumDashboardTab inicializovaný")
            
            self.quantum_chat_tab = QuantumChatTab(self.main_content, self.assistant, self.config_manager)
            print("✅ QuantumChatTab inicializovaný")
            
            self.quantum_modules_tab = QuantumModulesTab(self.main_content, self.assistant, self.config_manager)
            print("✅ QuantumModulesTab inicializovaný")
            
            self.quantum_settings_tab = QuantumSettingsTab(self.main_content, self.config_manager)
            print("✅ QuantumSettingsTab inicializovaný")
            
            print("🎉 Všetky quantum tabs úspešne inicializované!")
            
        except ImportError as e:
            print(f"❌ ImportError pri quantum taboch: {e}")
            traceback.print_exc()
            self.create_enhanced_fallback_tabs()
        except Exception as e:
            print(f"❌ Chyba pri inicializácii quantum tabov: {e}")
            traceback.print_exc()
            self.create_enhanced_fallback_tabs()
    
    def create_enhanced_fallback_tabs(self):
        """Vytvorí vylepšené fallback záložky s funkčným chatom"""
        print("🔄 Vytváram vylepšené fallback tabs...")
        
        # Dashboard tab
        self.quantum_dashboard_tab = ctk.CTkFrame(
            self.main_content, 
            fg_color=self.theme["bg"],
            border_width=0
        )
        self.setup_simple_dashboard(self.quantum_dashboard_tab)
        
        # Chat tab s funkčným chatom
        self.quantum_chat_tab = ctk.CTkFrame(
            self.main_content, 
            fg_color=self.theme["bg"],
            border_width=0
        )
        self.setup_simple_chat(self.quantum_chat_tab)
        
        # Modules tab
        self.quantum_modules_tab = ctk.CTkFrame(
            self.main_content, 
            fg_color=self.theme["bg"],
            border_width=0
        )
        self.setup_simple_modules(self.quantum_modules_tab)
        
        # Settings tab
        self.quantum_settings_tab = ctk.CTkFrame(
            self.main_content, 
            fg_color=self.theme["bg"],
            border_width=0
        )
        self.setup_simple_settings(self.quantum_settings_tab)
    
    def setup_simple_dashboard(self, parent):
        """Jednoduchý fallback dashboard"""
        main_frame = ctk.CTkFrame(parent, fg_color=self.theme["bg_tertiary"], corner_radius=20)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            main_frame, 
            text="📊 QUANTUM DASHBOARD", 
            text_color=self.theme["text_primary"],
            font=("Segoe UI", 24, "bold")
        ).pack(pady=20)
        
        ctk.CTkLabel(
            main_frame,
            text="Dashboard s pokročilými widgetmi bude dostupný v plnej verzii Quantum rozhrania.",
            text_color=self.theme["text_secondary"],
            font=("Segoe UI", 14),
            wraplength=600
        ).pack(pady=10)
        
        # Jednoduché metriky
        metrics_frame = ctk.CTkFrame(main_frame, fg_color=self.theme["bg_secondary"], corner_radius=15)
        metrics_frame.pack(fill="x", padx=50, pady=20)
        
        try:
            import psutil
            cpu = psutil.cpu_percent()
            memory = psutil.virtual_memory().percent
            
            ctk.CTkLabel(
                metrics_frame,
                text=f"⚡ CPU: {cpu}%",
                font=("Segoe UI", 14),
                text_color=self.theme["accent_glow"]
            ).pack(pady=10)
            
            ctk.CTkLabel(
                metrics_frame,
                text=f"🧠 RAM: {memory}%",
                font=("Segoe UI", 14),
                text_color=self.theme["accent_glow"]
            ).pack(pady=10)
            
        except:
            ctk.CTkLabel(
                metrics_frame,
                text="Systémové metriky nie sú dostupné",
                font=("Segoe UI", 14),
                text_color=self.theme["text_secondary"]
            ).pack(pady=20)
    
    def setup_simple_chat(self, parent):
        """Vytvorí jednoduchý funkčný chat BEZ CTkScrollableFrame"""
        # Hlavný rám
        main_frame = ctk.CTkFrame(parent, fg_color=self.theme["bg_tertiary"], corner_radius=20)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Nadpis
        ctk.CTkLabel(
            main_frame, 
            text="🌌 QUANTUM CHAT", 
            text_color=self.theme["text_primary"],
            font=("Segoe UI", 24, "bold")
        ).pack(pady=20)
        
        # Jednoduchá chat oblasť - BEZ scrollovania
        chat_frame = ctk.CTkFrame(main_frame, fg_color=self.theme["bg_secondary"], corner_radius=15)
        chat_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Jednoduché textové pole pre výstup (bez scrollbaru)
        self.simple_output = ctk.CTkTextbox(
            chat_frame,
            font=("Segoe UI", 12),
            fg_color=self.theme["bg_tertiary"],
            text_color=self.theme["text_primary"],
            wrap="word",
            height=400
        )
        self.simple_output.pack(fill="both", expand=True, padx=10, pady=10)
        self.simple_output.insert("1.0", "🌀 VITAJTE V QUANTUM CHATE\n\nSom váš AI asistent, pripravený pomôcť s:\n• 🤖 AI konverzáciami\n• 📧 Email funkciami\n• 🔧 Systémovými operáciami\n• 📁 Správou súborov\n\nČo by ste chceli preskúmať?\n\n")
        
        # Vstupný rám
        input_frame = ctk.CTkFrame(chat_frame, fg_color="transparent")
        input_frame.pack(fill="x", padx=10, pady=10)
        
        # Vstupné pole
        self.chat_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Napíšte svoju správu...",
            height=40,
            font=("Segoe UI", 14),
            fg_color=self.theme["bg_tertiary"],
            border_color=self.theme["accent_secondary"]
        )
        self.chat_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.chat_entry.bind("<Return>", self.simple_send_message)
        
        # Tlačidlo odoslať
        send_btn = ctk.CTkButton(
            input_frame,
            text="🚀 Odoslať",
            command=self.simple_send_message,
            width=100,
            height=40,
            fg_color=self.theme["accent"],
            hover_color=self.theme["accent_glow"],
            font=("Segoe UI", 14, "bold")
        )
        send_btn.pack(side="right")
    
    def simple_send_message(self, event=None):
        """Jednoduché odoslanie správy v fallback chate"""
        message = self.chat_entry.get().strip()
        if not message:
            return
        
        # Pridať správu používateľa
        self.simple_output.insert("end", f"\n\nVy: {message}\n")
        self.simple_output.see("end")
        
        # Spracovať pomocou assistant
        def process_message():
            try:
                response = self.assistant.process_command_sync(message)
                self.after(0, lambda: self.display_response(response))
            except Exception as e:
                self.after(0, lambda: self.display_response(f"❌ Chyba: {str(e)}"))
        
        threading.Thread(target=process_message, daemon=True).start()
        self.chat_entry.delete(0, "end")
    
    def display_response(self, response):
        """Zobrazí odpoveď v chate"""
        self.simple_output.insert("end", f"Asistent: {response}\n")
        self.simple_output.see("end")
    
    def setup_simple_modules(self, parent):
        """Jednoduchý zoznam modulov"""
        main_frame = ctk.CTkFrame(parent, fg_color=self.theme["bg_tertiary"], corner_radius=20)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            main_frame, 
            text="🔮 AKTÍVNE MODULY", 
            text_color=self.theme["text_primary"],
            font=("Segoe UI", 24, "bold")
        ).pack(pady=20)
        
        # Zoznam modulov
        modules_frame = ctk.CTkFrame(main_frame, fg_color=self.theme["bg_secondary"], corner_radius=15)
        modules_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        if hasattr(self.assistant, 'modules') and self.assistant.modules:
            for module_name, module_instance in self.assistant.modules.items():
                module_frame = ctk.CTkFrame(modules_frame, fg_color=self.theme["bg_tertiary"], corner_radius=10)
                module_frame.pack(fill="x", padx=10, pady=5)
                
                ctk.CTkLabel(
                    module_frame,
                    text=f"🔧 {module_name.upper()}",
                    font=("Segoe UI", 14, "bold"),
                    text_color=self.theme["accent_glow"]
                ).pack(anchor="w", padx=10, pady=5)
                
                # Získať popis modulu
                description = getattr(module_instance, '__doc__', 'Bez popisu') or 'Bez popisu'
                ctk.CTkLabel(
                    module_frame,
                    text=description,
                    font=("Segoe UI", 11),
                    text_color=self.theme["text_secondary"],
                    wraplength=600
                ).pack(anchor="w", padx=10, pady=(0, 5))
        else:
            ctk.CTkLabel(
                modules_frame,
                text="Žiadne načítané moduly",
                font=("Segoe UI", 14),
                text_color=self.theme["text_secondary"]
            ).pack(pady=20)
    
    def setup_simple_settings(self, parent):
        """Jednoduché nastavenia"""
        main_frame = ctk.CTkFrame(parent, fg_color=self.theme["bg_tertiary"], corner_radius=20)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            main_frame, 
            text="⚙️ KONFIGURÁCIA", 
            text_color=self.theme["text_primary"],
            font=("Segoe UI", 24, "bold")
        ).pack(pady=20)
        
        settings_frame = ctk.CTkFrame(main_frame, fg_color=self.theme["bg_secondary"], corner_radius=15)
        settings_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Jednoduché nastavenia
        settings_data = [
            ("🤖 AI Model", getattr(self.assistant, 'model_name', 'qwen3')),
            ("🎤 Hlasová aktivácia", "Dostupná" if hasattr(self.assistant, 'voice_engine') and self.assistant.voice_engine else "Nedostupná"),
            ("🔧 Načítané moduly", str(len(getattr(self.assistant, 'modules', {})))),
            ("🌐 AI Stav", "Pripojené" if hasattr(self.assistant, 'model_name') else "Nepripojené")
        ]
        
        for setting, value in settings_data:
            frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
            frame.pack(fill="x", padx=20, pady=10)
            
            ctk.CTkLabel(
                frame,
                text=setting,
                font=("Segoe UI", 14, "bold"),
                text_color=self.theme["text_primary"]
            ).pack(side="left")
            
            ctk.CTkLabel(
                frame,
                text=value,
                font=("Segoe UI", 14),
                text_color=self.theme["accent_glow"]
            ).pack(side="right")
    
    def setup_quantum_status_bar(self):
        """Vytvorí kvantový status bar"""
        status_bar = ctk.CTkFrame(
            self.quantum_container,
            height=60,
            fg_color=self.theme["bg_secondary"],
            corner_radius=0,
            border_width=0
        )
        status_bar.grid(row=1, column=1, sticky="ew")
        status_bar.grid_propagate(False)
        
        # Stavové indikátory
        status_items = [
            ("📊 DASHBOARD", "Live Metrics", "dashboard_status"),
            ("🤖 AI", f"Model: {getattr(self.assistant, 'model_name', 'Quantum')}", "ai_status"),
            ("🔮 MODULES", f"Aktívne: {len(getattr(self.assistant, 'modules', {}))}", "modules_status"),
            ("🎤 VOICE", "Quantum Ready", "voice_status"),
        ]
        
        status_frame = ctk.CTkFrame(status_bar, fg_color="transparent")
        status_frame.pack(side="left", padx=20)
        
        for icon, text, anim_id in status_items:
            frame = ctk.CTkFrame(status_frame, fg_color="transparent", border_width=0)
            frame.pack(side="left", padx=15)
            
            label = ctk.CTkLabel(
                frame,
                text=f"{icon} {text}",
                font=("Consolas", 11),
                text_color=self.theme["text_secondary"]
            )
            label.pack(pady=10)
    
    def start_background_animations(self):
        """Spustí pozadie animácií"""
        # Spusti pulzovanie loga
        self.animate_logo_pulse()
        
        # Spusti systémovú štatistiku
        self.update_system_stats()
    
    def animate_logo_pulse(self):
        """Animácia pulzovania loga"""
        def pulse():
            try:
                current_font = self.quantum_logo.cget("font")
                if isinstance(current_font, tuple):
                    current_size = current_font[1]
                else:
                    current_size = 24
                
                new_size = 24 + math.sin(time.time() * 2) * 2
                self.quantum_logo.configure(
                    font=("Segoe UI", int(new_size), "bold")
                )
            except:
                pass
            self.after(100, pulse)
        
        pulse()
    
    def update_system_stats(self):
        """Aktualizuje systémové štatistiky"""
        def update():
            try:
                import psutil
                cpu = psutil.cpu_percent()
                memory = psutil.virtual_memory().percent
                
                stats_text = f"• CPU: {cpu}% | MEM: {memory}%"
                self.quantum_status.configure(text=stats_text)
                
                # Zmeň farbu podľa zaťaženia
                if cpu > 80 or memory > 80:
                    self.quantum_status.configure(text_color=self.theme["warning"])
                else:
                    self.quantum_status.configure(text_color=self.theme["success"])
                    
            except:
                # Fallback ak psutil nie je dostupný
                current_time = time.strftime("%H:%M:%S")
                self.quantum_status.configure(text=f"• System Time: {current_time}")
            
            self.after(2000, update)
        
        update()
    
    def show_quantum_dashboard(self):
        """Zobrazí kvantový dashboard"""
        self.hide_all_quantum_tabs()
        try:
            self.quantum_dashboard_tab.pack(fill="both", expand=True)
        except Exception as e:
            print(f"Error showing dashboard tab: {e}")
            self.show_error_message("Dashboard", e)
    
    def show_quantum_chat(self):
        """Zobrazí kvantový chat"""
        self.hide_all_quantum_tabs()
        try:
            self.quantum_chat_tab.pack(fill="both", expand=True)
        except Exception as e:
            print(f"Error showing chat tab: {e}")
            self.show_error_message("Chat", e)
    
    def show_quantum_modules(self):
        """Zobrazí kvantové moduly"""
        self.hide_all_quantum_tabs()
        try:
            self.quantum_modules_tab.pack(fill="both", expand=True)
        except Exception as e:
            print(f"Error showing modules tab: {e}")
            self.show_error_message("Modules", e)
    
    def show_quantum_settings(self):
        """Zobrazí kvantové nastavenia"""
        self.hide_all_quantum_tabs()
        try:
            self.quantum_settings_tab.pack(fill="both", expand=True)
        except Exception as e:
            print(f"Error showing settings tab: {e}")
            self.show_error_message("Settings", e)
    
    def hide_all_quantum_tabs(self):
        """Skryje všetky kvantové záložky"""
        tabs = [self.quantum_dashboard_tab, self.quantum_chat_tab, self.quantum_modules_tab, 
                self.quantum_settings_tab]
        for tab in tabs:
            try:
                tab.pack_forget()
            except:
                pass
    
    def show_error_message(self, tab_name, error):
        """Zobrazí chybovú správu pre záložku"""
        error_frame = ctk.CTkFrame(
            self.main_content,
            fg_color=self.theme["bg_tertiary"],
            corner_radius=20,
            border_width=2,
            border_color=self.theme["error"]
        )
        error_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            error_frame,
            text=f"⚠️ {tab_name.upper()} ERROR",
            font=("Segoe UI", 24, "bold"),
            text_color=self.theme["error"]
        ).pack(pady=50)
        
        ctk.CTkLabel(
            error_frame,
            text=f"Unable to load {tab_name} tab:\n{str(error)}",
            text_color=self.theme["text_secondary"],
            font=("Segoe UI", 14),
            justify="center"
        ).pack(pady=10)

class QuantumButton(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        self.quantum_colors = theme_manager.get_theme("quantum_green")
        super().__init__(
            master,
            fg_color=self.quantum_colors["accent_secondary"],
            hover_color=self.quantum_colors["accent_glow"],
            text_color=self.quantum_colors["text_primary"],
            border_color=self.quantum_colors["accent_glow"],
            border_width=2,
            font=("Segoe UI", 14, "bold"),
            **kwargs
        )