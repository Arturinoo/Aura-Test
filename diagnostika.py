import os
import sys

print("🔍 Diagnostika štruktúry priečinkov...")
print("=" * 50)

# Získaj aktuálnu cestu
current_dir = os.path.dirname(os.path.abspath(__file__))
print(f"📁 Aktuálny priečinok: {current_dir}")

# Skontroluj štruktúru priečinkov
required_dirs = ["core", "modules", "config"]
required_files = ["main.py", "app.py"]

print("\n📋 Kontrola priečinkov:")
for dir_name in required_dirs:
    dir_path = os.path.join(current_dir, dir_name)
    exists = os.path.exists(dir_path)
    print(f"  {dir_name}: {'✅ EXISTUJE' if exists else '❌ CHÝBA'} - {dir_path}")
    
    if exists:
        files = os.listdir(dir_path)
        print(f"    Súbory: {files}")

print("\n📋 Kontrola súborov:")
for file_name in required_files:
    file_path = os.path.join(current_dir, file_name)
    exists = os.path.exists(file_path)
    print(f"  {file_name}: {'✅ EXISTUJE' if exists else '❌ CHÝBA'} - {file_path}")

print("\n🐍 Python sys.path:")
for i, path in enumerate(sys.path[:5]):  # Len prvých 5 ciest
    print(f"  {i}: {path}")

print("\n🔍 Pokus o import core.assistant...")
try:
    # Pridaj aktuálny priečinok do sys.path
    sys.path.insert(0, current_dir)
    
    from core.assistant import AIAssistant
    print("✅ ✅ ✅ IMPORT core.assistant ÚSPEŠNÝ!")
    
    # Test vytvorenia inštancie
    assistant = AIAssistant()
    print("✅ ✅ ✅ VYTVORENIE AIAssistant ÚSPEŠNÉ!")
    
except ImportError as e:
    print(f"❌ ❌ ❌ IMPORT ZLYHAL: {e}")
    print("\n💡 Možné riešenia:")
    print("1. Skontroluj, či existuje súbor core/assistant.py")
    print("2. Skontroluj, či core/assistant.py obsahuje triedu AIAssistant")
    print("3. Skontroluj, či v core/assistant.py nie sú chyby syntaxe")
except Exception as e:
    print(f"❌ Iná chyba: {e}")

input("\nStlač Enter pre ukončenie...")