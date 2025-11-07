# ui/themes.py
import customtkinter as ctk
import math
import time
from typing import Dict, Any, List
import threading

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
            "shadow_color": "rgba(129, 0, 255, 0.3)"
        }

class AnimationManager:
    """Manažér pre animácie a efekty"""
    
    @staticmethod
    def pulse_widget(widget, duration=2000):
        """Pulzujúca animácia pre widget"""
        def pulse():
            start_time = time.time()
            while time.time() - start_time < duration / 1000:
                progress = (time.time() - start_time) / (duration / 1000)
                alpha = 0.5 + 0.5 * math.sin(progress * math.pi * 2)
                try:
                    widget.configure(fg_color=AnimationManager.mix_colors(
                        PurpleAuraTheme.COLORS["vibrant_purple"],
                        PurpleAuraTheme.COLORS["neon_purple"],
                        alpha
                    ))
                except:
                    break
                time.sleep(0.05)
            # Reset na pôvodnú farbu
            try:
                widget.configure(fg_color=PurpleAuraTheme.COLORS["vibrant_purple"])
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
                border_color=PurpleAuraTheme.COLORS["electric_purple"],
                border_width=2
            )
        except:
            pass

class ThemeManager:
    """Manažér tém a štýlov"""
    
    @staticmethod
    def get_theme(theme_name="purple_aura"):
        return PurpleAuraTheme.get_theme(theme_name)
    
    @staticmethod
    def apply_theme(theme_name):
        return ThemeManager.get_theme(theme_name)
    
    @staticmethod
    def setup_customtkinter_theme():
        """Nastaví CustomTkinter pre PurpleAura tému - OPRAVENÁ VERZIA"""
        ctk.set_appearance_mode("dark")
        
        # ✅ OPRAVENÉ: Vytvoríme vlastnú tému pomocou set_default_color_theme
        try:
            # Vytvoríme dočasný JSON súbor s PurpleAura témou
            import json
            import tempfile
            import os
            
            purple_theme = {
                "CTk": {
                    "fg_color": [PurpleAuraTheme.COLORS["deep_purple"], PurpleAuraTheme.COLORS["dark_purple"]],
                    "top_fg_color": [PurpleAuraTheme.COLORS["royal_purple"], PurpleAuraTheme.COLORS["vibrant_purple"]],
                    "text_color": ["#FFFFFF", "#FFFFFF"]
                },
                "CTkFrame": {
                    "fg_color": [PurpleAuraTheme.COLORS["royal_purple"], PurpleAuraTheme.COLORS["vibrant_purple"]],
                    "top_fg_color": [PurpleAuraTheme.COLORS["vibrant_purple"], PurpleAuraTheme.COLORS["royal_purple"]],
                    "border_color": [PurpleAuraTheme.COLORS["electric_purple"], PurpleAuraTheme.COLORS["lavender"]]
                },
                "CTkButton": {
                    "fg_color": [PurpleAuraTheme.COLORS["electric_purple"], PurpleAuraTheme.COLORS["vibrant_purple"]],
                    "hover_color": [PurpleAuraTheme.COLORS["lavender"], PurpleAuraTheme.COLORS["light_lavender"]],
                    "text_color": ["white", "white"],
                    "border_color": [PurpleAuraTheme.COLORS["neon_purple"], PurpleAuraTheme.COLORS["magenta"]]
                },
                "CTkLabel": {
                    "text_color": ["white", "white"],
                    "fg_color": ["transparent", "transparent"]
                },
                "CTkEntry": {
                    "fg_color": [PurpleAuraTheme.COLORS["dark_purple"], PurpleAuraTheme.COLORS["royal_purple"]],
                    "border_color": [PurpleAuraTheme.COLORS["electric_purple"], PurpleAuraTheme.COLORS["lavender"]],
                    "text_color": ["white", "white"]
                },
                "CTkTextbox": {
                    "fg_color": [PurpleAuraTheme.COLORS["dark_purple"], PurpleAuraTheme.COLORS["royal_purple"]],
                    "border_color": [PurpleAuraTheme.COLORS["electric_purple"], PurpleAuraTheme.COLORS["lavender"]],
                    "text_color": ["white", "white"]
                }
            }
            
            # Uložíme do dočasného súboru
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(purple_theme, f)
                temp_theme_file = f.name
            
            # Nastavíme tému
            ctk.set_default_color_theme(temp_theme_file)
            
            # Súbor sa automaticky vymaže po skončení programu
            import atexit
            atexit.register(lambda: os.unlink(temp_theme_file) if os.path.exists(temp_theme_file) else None)
            
        except Exception as e:
            print(f"⚠️ Nepodarilo sa nastaviť PurpleAura tému: {e}")
            # Fallback na modrú tému
            ctk.set_default_color_theme("blue")