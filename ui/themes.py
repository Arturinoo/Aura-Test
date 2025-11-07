# ui/themes.py
import customtkinter as ctk
import math
import time
from typing import Dict, Any, List
import threading

class GreenAuraTheme:
    """GreenAura téma s tmavozelenými a tmavosivými farbami"""
    
    # ZELENO-SIVÁ PALETA FARIEB
    COLORS = {
        # Tmavé odtiene (pozadia)
        "deep_green": "#0A2F0A",       # Veľmi tmavá zelená - hlavné pozadie
        "forest_green": "#1B4D1B",     # Tmavá lesná zelená - sekundárne pozadie
        "dark_slate": "#2F4F4F",       # Tmavá bridlicová sivá - panely
        "charcoal_gray": "#36454F",    # Uhoľná sivá - alternatívne pozadie
        
        # Stredné odtiene (akcenty)
        "hunter_green": "#355E3B",     # Poľovnícka zelená - primárne akcenty
        "sage_green": "#87A96B",       # Salvová zelená - sekundárne akcenty
        "steel_blue": "#4682B4",       # Oceľová modrá - interaktívne prvky
        "slate_gray": "#708090",       # Bridlicová sivá - text a hranice
        
        # Svietivé odtiene (zvýraznenia)
        "emerald_green": "#50C878",    # Smaragdová zelená - hlavné zvýraznenia
        "mint_green": "#98FB98",       # Mätová zelená - hover efekty
        "neon_green": "#39FF14",       # Neónová zelená - aktívne stav
        "silver": "#C0C0C0",           # Strieborná - sekundárny text
        
        # Funkčné farby
        "success": "#00FF88",          # Úspech (zelená)
        "warning": "#FFAA00",          # Varovanie (oranžová)
        "error": "#FF4444",            # Chyba (červená)
        "info": "#4682B4"              # Informácie (modrá)
    }
    
    @staticmethod
    def get_theme(theme_name="green_aura"):
        """Vráti GreenAura tému - OPRAVENÁ VERZIA"""
        return {
            "bg": GreenAuraTheme.COLORS["deep_green"],
            "bg_secondary": GreenAuraTheme.COLORS["forest_green"],
            "bg_tertiary": GreenAuraTheme.COLORS["dark_slate"],
            "accent": GreenAuraTheme.COLORS["emerald_green"],
            "accent_secondary": GreenAuraTheme.COLORS["sage_green"],
            "accent_glow": GreenAuraTheme.COLORS["neon_green"],
            "text_primary": "#FFFFFF",
            "text_secondary": GreenAuraTheme.COLORS["silver"],
            "text_accent": GreenAuraTheme.COLORS["mint_green"],
            "success": GreenAuraTheme.COLORS["success"],
            "warning": GreenAuraTheme.COLORS["warning"],
            "error": GreenAuraTheme.COLORS["error"],
            "card_bg": GreenAuraTheme.COLORS["charcoal_gray"],
            "glass_effect": "rgba(10, 47, 10, 0.3)",
            "shadow_color": "rgba(80, 200, 120, 0.3)",
            "border": GreenAuraTheme.COLORS["slate_gray"],  # ✅ PRIDANÉ
            "border_color": GreenAuraTheme.COLORS["slate_gray"]  # ✅ PRIDANÉ
        }

class PurpleAuraTheme:
    """PurpleAura téma s animáciami a efektmi"""
    
    # Základné fialové farby
    COLORS = {
        "deep_purple": "#2D033B",
        "royal_purple": "#4C1A57", 
        "vibrant_purple": "#6A2C70",
        "lavender": "#A660C9",
        "light_lavender": "#C191D9",
        "electric_purple": "#8100FF",
        "magenta": "#FF00FF",
        "neon_purple": "#BC13FE",
        "dark_purple": "#1A0030"
    }
    
    @staticmethod
    def get_theme(theme_name="purple_aura"):
        """Vráti PurpleAura tému"""
        return {
            "bg": PurpleAuraTheme.COLORS["deep_purple"],
            "bg_secondary": PurpleAuraTheme.COLORS["royal_purple"],
            "bg_tertiary": PurpleAuraTheme.COLORS["vibrant_purple"],
            "accent": PurpleAuraTheme.COLORS["electric_purple"],
            "accent_secondary": PurpleAuraTheme.COLORS["lavender"],
            "accent_glow": PurpleAuraTheme.COLORS["neon_purple"],
            "text_primary": "#FFFFFF",
            "text_secondary": "#E0E0E0",
            "text_accent": PurpleAuraTheme.COLORS["light_lavender"],
            "success": "#00FF88",
            "warning": "#FFAA00",
            "error": "#FF4444",
            "card_bg": PurpleAuraTheme.COLORS["royal_purple"],
            "glass_effect": "rgba(74, 20, 140, 0.3)",
            "shadow_color": "rgba(129, 0, 255, 0.3)",
            "border": PurpleAuraTheme.COLORS["lavender"],  # ✅ PRIDANÉ
            "border_color": PurpleAuraTheme.COLORS["lavender"]  # ✅ PRIDANÉ
        }

