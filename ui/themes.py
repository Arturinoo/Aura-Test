import customtkinter as ctk
from typing import Dict, Any

class ThemeManager:
    """Manažér tém pre aplikáciu"""
    
    THEMES = {
        "dark": {
            "name": "Tmavá",
            "bg": "#1a1a1a",
            "bg_secondary": "#2d2d2d",
            "bg_tertiary": "#3d3d3d",
            "accent": "#0078d4",
            "accent_hover": "#106ebe",
            "text_primary": "#ffffff",
            "text_secondary": "#cccccc",
            "success": "#107c10",
            "warning": "#d83b01",
            "error": "#e81123",
            "border": "#404040"
        },
        "light": {
            "name": "Svetlá", 
            "bg": "#ffffff",
            "bg_secondary": "#f3f3f3",
            "bg_tertiary": "#e1e1e1",
            "accent": "#0078d4",
            "accent_hover": "#106ebe",
            "text_primary": "#000000",
            "text_secondary": "#666666",
            "success": "#107c10",
            "warning": "#d83b01",
            "error": "#e81123",
            "border": "#d1d1d1"
        },
        "blue": {
            "name": "Modrá",
            "bg": "#0d1b2a",
            "bg_secondary": "#1b263b",
            "bg_tertiary": "#415a77",
            "accent": "#ff9e00",
            "accent_hover": "#ffb133",
            "text_primary": "#e0e1dd",
            "text_secondary": "#a8b0b9",
            "success": "#4caf50",
            "warning": "#ff9800",
            "error": "#f44336",
            "border": "#415a77"
        },
        "green": {
            "name": "Zelená",
            "bg": "#1b4332",
            "bg_secondary": "#2d6a4f",
            "bg_tertiary": "#40916c",
            "accent": "#ff9e00",
            "accent_hover": "#ffb133",
            "text_primary": "#d8f3dc",
            "text_secondary": "#b7e4c7",
            "success": "#4caf50",
            "warning": "#ff9800",
            "error": "#f44336",
            "border": "#40916c"
        }
    }
    
    @classmethod
    def get_theme(cls, theme_name: str) -> Dict[str, Any]:
        """Vráti farby pre danú tému"""
        return cls.THEMES.get(theme_name, cls.THEMES["dark"])
    
    @classmethod
    def get_available_themes(cls):
        """Vráti zoznam dostupných tém"""
        return list(cls.THEMES.keys())
    
    @classmethod
    def apply_theme(cls, theme_name: str):
        """Aplikuje tému na celú aplikáciu"""
        theme = cls.get_theme(theme_name)
        
        # Nastav CustomTkinter theme
        ctk.set_appearance_mode("dark" if theme_name in ["dark", "blue", "green"] else "light")
        
        # Vytvor custom color theme
        custom_theme = {
            "fg_color": theme["bg_secondary"],
            "top_fg_color": theme["bg_secondary"],
            "text_color": theme["text_primary"],
            "button_color": theme["accent"],
            "button_hover_color": theme["accent_hover"],
            "border_color": theme["border"]
        }
        
        return theme