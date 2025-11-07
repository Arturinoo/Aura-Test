import sys
import os
sys.path.append(os.path.dirname(__file__))

print("🔍 Diagnostika UI...")

# Skontrolujte existenciu súborov
ui_files = [
    "ui/__init__.py",
    "ui/main_window.py", 
    "ui/chat_tab.py",
    "ui/modules_tab.py",
    "ui/settings_tab.py",
    "ui/styles.py"
]

for file in ui_files:
    exists = os.path.exists(file)
    print(f"{'✅' if exists else '❌'} {file}")

# Skúste importovať
try:
    from ui.main_window import MainWindow
    print("✅ MainWindow importovaný")
except Exception as e:
    print(f"❌ Chyba importu MainWindow: {e}")

try:
    from ui.modules_tab import ModulesTab
    print("✅ ModulesTab importovaný")
except Exception as e:
    print(f"❌ Chyba importu ModulesTab: {e}")

input("Stlač Enter pre pokračovanie...")