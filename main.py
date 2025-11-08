# main.py - QUANTUM EDITION (vylepšená)
import sys
import os
import customtkinter as ctk
import traceback

def main():
    try:
        print("🌀 Spúšťam Aura AI Assistant - Quantum Edition...")
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, current_dir)
        
        # Nastav Ultimate theme PRVÉ
        from ui.themes import theme_manager
        theme_manager.setup_ultimate_theme()
        
        # Import komponentov AŽ POTOM
        from core.config_manager import ConfigManager
        from core.assistant import AIAssistant
        
        print("🔮 Inicializujem Quantum komponenty...")
        config_manager = ConfigManager()
        assistant = AIAssistant(config_manager)
        
        # Skontroluj či AI funguje
        try:
            test_response = assistant.process_command_sync("test")
            print(f"✅ AI test: {test_response[:50]}...")
        except Exception as e:
            print(f"⚠️ AI test failed: {e}")
        
        print("🎨 Vytváram Quantum rozhranie...")
        from ui.main_window import QuantumMainWindow
        app = QuantumMainWindow(assistant, config_manager)
        
        print("✅ Quantum aplikácia úspešne inicializovaná!")
        print("🚀 Spúšťam hlavnú slučku...")
        
        # Spustenie aplikácie
        app.mainloop()
        
    except ImportError as e:
        print(f"💥 Chyba importu: {e}")
        traceback.print_exc()
        input("Stlačte Enter pre ukončenie...")
        
    except Exception as e:
        print(f"💥 Neočakávaná chyba: {e}")
        traceback.print_exc()
        input("Stlačte Enter pre ukončenie...")

if __name__ == '__main__':
    main()