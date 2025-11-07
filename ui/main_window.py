# ui/main_window.py
import customtkinter as ctk
from .chat_tab import ChatTab
from .settings_tab import SettingsTab
from .modules_tab import ModulesTab
from .themes import AnimationManager, PurpleAuraTheme
import threading
import time
from ui.gmail_tab import GmailTab

class MainWindow(ctk.CTk):
    def __init__(self, assistant, config_manager):
        super().__init__()
        
        self.assistant = assistant
        self.config_manager = config_manager
        self.gmail_tab = None
        
        # ✅ JEDNODUCHÉ nastavenie CustomTkinter - žiadna komplexná téma
        ctk.set_appearance_mode("dark")
        
        # Načítanie nastavení
        try:
            self.settings = config_manager.load_settings()
            self.current_theme = self.settings.get("ui", {}).get("theme", "purple_aura")
        except Exception as e:
            print(f"⚠️ Chyba pri načítaní nastavení: {e}, používam PurpleAura")
            self.settings = {}
            self.current_theme = "purple_aura"
        
        self.setup_window()
        self.setup_ui()
        
        # Spustenie background animácií
        self.start_background_effects()
        
    def setup_window(self):
        """Nastaví hlavné okno s PurpleAura štýlom"""
        self.title("✨ Aura AI Assistant - PurpleAura Edition")
        
        # Veľkosť okna
        width = self.settings.get("ui", {}).get("window_width", 1400)
        height = self.settings.get("ui", {}).get("window_height", 900)
        self.geometry(f"{width}x{height}")
        self.minsize(1200, 800)
        
        # Explicitne nastavená fialová farba pozadia
        self.configure(fg_color="#2D033B")  # deep_purple
        
        # Centrovanie
        self.center_window()
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    def center_window(self):
        """Centruje okno na obrazovke"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')
    
    def setup_ui(self):
        """Nastaví moderné PurpleAura používateľské rozhranie"""
        # Hlavný kontajner - JEDNODUCHÝ bez corner_radius
        main_container = ctk.CTkFrame(
            self,
            fg_color="#2D033B"  # deep_purple
        )
        main_container.grid(row=0, column=0, sticky="nsew")
        main_container.grid_rowconfigure(1, weight=1)
        main_container.grid_columnconfigure(1, weight=1)
        
        # Sidebar
        self.setup_sidebar(main_container)
        
        # Hlavný obsah
        self.setup_main_content(main_container)
        
        # Status bar
        self.setup_status_bar(main_container)
    
    def setup_sidebar(self, parent):
        """Nastaví PurpleAura sidebar"""
        self.sidebar = ctk.CTkFrame(
            parent, 
            width=220,
            fg_color="#4C1A57"  # royal_purple
        )
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar.grid_propagate(False)
        
        # Logo
        logo_frame = ctk.CTkFrame(
            self.sidebar, 
            height=100,
            fg_color="#6A2C70"  # vibrant_purple
        )
        logo_frame.pack(fill="x", padx=0, pady=0)
        
        ctk.CTkLabel(
            logo_frame,
            text="✨ Aura AI",
            font=("Segoe UI", 22, "bold"),
            text_color="white"
        ).pack(expand=True, pady=(20, 0))
        
        ctk.CTkLabel(
            logo_frame,
            text="PurpleAura Edition",
            font=("Segoe UI", 12),
            text_color="#C191D9"  # light_lavender
        ).pack(pady=(0, 20))
        
        # Navigačné tlačidlá
        nav_buttons = [
            ("💬 AI Chat", self.show_chat, "#8100FF"),  # electric_purple
            ("📧 Gmail", self.show_gmail, "#6A2C70"),   # vibrant_purple  
            ("🔌 Moduly", self.show_modules, "#FF00FF"), # magenta
            ("⚙️ Nastavenia", self.show_settings, "#A660C9") # lavender
        ]
        
        for text, command, color in nav_buttons:
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                height=50,
                fg_color=color,
                hover_color="#C191D9",  # light_lavender
                text_color="white",
                font=("Segoe UI", 14, "bold")
            )
            btn.pack(fill="x", padx=15, pady=8)
        
        # Informácia o téme
        theme_frame = ctk.CTkFrame(
            self.sidebar, 
            fg_color="#2D033B"  # deep_purple
        )
        theme_frame.pack(side="bottom", fill="x", padx=15, pady=15)
        
        ctk.CTkLabel(
            theme_frame, 
            text="🎨 PurpleAura Téma", 
            font=("Segoe UI", 12, "bold"),
            text_color="#BC13FE"  # neon_purple
        ).pack(anchor="w", pady=(5, 0))
        
        ctk.CTkLabel(
            theme_frame,
            text="Aktívna ✨",
            font=("Segoe UI", 10),
            text_color="#C191D9"  # light_lavender
        ).pack(anchor="w", pady=(0, 5))
    
    def setup_main_content(self, parent):
        """Nastaví hlavný obsahový panel"""
        self.main_content = ctk.CTkFrame(
            parent,
            fg_color="#2D033B"  # deep_purple
        )
        self.main_content.grid(row=0, column=1, sticky="nsew")
        
        # Inicializácia záložiek
        try:
            self.chat_tab = ChatTab(self.main_content, self.assistant, self.config_manager)
            self.modules_tab = ModulesTab(self.main_content, self.assistant, self.config_manager)
            self.settings_tab = SettingsTab(self.main_content, self.config_manager)
        except Exception as e:
            print(f"⚠️ Chyba pri inicializácii záložiek: {e}")
            # Fallback záložky
            self.chat_tab = ctk.CTkFrame(self.main_content, fg_color="#2D033B")
            ctk.CTkLabel(self.chat_tab, text="💬 AI Chat Tab", text_color="white").pack(pady=20)
            
            self.modules_tab = ctk.CTkFrame(self.main_content, fg_color="#2D033B")
            ctk.CTkLabel(self.modules_tab, text="🔌 Moduly Tab", text_color="white").pack(pady=20)
            
            self.settings_tab = ctk.CTkFrame(self.main_content, fg_color="#2D033B")
            ctk.CTkLabel(self.settings_tab, text="⚙️ Nastavenia Tab", text_color="white").pack(pady=20)
        
        # Začiatočná záložka
        self.show_chat()
    
    def setup_status_bar(self, parent):
        """Nastaví PurpleAura status bar"""
        status_bar = ctk.CTkFrame(
            parent, 
            height=50,
            fg_color="#4C1A57"  # royal_purple
        )
        status_bar.grid(row=1, column=1, sticky="ew")
        status_bar.grid_propagate(False)
        
        # Stav AI
        self.ai_status = ctk.CTkLabel(
            status_bar,
            text=f"🟣 AI: {getattr(self.assistant, 'model_name', 'Unknown')}",
            font=("Segoe UI", 11, "bold"),
            text_color="#BC13FE"  # neon_purple
        )
        self.ai_status.pack(side="left", padx=20, pady=10)
        
        # Stav modulov
        modules_count = len(getattr(self.assistant, 'modules', {}))
        self.modules_status = ctk.CTkLabel(
            status_bar,
            text=f"🔮 {modules_count} modulov", 
            font=("Segoe UI", 11),
            text_color="#E0E0E0"
        )
        self.modules_status.pack(side="left", padx=20, pady=10)
        
        # Stav hlasu
        self.voice_status = ctk.CTkLabel(
            status_bar,
            text="🎤 Hlas: Vypnutý",
            font=("Segoe UI", 11),
            text_color="#E0E0E0"
        )
        self.voice_status.pack(side="left", padx=20, pady=10)
        
        # Separátor
        ctk.CTkLabel(
            status_bar, 
            text="|", 
            text_color="#A660C9"  # lavender
        ).pack(side="left", padx=10)
        
        # Online stav
        self.online_status = ctk.CTkLabel(
            status_bar,
            text="🌐 Online",
            font=("Segoe UI", 11),
            text_color="#00FF88"  # success
        )
        self.online_status.pack(side="left", padx=20, pady=10)
        
        # Čas
        self.time_label = ctk.CTkLabel(
            status_bar,
            text="",
            font=("Segoe UI", 11),
            text_color="#C191D9"  # light_lavender
        )
        self.time_label.pack(side="right", padx=20, pady=10)
        
        # Spusti časovú slučku
        self.update_time()
    
    def start_background_effects(self):
        """Spustí background animácie a efekty"""
        # Pulzujúci efekt pre AI status
        def pulse_ai_status():
            while True:
                try:
                    current_color = self.ai_status.cget("text_color")
                    if current_color == "#BC13FE":  # neon_purple
                        new_color = "#C191D9"  # light_lavender
                    else:
                        new_color = "#BC13FE"  # neon_purple
                    
                    self.ai_status.configure(text_color=new_color)
                    time.sleep(1)
                except:
                    break
        
        pulse_thread = threading.Thread(target=pulse_ai_status, daemon=True)
        pulse_thread.start()
    
    def update_time(self):
        """Aktualizuje čas"""
        from datetime import datetime
        try:
            current_time = datetime.now().strftime("%H:%M:%S | %d.%m.%Y")
            self.time_label.configure(text=f"🕒 {current_time}")
            self.after(1000, self.update_time)
        except:
            pass
    
    def show_gmail(self):
        """Zobrazí Gmail záložku"""
        self.hide_all_tabs()
        try:
            if self.gmail_tab is None:
                self.gmail_tab = GmailTab(self.main_content, self.assistant, self.config_manager)
            self.gmail_tab.pack(fill="both", expand=True)
        except Exception as e:
            print(f"⚠️ Chyba pri zobrazovaní Gmail tab: {e}")
            fallback_frame = ctk.CTkFrame(self.main_content, fg_color="#2D033B")
            ctk.CTkLabel(fallback_frame, text="📧 Gmail Tab - Dočasne nedostupné", text_color="white").pack(pady=20)
            fallback_frame.pack(fill="both", expand=True)
    
    def show_chat(self):
        """Zobrazí chat záložku"""
        self.hide_all_tabs()
        try:
            self.chat_tab.pack(fill="both", expand=True)
        except:
            fallback_frame = ctk.CTkFrame(self.main_content, fg_color="#2D033B")
            ctk.CTkLabel(fallback_frame, text="💬 Chat Tab - Dočasne nedostupné", text_color="white").pack(pady=20)
            fallback_frame.pack(fill="both", expand=True)
    
    def show_modules(self):
        """Zobrazí záložku modulov"""
        self.hide_all_tabs()
        try:
            self.modules_tab.pack(fill="both", expand=True)
        except:
            fallback_frame = ctk.CTkFrame(self.main_content, fg_color="#2D033B")
            ctk.CTkLabel(fallback_frame, text="🔌 Moduly Tab - Dočasne nedostupné", text_color="white").pack(pady=20)
            fallback_frame.pack(fill="both", expand=True)
    
    def show_settings(self):
        """Zobrazí záložku nastavení"""
        self.hide_all_tabs()
        try:
            self.settings_tab.pack(fill="both", expand=True)
        except:
            fallback_frame = ctk.CTkFrame(self.main_content, fg_color="#2D033B")
            ctk.CTkLabel(fallback_frame, text="⚙️ Nastavenia Tab - Dočasne nedostupné", text_color="white").pack(pady=20)
            fallback_frame.pack(fill="both", expand=True)
    
    def hide_all_tabs(self):
        """Skryje všetky záložky"""
        tabs_to_hide = [self.chat_tab, self.modules_tab, self.settings_tab]
        if self.gmail_tab is not None:
            tabs_to_hide.append(self.gmail_tab)
            
        for tab in tabs_to_hide:
            try:
                if hasattr(tab, 'pack_forget'):
                    tab.pack_forget()
            except:
                pass

    def show_notification(self, title, message, duration=3000):
        """Zobrazí PurpleAura notifikáciu"""
        try:
            # Vytvorenie notifikačného okna
            notification = ctk.CTkToplevel(self)
            notification.title(title)
            notification.geometry("300x100")
            notification.configure(fg_color="#2D033B")  # deep_purple
            notification.attributes("-topmost", True)
            
            # Centrovanie notifikácie
            notification.transient(self)
            notification.grab_set()
            
            x = self.winfo_x() + (self.winfo_width() // 2) - 150
            y = self.winfo_y() + (self.winfo_height() // 2) - 50
            notification.geometry(f"+{x}+{y}")
            
            # Obsah notifikácie
            ctk.CTkLabel(
                notification,
                text="✨ " + title,
                font=("Segoe UI", 14, "bold"),
                text_color="#BC13FE"  # neon_purple
            ).pack(pady=(10, 0))
            
            ctk.CTkLabel(
                notification,
                text=message,
                font=("Segoe UI", 12),
                text_color="#E0E0E0"
            ).pack(pady=5)
            
            # Automatické zatvorenie
            notification.after(duration, notification.destroy)
        except Exception as e:
            print(f"⚠️ Chyba pri zobrazovaní notifikácie: {e}")