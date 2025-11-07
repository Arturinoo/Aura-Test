import customtkinter as ctk
from .themes import ThemeManager

class SettingsTab(ctk.CTkFrame):
    def __init__(self, parent, config_manager):
        super().__init__(parent)
        self.parent = parent
        self.config_manager = config_manager
        self.current_theme = "green_aura"  # ✅ Zmena na green_aura
        
        self.setup_ui()
        self.load_current_settings()
    
    def setup_ui(self):
        """Nastaví pokročilé používateľské rozhranie nastavení"""
        # Scrollable area
        scroll_frame = ctk.CTkScrollableFrame(self)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Nadpis
        ctk.CTkLabel(
            scroll_frame,
            text="⚙️ Pokročilé Nastavenia",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=10)
        
        # AI Settings
        self.setup_ai_settings(scroll_frame)
        
        # Voice Settings
        self.setup_voice_settings(scroll_frame)
        
        # UI Settings
        self.setup_ui_settings(scroll_frame)
        
        # Save button
        save_btn = ctk.CTkButton(
            scroll_frame,
            text="💾 Uložiť Všetky Nastavenia",
            height=40,
            command=self.save_all_settings
        )
        save_btn.pack(pady=20)
    
    def setup_ai_settings(self, parent):
        """Nastaví sekciu AI nastavení"""
        ai_frame = ctk.CTkFrame(parent)
        ai_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            ai_frame,
            text="🤖 AI Nastavenia",
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w", padx=10, pady=10)
        
        # Model selection
        ctk.CTkLabel(ai_frame, text="AI Model:").pack(anchor="w", padx=10, pady=5)
        self.ai_model = ctk.CTkEntry(ai_frame, placeholder_text="qwen2.5:7b")
        self.ai_model.pack(fill="x", padx=10, pady=5)
        
        # Temperature
        ctk.CTkLabel(ai_frame, text="Teplota (kreativita):").pack(anchor="w", padx=10, pady=(10, 0))
        self.temperature = ctk.CTkSlider(
            ai_frame,
            from_=0.1,
            to=1.0,
            number_of_steps=10
        )
        self.temperature.pack(fill="x", padx=10, pady=5)
        
        # Max tokens
        ctk.CTkLabel(ai_frame, text="Maximálny počet tokenov:").pack(anchor="w", padx=10, pady=(10, 0))
        self.max_tokens = ctk.CTkEntry(ai_frame, placeholder_text="1000")
        self.max_tokens.pack(fill="x", padx=10, pady=5)
    
    def setup_voice_settings(self, parent):
        """Nastaví sekciu hlasových nastavení"""
        voice_frame = ctk.CTkFrame(parent)
        voice_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            voice_frame,
            text="🎤 Hlasové Nastavenia", 
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w", padx=10, pady=10)
        
        # Voice enable/disable
        self.voice_enabled = ctk.CTkSwitch(
            voice_frame,
            text="Povoliť hlasové ovládanie"
        )
        self.voice_enabled.pack(anchor="w", padx=10, pady=5)
        
        # Wake word
        ctk.CTkLabel(voice_frame, text="Wake-word (kľúčové slovo):").pack(anchor="w", padx=10, pady=(10, 0))
        self.wake_word = ctk.CTkEntry(voice_frame, placeholder_text="asistent")
        self.wake_word.pack(fill="x", padx=10, pady=5)
        
        # Speech rate
        ctk.CTkLabel(voice_frame, text="Rýchlosť reči:").pack(anchor="w", padx=10, pady=(10, 0))
        rate_frame = ctk.CTkFrame(voice_frame, fg_color="transparent")
        rate_frame.pack(fill="x", padx=10, pady=5)
        
        self.speech_rate = ctk.CTkSlider(
            rate_frame,
            from_=50,
            to=300,
            number_of_steps=25
        )
        self.speech_rate.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.speech_rate_label = ctk.CTkLabel(rate_frame, text="150", width=40)
        self.speech_rate_label.pack(side="right")
        
        self.speech_rate.configure(command=self.update_speech_rate_label)
    
    def setup_ui_settings(self, parent):
        """Nastaví sekciu UI nastavení"""
        ui_frame = ctk.CTkFrame(parent)
        ui_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            ui_frame,
            text="🎨 UI Nastavenia",
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w", padx=10, pady=10)
        
        # Theme selection
        ctk.CTkLabel(ui_frame, text="Téma:").pack(anchor="w", padx=10, pady=5)
        self.theme = ctk.CTkOptionMenu(
            ui_frame,
            values=["green_aura", "purple_aura", "dark", "light", "blue"]  # ✅ green_aura ako prvá
        )
        self.theme.pack(fill="x", padx=10, pady=5)
        
        # Font size
        ctk.CTkLabel(ui_frame, text="Veľkosť písma:").pack(anchor="w", padx=10, pady=(10, 0))
        self.font_size = ctk.CTkOptionMenu(
            ui_frame,
            values=["10", "11", "12", "14", "16"]
        )
        self.font_size.pack(fill="x", padx=10, pady=5)
    
    def update_speech_rate_label(self, value):
        """Aktualizuje label rýchlosti reči"""
        self.speech_rate_label.configure(text=str(int(float(value))))
    
    def load_current_settings(self):
        """Načíta aktuálne nastavenia"""
        try:
            settings = self.config_manager.load_settings()
            
            # AI settings
            ai_settings = settings.get("ai", {})
            self.ai_model.insert(0, ai_settings.get("local_model", "qwen2.5:7b"))
            self.temperature.set(ai_settings.get("temperature", 0.7))
            self.max_tokens.insert(0, str(ai_settings.get("max_tokens", 1000)))
            
            # Voice settings
            voice_settings = settings.get("voice", {})
            if voice_settings.get("enabled", True):
                self.voice_enabled.select()
            else:
                self.voice_enabled.deselect()
            
            self.wake_word.insert(0, voice_settings.get("wake_word", "asistent"))
            self.speech_rate.set(voice_settings.get("speech_rate", 150))
            self.update_speech_rate_label(voice_settings.get("speech_rate", 150))
            
            # UI settings
            ui_settings = settings.get("ui", {})
            self.theme.set(ui_settings.get("theme", "green_aura"))  # ✅ Zmena na green_aura
            self.font_size.set(str(ui_settings.get("font_size", 12)))
            
        except Exception as e:
            print(f"❌ Chyba pri načítaní nastavení: {e}")
    
    def save_all_settings(self):
        """Uloží všetky nastavenia"""
        try:
            settings = self.config_manager.load_settings()
            
            # AI settings
            settings["ai"] = {
                "local_model": self.ai_model.get(),
                "cloud_model": settings.get("ai", {}).get("cloud_model", "gpt-4"),
                "use_cloud": False,
                "temperature": self.temperature.get(),
                "max_tokens": int(self.max_tokens.get() or 1000)
            }
            
            # Voice settings
            settings["voice"] = {
                "enabled": self.voice_enabled.get(),
                "wake_word": self.wake_word.get(),
                "language": "sk-SK",
                "speech_rate": self.speech_rate.get()
            }
            
            # UI settings
            settings["ui"] = {
                "theme": self.theme.get(),
                "font_size": int(self.font_size.get()),
                "window_width": settings.get("ui", {}).get("window_width", 1400),
                "window_height": settings.get("ui", {}).get("window_height", 900)
            }
            
            self.config_manager.save_settings(settings)
            
            # Aktualizuj hlasové nastavenia
            if hasattr(self.parent, 'assistant'):
                self.parent.assistant.update_voice_settings()
            
            self.show_success("✅ Všetky nastavenia boli úspešne uložené!")
            
        except Exception as e:
            self.show_error(f"❌ Chyba pri ukladaní nastavení: {e}")
    
    def show_success(self, message):
        """Zobrazí úspešnú správu"""
        # TODO: Implementovať notifikácie
        print(message)
    
    def show_error(self, message):
        """Zobrazí chybovú správu"""
        # TODO: Implementovať notifikácie  
        print(message)