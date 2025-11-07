# ui/gmail_tab.py
import customtkinter as ctk
from .themes import GreenAuraTheme, AnimationManager  # ✅ Zmena na GreenAuraTheme
import requests
import json

class GmailTab(ctk.CTkFrame):
    def __init__(self, parent, assistant=None, config_manager=None):
        super().__init__(parent)
        
        self.assistant = assistant
        self.config_manager = config_manager
        self.current_emails = []
        
        # Získanie témy
        try:
            settings = config_manager.load_settings() if config_manager else {}
            self.current_theme = settings.get("ui", {}).get("theme", "green_aura")  # ✅ Zmena na green_aura
        except:
            self.current_theme = "green_aura"  # ✅ Zmena na green_aura
            
        self.init_ui()
        
    def init_ui(self):
        """Inicializuje GreenAura Gmail rozhranie - OPRAVENÁ VERZIA"""
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Získaj tému
        theme = GreenAuraTheme.get_theme(self.current_theme)
        
        # Hlavný kontajner s GreenAura štýlom
        main_container = ctk.CTkFrame(
            self, 
            fg_color=theme["bg_secondary"],
            corner_radius=20
        )
        main_container.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        main_container.grid_rowconfigure(1, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        
        # Header s efektom
        header_frame = ctk.CTkFrame(
            main_container,
            fg_color=theme["accent"],
            height=80,
            corner_radius=15
        )
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        header_frame.grid_propagate(False)
        
        ctk.CTkLabel(
            header_frame,
            text="📧 Gmail Manager",
            font=("Segoe UI", 20, "bold"),
            text_color=theme["text_primary"]
        ).pack(side="left", padx=20, pady=20)
        
        self.connection_status = ctk.CTkLabel(
            header_frame,
            text="🔮 Kontrolujem spojenie...",
            font=("Segoe UI", 14),
            text_color=theme["text_accent"]
        )
        self.connection_status.pack(side="right", padx=20, pady=20)
        
        # Tlačidlá s GreenAura efektmi
        button_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        button_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        # Hlavné tlačidlá
        btn_connect = ctk.CTkButton(
            button_frame,
            text="🔗 Pripojiť Gmail",
            command=self.connect_gmail,
            height=50,
            fg_color=theme["accent"],
            hover_color=theme["accent_secondary"],
            font=("Segoe UI", 14, "bold"),
            corner_radius=12
        )
        btn_connect.pack(pady=10)
        
        btn_refresh = ctk.CTkButton(
            button_frame,
            text="🔄 Obnoviť emaily",
            command=self.refresh_emails,
            height=50,
            fg_color=theme["accent_secondary"],
            hover_color=theme["accent_glow"],
            font=("Segoe UI", 14, "bold"),
            corner_radius=12,
            state="disabled"
        )
        btn_refresh.pack(pady=10)
        self.refresh_btn = btn_refresh
        
        # Vyhľadávanie
        search_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        search_frame.pack(fill="x", pady=10)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Hľadať v emailoch...",
            height=40,
            font=("Segoe UI", 12),
            corner_radius=10
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        btn_search = ctk.CTkButton(
            search_frame,
            text="Hľadať",
            command=self.search_emails,
            width=100,
            height=40,
            fg_color=theme["accent"],
            hover_color=theme["accent_secondary"],
            corner_radius=10
        )
        btn_search.pack(side="right")
        
        # Výsledky emailov
        self.email_display = ctk.CTkTextbox(
            main_container,
            wrap="word",
            font=("Consolas", 11),
            fg_color=theme["bg_tertiary"],
            text_color=theme["text_primary"],
            corner_radius=15
        )
        self.email_display.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        
        # Skontroluj stav pri spustení
        self.after(100, self.check_gmail_status)
    
    def check_gmail_status(self):
        """Skontroluje stav Gmail API s GreenAura štýlom"""
        theme = GreenAuraTheme.get_theme(self.current_theme)
        try:
            response = requests.get('http://localhost:5001/gmail-status', timeout=5)
            data = response.json()
            
            if data.get('status') == 'connected':
                self.connection_status.configure(
                    text="✅ Gmail Pripojené",
                    text_color=theme["success"]
                )
                self.refresh_btn.configure(state="normal")
                self.email_display.insert("end", "✨ Gmail API je pripojené\n\n")
                AnimationManager.pulse_widget(self.connection_status, 2000)
                self.refresh_emails()
            else:
                self.connection_status.configure(
                    text="❌ Gmail Nepripojené", 
                    text_color=theme["error"]
                )
                self.email_display.insert("end", f"💫 {data.get('message', 'Neznáma chyba')}\n")
                
        except Exception as e:
            self.connection_status.configure(
                text="⚠️ Chyba pripojenia",
                text_color=theme["warning"]
            )
            self.email_display.insert("end", f"🔮 Chyba: {str(e)}\n")
            self.email_display.insert("end", "Uistite sa, že Gmail API server beží na porte 5001\n")
        
        self.email_display.see("end")
    
    def connect_gmail(self):
        """Spustí OAuth autorizáciu"""
        import webbrowser
        webbrowser.open('http://localhost:5001/authorize')
        self.email_display.insert("end", "🔮 Otváram autorizačnú stránku v prehliadači...\n")
        self.email_display.see("end")
        
        # Pulzujúci efekt počas autorizácie
        AnimationManager.pulse_widget(self.connection_status, 3000)
        
        # Skontroluj stav po 5 sekundách
        self.after(5000, self.check_gmail_status)
    
    def refresh_emails(self):
        """Načítaje emaily z Gmail API"""
        theme = GreenAuraTheme.get_theme(self.current_theme)
        try:
            response = requests.get('http://localhost:5001/gmail-emails?max=10')
            data = response.json()
            
            self.email_display.delete("1.0", "end")
            
            if 'emails' in data:
                emails = data['emails']
                self.email_display.insert("end", f"✨ Načítané emaily: {len(emails)}\n\n")
                
                for i, email in enumerate(emails, 1):
                    self.email_display.insert("end", f"📧 Email {i}:\n", "email_header")
                    self.email_display.insert("end", f"   👤 Od: {email['from']}\n")
                    self.email_display.insert("end", f"   📋 Predmet: {email['subject']}\n")
                    self.email_display.insert("end", f"   📝 Ukážka: {email['snippet'][:100]}...\n")
                    self.email_display.insert("end", "―" * 50 + "\n\n")
                    
                    # Tag pre zvýraznenie hlavičky emailu
                    self.email_display.tag_config("email_header", 
                                                foreground=theme["accent_glow"],
                                                font=("Consolas", 11, "bold"))
            else:
                self.email_display.insert("end", f"❌ Chyba: {data.get('error', 'Neznáma chyba')}\n")
                
        except Exception as e:
            self.email_display.insert("end", f"💥 Chyba pri načítaní emailov: {str(e)}\n")
        
        self.email_display.see("end")
    
    def search_emails(self):
        """Vyhľadáva v emailoch"""
        theme = GreenAuraTheme.get_theme(self.current_theme)
        query = self.search_entry.get().strip()
        if not query:
            return
            
        try:
            response = requests.get(f'http://localhost:5001/gmail-search?q={query}')
            data = response.json()
            
            self.email_display.delete("1.0", "end")
            
            if 'emails' in data:
                emails = data['emails']
                self.email_display.insert("end", f"🔍 Výsledky pre '{query}': {len(emails)} emailov\n\n")
                
                for i, email in enumerate(emails, 1):
                    self.email_display.insert("end", f"📧 {i}. {email['from']}\n", "search_result")
                    self.email_display.insert("end", f"   📋 {email['subject']}\n")
                    self.email_display.insert("end", f"   📝 {email['snippet'][:80]}...\n")
                    self.email_display.insert("end", "―" * 40 + "\n\n")
                    
                    self.email_display.tag_config("search_result", 
                                                foreground=theme["accent"])
            else:
                self.email_display.insert("end", f"❌ Chyba: {data.get('error', 'Neznáma chyba')}\n")
                
        except Exception as e:
            self.email_display.insert("end", f"💥 Chyba pri vyhľadávaní: {str(e)}\n")
        
        self.email_display.see("end")