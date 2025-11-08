# ui/themes.py - OPRAVENÁ VERZIA
import customtkinter as ctk
import time
import math

class AnimationEngine:
    def __init__(self):
        self.widgets = {}
        self.animations = {}
    
    def register_widget(self, widget_id, widget):
        self.widgets[widget_id] = widget
    
    def animate_glow(self, widget_id, colors):
        if widget_id not in self.widgets:
            return
        
        def animate_step(step=0):
            if widget_id not in self.widgets:
                return
            
            try:
                color_index = step % len(colors)
                widget = self.widgets[widget_id]
                
                if hasattr(widget, 'configure'):
                    widget.configure(text_color=colors[color_index])
                
                self.animations[widget_id] = widget.after(500, lambda: animate_step(step + 1))
            except:
                pass
        
        animate_step()
    
    def create_ripple(self, widget, x, y):
        """Vytvorí ripple efekt pri kliknutí"""
        try:
            # Vytvoríme dočasný canvas pre ripple efekt
            ripple = ctk.CTkFrame(
                widget,
                width=20,
                height=20,
                fg_color="white",
                corner_radius=10
            )
            ripple.place(x=x-10, y=y-10)
            
            # Animácia rastu a zániku
            def animate_ripple(size=20, alpha=1.0):
                if size > 100 or alpha <= 0:
                    ripple.destroy()
                    return
                
                ripple.configure(width=size, height=size)
                new_alpha = alpha - 0.1
                if new_alpha > 0:
                    ripple.after(20, lambda: animate_ripple(size + 5, new_alpha))
            
            animate_ripple()
        except:
            pass
    
    def stop_animation(self, widget_id):
        if widget_id in self.animations:
            try:
                self.widgets[widget_id].after_cancel(self.animations[widget_id])
            except:
                pass

class ThemeManager:
    def __init__(self):
        self.animation_engine = AnimationEngine()
        self.setup_themes()
    
    def setup_themes(self):
        """Nastaví kompletnú tému s opravou pre CTkScrollbar"""
        self.themes = {
            "quantum_green": {
                # Hlavné farby
                "bg": "#0a0a0a",
                "bg_secondary": "#1a1a1a", 
                "bg_tertiary": "#2a2a2a",
                "text_primary": "#ffffff",
                "text_secondary": "#aaaaaa",
                
                # Akcentné farby
                "accent": "#00ff00",
                "accent_secondary": "#00cc00",
                "accent_glow": "#00ff00",
                
                # Štátové farby
                "success": "#00ff00",
                "warning": "#ffff00",
                "error": "#ff0000",
                
                # Ohraničenie
                "border": "#333333",
                
                # CustomTkinter špecifické kľúče - OPRAVA
                "CTkScrollbar": {
                    "fg_color": "#1a1a1a",
                    "button_color": "#00ff00",
                    "button_hover_color": "#00cc00"
                },
                "CTkScrollableFrame": {
                    "fg_color": "#1a1a1a",
                    "scrollbar_button_color": "#00ff00",
                    "scrollbar_button_hover_color": "#00cc00"
                },
                "CTkTextbox": {
                    "fg_color": "#1a1a1a",
                    "text_color": "#ffffff",
                    "scrollbar_button_color": "#00ff00",
                    "scrollbar_button_hover_color": "#00cc00"
                },
                "CTkOptionMenu": {
                    "fg_color": "#1a1a1a",
                    "button_color": "#00cc00",
                    "button_hover_color": "#00ff00",
                    "text_color": "#ffffff"
                },
                "CTkSlider": {
                    "fg_color": "#1a1a1a",
                    "progress_color": "#00cc00",
                    "button_color": "#00ff00",
                    "button_hover_color": "#00cc00"
                },
                "CTkSwitch": {
                    "fg_color": "#1a1a1a",
                    "progress_color": "#00cc00",
                    "button_color": "#00ff00",
                    "button_hover_color": "#00cc00"
                }
            }
        }
    
    def get_theme(self, theme_name):
        """Získa tému podľa názvu"""
        return self.themes.get(theme_name, self.themes["quantum_green"])
    
    def setup_ultimate_theme(self):
        """Nastaví ultimate tému pre celú aplikáciu"""
        try:
            # Nastavíme CustomTkinter theme
            ctk.set_appearance_mode("dark")
            
            # Vytvoríme custom theme pre CustomTkinter
            custom_theme = {
                "CTk": {
                    "fg_color": ["#0a0a0a", "#0a0a0a"],
                    "top_fg_color": ["#1a1a1a", "#1a1a1a"],
                    "text_color": ["#ffffff", "#ffffff"]
                },
                "CTkScrollbar": {
                    "fg_color": ["#1a1a1a", "#1a1a1a"],
                    "button_color": ["#00ff00", "#00ff00"],
                    "button_hover_color": ["#00cc00", "#00cc00"]
                },
                "CTkScrollableFrame": {
                    "fg_color": ["#1a1a1a", "#1a1a1a"],
                    "scrollbar_button_color": ["#00ff00", "#00ff00"],
                    "scrollbar_button_hover_color": ["#00cc00", "#00cc00"]
                },
                "CTkTextbox": {
                    "fg_color": ["#1a1a1a", "#1a1a1a"],
                    "text_color": ["#ffffff", "#ffffff"],
                    "scrollbar_button_color": ["#00ff00", "#00ff00"],
                    "scrollbar_button_hover_color": ["#00cc00", "#00cc00"]
                }
            }
            
            # Nastavíme custom theme
            ctk.ThemeManager._theme = custom_theme
            print("✅ Ultimate theme nastavená")
            
        except Exception as e:
            print(f"⚠️ Chyba pri nastavovaní témy: {e}")
            # Fallback na základné nastavenie
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("green")

# Globálna inštancia
theme_manager = ThemeManager()