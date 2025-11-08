# ui/quantum_settings_tab.py
import customtkinter as ctk
from customtkinter import CTkScrollableFrame, CTkTabview, CTkOptionMenu, CTkSlider, CTkSwitch
from .themes import theme_manager

class QuantumSettingsTab(ctk.CTkFrame):
    def __init__(self, parent, config_manager):
        self.theme = theme_manager.get_theme("quantum_green")
        super().__init__(parent, fg_color=self.theme["bg"], corner_radius=0, border_width=0)
        
        self.config_manager = config_manager
        
        self.setup_quantum_settings_ui()
        self.load_current_settings()
    
    def setup_quantum_settings_ui(self):
        """Vytvorí quantum settings interface"""
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
        self.setup_settings_header(main_container)
        
        # Obsah
        self.setup_settings_content(main_container)
    
    def setup_settings_header(self, parent):
        """Vytvorí header nastavení"""
        header = ctk.CTkFrame(
            parent,
            height=80,
            fg_color=self.theme["bg_secondary"],
            corner_radius=0,
            border_width=0
        )
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        
        ctk.CTkLabel(
            header,
            text="⚙️ QUANTUM SETTINGS",
            font=("Segoe UI", 20, "bold"),
            text_color=self.theme["accent_glow"]
        ).pack(side="left", padx=30, pady=20)
        
        self.settings_status = ctk.CTkLabel(
            header,
            text="CONFIGURATION ACTIVE",
            font=("Consolas", 12),
            text_color=self.theme["success"]
        )
        self.settings_status.pack(side="right", padx=30, pady=20)
    
    def setup_settings_content(self, parent):
        """Vytvorí obsah nastavení"""
        scroll_frame = ctk.CTkScrollableFrame(
            parent,
            fg_color=self.theme["bg"],
            scrollbar_button_color=self.theme["accent_secondary"],
            scrollbar_button_hover_color=self.theme["accent_glow"]
        )
        scroll_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        
        # AI Settings
        self.setup_ai_settings(scroll_frame)
        
        # Voice Settings
        self.setup_voice_settings(scroll_frame)
        
        # UI Settings
        self.setup_ui_settings(scroll_frame)
        
        # System Settings
        self.setup_system_settings(scroll_frame)
        
        # Save button
        ctk.CTkButton(
            scroll_frame,
            text="💾 SAVE QUANTUM CONFIGURATION",
            command=self.save_all_settings,
            height=60,
            fg_color=self.theme["accent"],
            hover_color=self.theme["accent_glow"],
            font=("Segoe UI", 16, "bold"),
            corner_radius=15
        ).pack(fill="x", pady=20)
    
    def setup_ai_settings(self, parent):
        """Nastaví AI sekciu"""
        section_frame = ctk.CTkFrame(
            parent,
            fg_color=self.theme["bg_secondary"],
            corner_radius=15,
            border_width=2,
            border_color=self.theme["accent_secondary"]
        )
        section_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            section_frame,
            text="🤖 QUANTUM AI SETTINGS",
            font=("Segoe UI", 16, "bold"),
            text_color=self.theme["accent_glow"]
        ).pack(anchor="w", padx=20, pady=15)
        
        # Model selection
        ctk.CTkLabel(
            section_frame,
            text="AI Model:",
            font=("Segoe UI", 12, "bold"),
            text_color=self.theme["text_primary"]
        ).pack(anchor="w", padx=20, pady=(0, 5))
        
        self.ai_model = ctk.CTkOptionMenu(
            section_frame,
            values=["qwen3", "qwen2.5:7b", "llama2", "mistral"],
            fg_color=self.theme["bg_tertiary"],
            button_color=self.theme["accent_secondary"],
            button_hover_color=self.theme["accent_glow"],
            text_color=self.theme["text_primary"]
        )
        self.ai_model.pack(fill="x", padx=20, pady=(0, 15))
        
        # Temperature
        temp_frame = ctk.CTkFrame(section_frame, fg_color="transparent", border_width=0)
        temp_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            temp_frame,
            text="Creativity (Temperature):",
            font=("Segoe UI", 12, "bold"),
            text_color=self.theme["text_primary"]
        ).pack(anchor="w")
        
        self.temperature = ctk.CTkSlider(
            temp_frame,
            from_=0.1,
            to=1.0,
            number_of_steps=10,
            fg_color=self.theme["bg_tertiary"],
            progress_color=self.theme["accent_secondary"],
            button_color=self.theme["accent_glow"],
            button_hover_color=self.theme["accent"]
        )
        self.temperature.pack(fill="x", pady=5)
        self.temperature.set(0.7)
        
        # Max tokens
        ctk.CTkLabel(
            section_frame,
            text="Max Response Length:",
            font=("Segoe UI", 12, "bold"),
            text_color=self.theme["text_primary"]
        ).pack(anchor="w", padx=20, pady=(15, 5))
        
        self.max_tokens = ctk.CTkEntry(
            section_frame,
            placeholder_text="1000",
            fg_color=self.theme["bg_tertiary"],
            text_color=self.theme["text_primary"],
            border_color=self.theme["accent_secondary"]
        )
        self.max_tokens.pack(fill="x", padx=20, pady=(0, 15))
        self.max_tokens.insert(0, "1000")
    
    def setup_voice_settings(self, parent):
        """Nastaví hlasovú sekciu"""
        section_frame = ctk.CTkFrame(
            parent,
            fg_color=self.theme["bg_secondary"],
            corner_radius=15,
            border_width=2,
            border_color=self.theme["accent_secondary"]
        )
        section_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            section_frame,
            text="🎤 QUANTUM VOICE SETTINGS",
            font=("Segoe UI", 16, "bold"),
            text_color=self.theme["accent_glow"]
        ).pack(anchor="w", padx=20, pady=15)
        
        # Voice enable
        self.voice_enabled = ctk.CTkSwitch(
            section_frame,
            text="Enable Quantum Voice Control",
            font=("Segoe UI", 12),
            fg_color=self.theme["accent_secondary"],
            progress_color=self.theme["accent_glow"]
        )
        self.voice_enabled.pack(anchor="w", padx=20, pady=10)
        self.voice_enabled.select()
        
        # Wake word
        ctk.CTkLabel(
            section_frame,
            text="Wake Word:",
            font=("Segoe UI", 12, "bold"),
            text_color=self.theme["text_primary"]
        ).pack(anchor="w", padx=20, pady=(15, 5))
        
        self.wake_word = ctk.CTkEntry(
            section_frame,
            placeholder_text="quantum",
            fg_color=self.theme["bg_tertiary"],
            text_color=self.theme["text_primary"],
            border_color=self.theme["accent_secondary"]
        )
        self.wake_word.pack(fill="x", padx=20, pady=(0, 15))
        self.wake_word.insert(0, "quantum")
    
    def setup_ui_settings(self, parent):
        """Nastaví UI sekciu"""
        section_frame = ctk.CTkFrame(
            parent,
            fg_color=self.theme["bg_secondary"],
            corner_radius=15,
            border_width=2,
            border_color=self.theme["accent_secondary"]
        )
        section_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            section_frame,
            text="🎨 QUANTUM UI SETTINGS",
            font=("Segoe UI", 16, "bold"),
            text_color=self.theme["accent_glow"]
        ).pack(anchor="w", padx=20, pady=15)
        
        # Theme selection
        ctk.CTkLabel(
            section_frame,
            text="Quantum Theme:",
            font=("Segoe UI", 12, "bold"),
            text_color=self.theme["text_primary"]
        ).pack(anchor="w", padx=20, pady=(0, 5))
        
        self.theme_selector = ctk.CTkOptionMenu(
            section_frame,
            values=["quantum_green", "quantum_blue", "quantum_purple", "quantum_red"],
            fg_color=self.theme["bg_tertiary"],
            button_color=self.theme["accent_secondary"],
            button_hover_color=self.theme["accent_glow"],
            text_color=self.theme["text_primary"]
        )
        self.theme_selector.pack(fill="x", padx=20, pady=(0, 15))
        
        # Animation toggle
        self.animations_enabled = ctk.CTkSwitch(
            section_frame,
            text="Enable Quantum Animations",
            font=("Segoe UI", 12),
            fg_color=self.theme["accent_secondary"],
            progress_color=self.theme["accent_glow"]
        )
        self.animations_enabled.pack(anchor="w", padx=20, pady=10)
        self.animations_enabled.select()
    
    def setup_system_settings(self, parent):
        """Nastaví systémovú sekciu"""
        section_frame = ctk.CTkFrame(
            parent,
            fg_color=self.theme["bg_secondary"],
            corner_radius=15,
            border_width=2,
            border_color=self.theme["accent_secondary"]
        )
        section_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            section_frame,
            text="⚡ QUANTUM SYSTEM SETTINGS",
            font=("Segoe UI", 16, "bold"),
            text_color=self.theme["accent_glow"]
        ).pack(anchor="w", padx=20, pady=15)
        
        # Auto-start
        self.auto_start = ctk.CTkSwitch(
            section_frame,
            text="Launch at System Startup",
            font=("Segoe UI", 12),
            fg_color=self.theme["accent_secondary"],
            progress_color=self.theme["accent_glow"]
        )
        self.auto_start.pack(anchor="w", padx=20, pady=10)
        
        # Auto-update
        self.auto_update = ctk.CTkSwitch(
            section_frame,
            text="Automatic Quantum Updates",
            font=("Segoe UI", 12),
            fg_color=self.theme["accent_secondary"],
            progress_color=self.theme["accent_glow"]
        )
        self.auto_update.pack(anchor="w", padx=20, pady=10)
        self.auto_update.select()
        
        # Performance mode
        self.performance_mode = ctk.CTkSwitch(
            section_frame,
            text="High Performance Mode",
            font=("Segoe UI", 12),
            fg_color=self.theme["accent_secondary"],
            progress_color=self.theme["accent_glow"]
        )
        self.performance_mode.pack(anchor="w", padx=20, pady=10)
    
    def load_current_settings(self):
        """Načíta aktuálne nastavenia"""
        try:
            settings = self.config_manager.load_settings()
            
            # AI settings
            ai_settings = settings.get("ai", {})
            self.ai_model.set(ai_settings.get("local_model", "qwen3"))
            self.temperature.set(ai_settings.get("temperature", 0.7))
            self.max_tokens.delete(0, "end")
            self.max_tokens.insert(0, str(ai_settings.get("max_tokens", 1000)))
            
            # Voice settings
            voice_settings = settings.get("voice", {})
            if voice_settings.get("enabled", True):
                self.voice_enabled.select()
            else:
                self.voice_enabled.deselect()
            
            self.wake_word.delete(0, "end")
            self.wake_word.insert(0, voice_settings.get("wake_word", "quantum"))
            
            # UI settings
            ui_settings = settings.get("ui", {})
            self.theme_selector.set(ui_settings.get("theme", "quantum_green"))
            
            if ui_settings.get("animations", True):
                self.animations_enabled.select()
            else:
                self.animations_enabled.deselect()
                
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    def save_all_settings(self):
        """Uloží všetky nastavenia"""
        try:
            settings = self.config_manager.load_settings()
            
            # AI settings
            settings["ai"] = {
                "local_model": self.ai_model.get(),
                "temperature": self.temperature.get(),
                "max_tokens": int(self.max_tokens.get() or 1000)
            }
            
            # Voice settings
            settings["voice"] = {
                "enabled": self.voice_enabled.get(),
                "wake_word": self.wake_word.get()
            }
            
            # UI settings
            settings["ui"] = {
                "theme": self.theme_selector.get(),
                "animations": self.animations_enabled.get()
            }
            
            # System settings
            settings["system"] = {
                "auto_start": self.auto_start.get(),
                "auto_update": self.auto_update.get(),
                "performance_mode": self.performance_mode.get()
            }
            
            self.config_manager.save_settings(settings)
            self.show_success("Quantum configuration saved successfully!")
            
        except Exception as e:
            self.show_error(f"Error saving settings: {e}")
    
    def show_success(self, message):
        """Zobrazí úspešnú správu"""
        self.settings_status.configure(text="✅ CONFIGURATION SAVED", text_color=self.theme["success"])
    
    def show_error(self, message):
        """Zobrazí chybovú správu"""
        self.settings_status.configure(text="❌ SAVE FAILED", text_color=self.theme["error"])
        print(f"Settings Error: {message}")