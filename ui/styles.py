import customtkinter as ctk
from .themes import ThemeManager

class AppStyles:
    """Pokročilý systém štýlov pre aplikáciu"""
    
    @staticmethod
    def create_rounded_button(master, text, command, **kwargs):
        """Vytvorí zaoblené tlačidlo s moderným vzhľadom"""
        return ctk.CTkButton(
            master,
            text=text,
            command=command,
            corner_radius=15,
            border_width=0,
            fg_color=ThemeManager.get_theme("dark")["accent"],
            hover_color=ThemeManager.get_theme("dark")["accent_hover"],
            text_color=ThemeManager.get_theme("dark")["text_primary"],
            font=("Segoe UI", 12, "bold"),
            **kwargs
        )
    
    @staticmethod
    def create_card(master, **kwargs):
        """Vytvorí moderný kartový widget"""
        return ctk.CTkFrame(
            master,
            corner_radius=12,
            border_width=1,
            fg_color=ThemeManager.get_theme("dark")["bg_secondary"],
            border_color=ThemeManager.get_theme("dark")["border"],
            **kwargs
        )
    
    @staticmethod
    def create_modern_entry(master, placeholder, **kwargs):
        """Vytvorí moderný vstup"""
        return ctk.CTkEntry(
            master,
            placeholder_text=placeholder,
            corner_radius=10,
            border_width=0,
            fg_color=ThemeManager.get_theme("dark")["bg_tertiary"],
            text_color=ThemeManager.get_theme("dark")["text_primary"],
            placeholder_text_color=ThemeManager.get_theme("dark")["text_secondary"],
            font=("Segoe UI", 11),
            **kwargs
        )
    
    @staticmethod
    def create_section_title(master, text):
        """Vytvorí nadpis sekcie"""
        return ctk.CTkLabel(
            master,
            text=text,
            font=("Segoe UI", 16, "bold"),
            text_color=ThemeManager.get_theme("dark")["text_primary"]
        )

class AnimationManager:
    """Manažér animácií pre UI"""
    
    @staticmethod
    def fade_in(widget, duration=200):
        """Animácia plynulého zobrazenia"""
        widget.configure(state="normal")
        
    @staticmethod
    def slide_in(widget, from_right=True):
        """Animácia vysunutia"""
        # Toto by sa dalo implementovať s move pomocou after()
        pass