class AnimationManager:
    """Manažér pre animácie a efekty"""
    
    @staticmethod
    def pulse_widget(widget, duration=2000):
        """Pulzujúca animácia pre widget - IMPLEMENTÁCIA"""
        def pulse():
            start_time = time.time()
            original_color = widget.cget("text_color")
            colors = [GreenAuraTheme.COLORS["neon_green"], GreenAuraTheme.COLORS["mint_green"]]
            
            while time.time() - start_time < duration / 1000:
                try:
                    progress = (time.time() - start_time) / (duration / 1000)
                    color_index = int(progress * 10) % 2
                    widget.configure(text_color=colors[color_index])
                    time.sleep(0.2)
                except:
                    break
            
            # Reset na pôvodnú farbu
            try:
                widget.configure(text_color=original_color)
            except:
                pass
        
        thread = threading.Thread(target=pulse, daemon=True)
        thread.start()
    
    @staticmethod
    def mix_colors(color1, color2, ratio):
        """Zmieša dve farby podľa pomeru"""
        try:
            r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
            r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
            
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            
            return f"#{r:02x}{g:02x}{b:02x}"
        except:
            return color1
    
    @staticmethod
    def create_glow_effect(widget):
        """Pridá glow efekt widgetu"""
        try:
            widget.configure(
                border_color=GreenAuraTheme.COLORS["emerald_green"],
                border_width=2
            )
        except:
            pass

class ThemeManager:
    """Manažér tém a štýlov"""
    
    @staticmethod
    def get_theme(theme_name="green_aura"):  # ✅ Zmena na green_aura ako predvolenú
        if theme_name == "green_aura":
            return GreenAuraTheme.get_theme(theme_name)
        elif theme_name == "purple_aura":
            return PurpleAuraTheme.get_theme(theme_name)
        else:
            return GreenAuraTheme.get_theme("green_aura")  # ✅ Fallback na green_aura
    
    @staticmethod
    def apply_theme(theme_name):
        return ThemeManager.get_theme(theme_name)
    
    @staticmethod
    def setup_customtkinter_theme():
        """Nastaví CustomTkinter pre GreenAura tému"""
        ctk.set_appearance_mode("dark")
        
        try:
            import json
            import tempfile
            import os
            
            green_theme = {
                "CTk": {
                    "fg_color": [GreenAuraTheme.COLORS["deep_green"], GreenAuraTheme.COLORS["charcoal_gray"]],
                    "top_fg_color": [GreenAuraTheme.COLORS["forest_green"], GreenAuraTheme.COLORS["dark_slate"]],
                    "text_color": ["#FFFFFF", "#FFFFFF"]
                },
                "CTkFrame": {
                    "fg_color": [GreenAuraTheme.COLORS["forest_green"], GreenAuraTheme.COLORS["dark_slate"]],
                    "top_fg_color": [GreenAuraTheme.COLORS["dark_slate"], GreenAuraTheme.COLORS["forest_green"]],
                    "border_color": [GreenAuraTheme.COLORS["emerald_green"], GreenAuraTheme.COLORS["sage_green"]]
                },
                "CTkButton": {
                    "fg_color": [GreenAuraTheme.COLORS["emerald_green"], GreenAuraTheme.COLORS["hunter_green"]],
                    "hover_color": [GreenAuraTheme.COLORS["mint_green"], GreenAuraTheme.COLORS["sage_green"]],
                    "text_color": ["white", "white"],
                    "border_color": [GreenAuraTheme.COLORS["neon_green"], GreenAuraTheme.COLORS["mint_green"]]
                },
                "CTkLabel": {
                    "text_color": ["white", "white"],
                    "fg_color": ["transparent", "transparent"]
                },
                "CTkEntry": {
                    "fg_color": [GreenAuraTheme.COLORS["charcoal_gray"], GreenAuraTheme.COLORS["forest_green"]],
                    "border_color": [GreenAuraTheme.COLORS["emerald_green"], GreenAuraTheme.COLORS["sage_green"]],
                    "text_color": ["white", "white"]
                },
                "CTkTextbox": {
                    "fg_color": [GreenAuraTheme.COLORS["charcoal_gray"], GreenAuraTheme.COLORS["forest_green"]],
                    "border_color": [GreenAuraTheme.COLORS["emerald_green"], GreenAuraTheme.COLORS["sage_green"]],
                    "text_color": ["white", "white"]
                }
            }
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(green_theme, f)
                temp_theme_file = f.name
            
            ctk.set_default_color_theme(temp_theme_file)
            
            import atexit
            atexit.register(lambda: os.unlink(temp_theme_file) if os.path.exists(temp_theme_file) else None)
            
        except Exception as e:
            print(f"⚠️ Nepodarilo sa nastaviť GreenAura tému: {e}")
            ctk.set_default_color_theme("blue")