import json
import os
from typing import Dict, Any

class ConfigManager:
    def __init__(self):
        self.config_dir = "config"
        self.settings_file = os.path.join(self.config_dir, "settings.json")
        self.models_file = os.path.join(self.config_dir, "models.json")
        self.voice_file = os.path.join(self.config_dir, "voice_config.json")
        
        self.default_settings = {
            "ai": {
                "local_model": "qwen3",
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
            "ui": {  # ✅ PRIDANÉ UI NASTAVENIA
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
        
        self.ensure_config_files()
    
    def ensure_config_files(self):
        """Zabezpečí, že konfiguračné súbory existujú"""
        os.makedirs(self.config_dir, exist_ok=True)
        
        if not os.path.exists(self.settings_file):
            self.save_settings(self.default_settings)
        
        if not os.path.exists(self.models_file):
            self.save_models({"available_models": ["qwen3", "llama2", "mistral"]})
    
    def load_settings(self) -> Dict[str, Any]:
        """Načíta nastavenia s fallback na predvolené hodnoty"""
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                loaded_settings = json.load(f)
            
            # Zlúči načítané nastavenia s predvolenými (pre nové kľúče)
            return self.merge_settings(self.default_settings, loaded_settings)
            
        except Exception as e:
            print(f"❌ Chyba pri načítaní nastavení: {e}, používam predvolené")
            return self.default_settings
    
    def merge_settings(self, default: Dict, loaded: Dict) -> Dict:
        """Rekurzívne zlúči nastavenia, aby sa zachovali nové kľúče"""
        result = default.copy()
        
        for key, value in loaded.items():
            if key in result:
                if isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = self.merge_settings(result[key], value)
                else:
                    result[key] = value
            else:
                result[key] = value
                
        return result
    
    def save_settings(self, settings: Dict[str, Any]):
        """Uloží nastavenia do súboru"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4, ensure_ascii=False)
            print("✅ Nastavenia uložené")
        except Exception as e:
            print(f"❌ Chyba pri ukladaní nastavení: {e}")
    
    def load_models(self) -> Dict[str, Any]:
        try:
            with open(self.models_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {"available_models": ["qwen3"]}
    
    def save_models(self, models: Dict[str, Any]):
        with open(self.models_file, 'w', encoding='utf-8') as f:
            json.dump(models, f, indent=4, ensure_ascii=False)