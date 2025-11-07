import os
import json
import sys

def fix_config():
    """Opraví chýbajúce nastavenia v config súboroch"""
    config_dir = "config"
    settings_file = os.path.join(config_dir, "settings.json")
    
    # Predvolené nastavenia s UI sekciou
    default_settings = {
        "ai": {
            "local_model": "qwen2:7b",
            "cloud_model": "gpt-4", 
            "use_cloud": False,
            "temperature": 0.7,
            "max_tokens": 1000
        },
        "voice": {
            "enabled": True,
            "wake_word": "asistent",
            "language": "sk-SK",
            "speech_rate": 150
        },
        "ui": {
            "theme": "dark",
            "font_size": 12,
            "window_width": 1400,
            "window_height": 900,
            "sidebar_width": 200
        },
        "modules": {
            "file_manager": True,
            "code_analyzer": True,
            "system_tools": True,
            "web_tools": False
        }
    }
    
    # Vytvor priečinok ak neexistuje
    os.makedirs(config_dir, exist_ok=True)
    
    # Načítaj existujúce nastavenia alebo vytvor nové
    if os.path.exists(settings_file):
        try:
            with open(settings_file, 'r', encoding='utf-8') as f:
                existing_settings = json.load(f)
            
            # Zlúč s predvolenými nastaveniami
            merged_settings = merge_settings(default_settings, existing_settings)
            
            # Ulož opravené nastavenia
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(merged_settings, f, indent=4, ensure_ascii=False)
            
            print("✅ Konfiguračný súbor bol opravený - pridaná UI sekcia")
            
        except Exception as e:
            print(f"❌ Chyba pri oprave konfigurácie: {e}")
            # Vytvor nový súbor s predvolenými nastaveniami
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(default_settings, f, indent=4, ensure_ascii=False)
            print("✅ Vytvorený nový konfiguračný súbor")
    else:
        # Vytvor nový súbor
        with open(settings_file, 'w', encoding='utf-8') as f:
            json.dump(default_settings, f, indent=4, ensure_ascii=False)
        print("✅ Vytvorený nový konfiguračný súbor s UI nastaveniami")

def merge_settings(default, existing):
    """Rekurzívne zlúči nastavenia"""
    result = default.copy()
    
    for key, value in existing.items():
        if key in result:
            if isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = merge_settings(result[key], value)
            else:
                result[key] = value
        else:
            result[key] = value
            
    return result

if __name__ == "__main__":
    print("🔧 Opravujem konfiguráciu...")
    fix_config()
    print("\n🚀 Skúste spustiť aplikáciu znova: python app.py")
    input("Stlačte Enter pre ukončenie...")