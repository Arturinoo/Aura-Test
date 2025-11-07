import customtkinter as ctk
import os
import sys

# Pridaj aktuálny priečinok do Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from core.assistant import AIAssistant
from core.config_manager import ConfigManager
from ui.main_window import MainWindow

class AIAssistantApp:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.assistant = AIAssistant(self.config_manager)
        
    def run(self):
        """Spustí aplikáciu s hlavným oknom"""
        try:
            print("🖥️ Vytváram hlavné okno...")
            self.main_window = MainWindow(self.assistant, self.config_manager)
            print("🚀 Spúšťam aplikáciu...")
            self.main_window.mainloop()
        except Exception as e:
            print(f"❌ Chyba pri spustení GUI: {e}")
            import traceback
            traceback.print_exc()

def main():
    app = AIAssistantApp()
    app.run()

if __name__ == "__main__":
    main()