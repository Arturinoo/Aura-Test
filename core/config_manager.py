import json
import os
from typing import Dict, Any

class ConfigManager:
    def __init__(self):
        self.config_dir = "config"
        self.settings_file = os.path.join(self.config_dir, "settings.json")
        self.ensure_config_files()
    
    def ensure_config_files(self):
        """Zabezpečí, že konfiguračné súbory existujú"""
        os.makedirs(self.config_dir, exist_ok=True)
        
        default_settings = {
            "ai": {
                "local_model": "qwen2:7b",
                "temperature": 0.7,
                "max_tokens": 1000
            },
            "voice": {
                "enabled": True,
                "language": "sk-SK"
            }
        }
        
        if not os.path.exists(self.settings_file):
            self.save_settings(default_settings)
    
    def load_settings(self) -> Dict[str, Any]:
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {
                "ai": {"local_model": "qwen2:7b"},
                "voice": {"enabled": True}
            }
    
    def save_settings(self, settings: Dict[str, Any]):
        with open(self.settings_file, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)