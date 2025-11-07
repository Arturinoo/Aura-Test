# app.py - AI Assistant hlavná aplikácia
import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow  # alebo podľa tvojho skutočného importu

class AIAssistantApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = MainWindow()
        
    def run(self):
        self.main_window.show()
        return self.app.exec_()

if __name__ == '__main__':
    assistant = AIAssistantApp()
    sys.exit(assistant.run())