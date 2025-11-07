#!/usr/bin/env python3
"""
Hlavný spúšťací súbor pre AI Assistant Windows aplikáciu
"""

import sys
import os

def check_dependencies():
    """Skontroluje potrebné závislosti"""
    try:
        import customtkinter
        import ollama
        return True
    except ImportError as e:
        print(f"❌ Chýbajúce závislosti: {e}")
        return False

def main():
    """Hlavná funkcia"""
    print("🚀 Spúštam AI Assistant...")
    
    # Pridaj aktuálny priečinok do Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(current_dir)
    
    if not check_dependencies():
        print("📦 Inštaluj závislosti: pip install -r requirements.txt")
        input("Stlač Enter pre ukončenie...")
        return
    
    try:
        from app import AIAssistantApp
        print("✅ Všetky závislosti sú nainštalované!")
        print("🖥️  Spúštam grafickú aplikáciu...")
        app = AIAssistantApp()
        app.run()
    except Exception as e:
        print(f"❌ Neočakávaná chyba: {e}")
        import traceback
        traceback.print_exc()
        input("Stlač Enter pre ukončenie...")

if __name__ == "__main__":
    main()