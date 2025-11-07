import customtkinter as ctk
from .chat_tab import ChatTab
from .settings_tab import SettingsTab
from .modules_tab import ModulesTab
from .themes import ThemeManager
from .styles import AppStyles
import threading
import time

class MainWindow(ctk.CTk):
    def __init__(self, assistant, config_manager):
        super().__init__()
        
        self.assistant = assistant
        self.config_manager = config_manager
        
        # Bezpečné načítanie nastavení s fallback
        try:
            self.settings = config_manager.load_settings()
            self.current_theme = self.settings.get("ui", {}).get("theme", "dark")
        except Exception as e:
            print(f"⚠️ Chyba pri načítaní nastavení: {e}, používam predvolené")
            self.settings = {}
            self.current_theme = "dark"
        
        self.setup_window()
        self.setup_ui()
        self.apply_theme(self.current_theme)
        
    def setup_window(self):
        """Nastaví hlavné okno s fallback hodnotami"""
        self.title("🤖 AI Assistant - Windows 10")
        
        # Fallback pre veľkosť okna
        width = self.settings.get("ui", {}).get("window_width", 1400)
        height = self.settings.get("ui", {}).get("window_height", 900)
        self.geometry(f"{width}x{height}")
        self.minsize(1200, 800)
        
        # Centrovanie okna
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
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Nastaví moderné používateľské rozhranie"""
        # Hlavný kontajner
        main_container = ctk.CTkFrame(self, fg_color=ThemeManager.get_theme(self.current_theme)["bg"])
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
        """Nastaví moderný sidebar"""
        sidebar = ctk.CTkFrame(parent, width=200, corner_radius=0)
        sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        sidebar.grid_propagate(False)
        
        # Logo/názov aplikácie
        logo_frame = ctk.CTkFrame(sidebar, fg_color="transparent", height=80)
        logo_frame.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkLabel(
            logo_frame,
            text="🤖 AI Assistant",
            font=("Segoe UI", 20, "bold"),
            text_color=ThemeManager.get_theme(self.current_theme)["accent"]
        ).pack(anchor="w")
        
        # Navigačné tlačidlá
        nav_buttons = [
            ("💬 Chat", self.show_chat),
            ("🔌 Moduly", self.show_modules),
            ("⚙️ Nastavenia", self.show_settings)
        ]
        
        for text, command in nav_buttons:
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                command=command,
                corner_radius=10,
                height=45,
                anchor="w",
                fg_color="transparent",
                text_color=ThemeManager.get_theme(self.current_theme)["text_primary"],
                hover_color=ThemeManager.get_theme(self.current_theme)["bg_tertiary"],
                font=("Segoe UI", 13)
            )
            btn.pack(fill="x", padx=10, pady=5)
        
        # Téma prepínač
        theme_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        theme_frame.pack(side="bottom", fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(theme_frame, text="Téma:", font=("Segoe UI", 12)).pack(anchor="w")
        
        theme_var = ctk.StringVar(value=self.current_theme)
        theme_dropdown = ctk.CTkOptionMenu(
            theme_frame,
            values=["dark", "light", "blue", "green"],
            variable=theme_var,
            command=self.on_theme_change,
            width=180
        )
        theme_dropdown.pack(fill="x", pady=5)
    
    def setup_main_content(self, parent):
        """Nastaví hlavný obsahový panel"""
        # Hlavný obsahový frame
        self.main_content = ctk.CTkFrame(parent, fg_color=ThemeManager.get_theme(self.current_theme)["bg_secondary"])
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        # Inicializácia záložiek
        self.chat_tab = ChatTab(self.main_content, self.assistant, self.config_manager)
        self.modules_tab = ModulesTab(self.main_content, self.assistant, self.config_manager)
        self.settings_tab = SettingsTab(self.main_content, self.config_manager)
        
        # Začiatočná záložka
        self.show_chat()
    
    def setup_status_bar(self, parent):
        """Nastaví moderný status bar"""
        status_bar = ctk.CTkFrame(parent, height=40)
        status_bar.grid(row=1, column=1, sticky="ew", padx=10, pady=(0, 10))
        status_bar.grid_propagate(False)
        
        # Stav AI
        self.ai_status = ctk.CTkLabel(
            status_bar,
            text=f"🟢 AI: {self.assistant.model_name}",
            font=("Segoe UI", 10)
        )
        self.ai_status.pack(side="left", padx=15)
        
        # Stav modulov
        modules_count = len(self.assistant.modules)
        self.modules_status = ctk.CTkLabel(
            status_bar,
            text=f"📦 {modules_count} modulov", 
            font=("Segoe UI", 10)
        )
        self.modules_status.pack(side="left", padx=15)
        
        # Stav hlasu
        self.voice_status = ctk.CTkLabel(
            status_bar,
            text="🎤 Hlas: Vypnutý",
            font=("Segoe UI", 10)
        )
        self.voice_status.pack(side="left", padx=15)
        
        # Separátor
        ctk.CTkLabel(status_bar, text="|").pack(side="left", padx=10)
        
        # Online stav
        self.online_status = ctk.CTkLabel(
            status_bar,
            text="🌐 Online",
            font=("Segoe UI", 10)
        )
        self.online_status.pack(side="left", padx=15)
        
        # Čas
        self.time_label = ctk.CTkLabel(
            status_bar,
            text="",
            font=("Segoe UI", 10)
        )
        self.time_label.pack(side="right", padx=15)
        
        # Spusti časovú slučku
        self.update_time()
    
    def update_time(self):
        """Aktualizuje čas v status bare"""
        from datetime import datetime
        current_time = datetime.now().strftime("%H:%M:%S | %d.%m.%Y")
        self.time_label.configure(text=current_time)
        self.after(1000, self.update_time)
    
    def show_chat(self):
        """Zobrazí chat záložku"""
        self.hide_all_tabs()
        self.chat_tab.pack(fill="both", expand=True)
    
    def show_modules(self):
        """Zobrazí záložku modulov"""
        self.hide_all_tabs()
        self.modules_tab.pack(fill="both", expand=True)
    
    def show_settings(self):
        """Zobrazí záložku nastavení"""
        self.hide_all_tabs()
        self.settings_tab.pack(fill="both", expand=True)
    
    def hide_all_tabs(self):
        """Skryje všetky záložky"""
        for tab in [self.chat_tab, self.modules_tab, self.settings_tab]:
            tab.pack_forget()
    
    def on_theme_change(self, theme_name):
        """Zmení tému aplikácie"""
        self.current_theme = theme_name
        self.apply_theme(theme_name)
        
        # Ulož nastavenia
        try:
            settings = self.config_manager.load_settings()
            settings["ui"]["theme"] = theme_name
            self.config_manager.save_settings(settings)
        except:
            pass
    
    def apply_theme(self, theme_name):
        """Aplikuje tému na celú aplikáciu"""
        theme = ThemeManager.apply_theme(theme_name)
        
        # Aktualizuj všetky widgety
        self._update_widget_colors(self, theme)
    
    def _update_widget_colors(self, widget, theme):
        """Rekurzívne aktualizuje farby widgetov"""
        try:
            if isinstance(widget, (ctk.CTkFrame, ctk.CTkScrollableFrame)):
                if widget.cget("fg_color") not in ["transparent", None]:
                    widget.configure(fg_color=theme["bg_secondary"])
            
            if isinstance(widget, ctk.CTkLabel):
                if widget.cget("text_color") not in [None, ""]:
                    widget.configure(text_color=theme["text_primary"])
        
        except Exception:
            pass
        
        # Rekurzívne pre deti
        for child in widget.winfo_children():
            self._update_widget_colors(child, theme)

    # ✅ PRIDANÁ METÓDA - musí byť VNÚTRI triedy
    def show_status_message(self, message, duration=3000):
        """Zobrazí dočasnú správu v status bare"""
        original_text = self.ai_status.cget("text")
        self.ai_status.configure(text=message)
        
        # Obnov pôvodný text po určitom čase
        def restore_text():
            self.ai_status.configure(text=original_text)
        
        self.after(duration, restore_text)