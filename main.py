# main.py - PurpleAura Edition (stabilná verzia)
import sys
import os
import customtkinter as ctk

def main():
    try:
        print("✨ Spúšťam Aura AI Assistant - PurpleAura Edition...")
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, current_dir)
        
        # ✅ OPRAVENÉ: Jednoduchšia inicializácia CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")  # Použijeme dark-blue ako základ
        
        # Import komponentov
        from core.config_manager import ConfigManager
        from core.assistant import AIAssistant
        from ui.main_window import MainWindow
        
        print("🔮 Inicializujem PurpleAura komponenty...")
        config_manager = ConfigManager()
        assistant = AIAssistant(config_manager)
        
        print("🎨 Vytváram PurpleAura rozhranie...")
        app = MainWindow(assistant, config_manager)
        
        print("✅ PurpleAura aplikácia úspešne inicializovaná!")
        print("🚀 Spúšťam hlavnú slučku...")
        
        # Spustenie aplikácie
        app.mainloop()
        
    except Exception as e:
        print(f"💥 Chyba pri spustení aplikácie: {e}")
        import traceback
        traceback.print_exc()
        input("Stlačte Enter pre ukončenie...")

if __name__ == '__main__':
    main()