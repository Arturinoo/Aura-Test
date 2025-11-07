# app.py - AI Assistant hlavná aplikácia
import sys
import os
import customtkinter as ctk  # ✅ Zmena: Použijeme CustomTkinter namiesto PyQt5

class AIAssistantApp:
    def __init__(self):
        # ✅ OPRAVENÉ: Inicializácia CustomTkinter namiesto PyQt5
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Import a vytvorenie inštancií
        try:
            print("🔍 Inicializujem ConfigManager...")
            from core.config_manager import ConfigManager
            self.config_manager = ConfigManager()
            print("✅ ConfigManager inicializovaný")
            
            print("🔍 Inicializujem AIAssistant...")
            from core.assistant import AIAssistant
            self.assistant = AIAssistant(self.config_manager)
            print("✅ AIAssistant inicializovaný")
            
            print("🔍 Inicializujem MainWindow...")
            from ui.main_window import MainWindow
            self.main_window = MainWindow(self.assistant, self.config_manager)
            print("✅ MainWindow inicializovaný")
            
        except ImportError as e:
            print(f"❌ Chyba importu: {e}")
            self.show_error_dialog(f"Chyba importu: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Iná chyba: {e}")
            import traceback
            traceback.print_exc()
            self.show_error_dialog(f"Chyba: {e}")
            sys.exit(1)
        
    def show_error_dialog(self, message):
        """Zobrazí chybové dialógové okno"""
        # ✅ OPRAVENÉ: Použijeme Tkinter messagebox
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()  # Skryjeme hlavné okno
        messagebox.showerror("Chyba", message)
        root.destroy()
        
    def run(self):
        """Spustí aplikáciu - Tkinter používa mainloop() namiesto show()"""
        # ✅ OPRAVENÉ: mainloop() namiesto show()
        if hasattr(self.main_window, 'mainloop'):
            return self.main_window.mainloop()
        else:
            print("❌ MainWindow nemá metódu mainloop()")
            return 0

if __name__ == '__main__':
    app = AIAssistantApp()
    sys.exit(app.run())