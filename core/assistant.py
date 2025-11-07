import ollama
from typing import Dict, Any, List
import importlib
import os
from .voice_engine import VoiceEngine  # ✅ PRIDANÉ

class AIAssistant:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.model_name = "qwen3"  # Upravte podľa vášho modelu
        self.modules = {}
        self.voice_engine = VoiceEngine(config_manager)  # ✅ PRIDANÉ
        self.load_modules()
        print("✅ AIAssistant inicializovaný s modelom:", self.model_name)
        
    def load_modules(self):
        """Načítaj všetky dostupné moduly"""
        modules_dir = "modules"
        if not os.path.exists(modules_dir):
            print("❌ Priečinok modules neexistuje - vytváram...")
            os.makedirs(modules_dir, exist_ok=True)
            return
            
        print(f"🔍 Hľadám moduly v {modules_dir}...")
        
        for filename in os.listdir(modules_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]  # Odstráni .py
                try:
                    print(f"🔧 Načítavam modul: {module_name}")
                    
                    # Dynamický import
                    spec = importlib.util.spec_from_file_location(module_name, f"modules/{filename}")
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # Nájdeme hlavnú triedu (predpokladáme, že má rovnaký názov ako súbor)
                    class_name = module_name.title().replace('_', '')
                    if hasattr(module, class_name):
                        module_class = getattr(module, class_name)
                        self.modules[module_name] = module_class()
                        print(f"✅ Načítaný modul: {module_name}")
                    else:
                        print(f"⚠️  Modul {module_name} nemá triedu {class_name}")
                        
                except Exception as e:
                    print(f"❌ Chyba pri načítaní modulu {module_name}: {e}")
    
    async def process_command(self, command: str) -> str:
        """Spracuj príkaz od používateľa"""
        try:
            print(f"🔍 Spracovávam príkaz: {command}")
            
            # Spracuj hlasové hotkeys
            if command.startswith("🔧 HOTKEY:"):
                return await self.process_hotkey(command)
            
            # Najprv skús nájsť špecifický modul pre príkaz
            for module_name, module_instance in self.modules.items():
                if hasattr(module_instance, 'can_handle') and module_instance.can_handle(command):
                    print(f"🔧 Používam modul: {module_name}")
                    return await module_instance.handle(command)
            
            # Ak žiaden modul nevie spracovať, použi AI
            print("🤖 Používam AI model...")
            return await self._ask_ai(command)
            
        except Exception as e:
            return f"❌ Chyba pri spracovaní príkazu: {str(e)}"
    
    async def process_hotkey(self, hotkey_command: str) -> str:
        """Spracuje hlasové hotkeys"""
        try:
            action = hotkey_command.replace("🔧 HOTKEY:", "").strip()
            
            if action == "stop":
                self.voice_engine.stop_speaking()
                return "🔇 Prehováranie zastavené"
            elif action == "cancel":
                self.voice_engine.stop_listening()
                return "🔇 Počúvanie zrušené"
            elif action == "help":
                help_text = """
🎙️ **Hlasové príkazy:**
- "Zastav" - zastaví prehováranie
- "Zruš" - zruší počúvanie  
- "Pomoc" - zobrazí túto nápovedu
- "Asistent" - wake-word pre aktiváciu
"""
                return help_text
            else:
                return f"ℹ️  Neznámy hotkey: {action}"
                
        except Exception as e:
            return f"❌ Chyba pri spracovaní hotkey: {str(e)}"
    
    async def _ask_ai(self, prompt: str) -> str:
        """Komunikácia s Ollama modelom"""
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[{'role': 'user', 'content': prompt}]
            )
            return response['message']['content']
        except Exception as e:
            return f"❌ Chyba pri komunikácii s AI: {str(e)}"
    
    def start_voice_listening(self, callback: Callable[[str], None]):
        """Spustí nepretržité hlasové počúvanie"""
        settings = self.config_manager.load_settings()
        wake_word = settings.get("voice", {}).get("wake_word", "asistent")
        self.voice_engine.listen_continuous(callback, wake_word)
    
    def stop_voice_listening(self):
        """Zastaví hlasové počúvanie"""
        self.voice_engine.stop_listening()
    
    def speak_response(self, text: str):
        """Prehovorí odpoveď"""
        self.voice_engine.speak_async(text)
    
    def get_voice_status(self) -> dict:
        """Vráti stav hlasového engine"""
        return self.voice_engine.get_voice_status()
    
    def update_voice_settings(self):
        """Aktualizuje hlasové nastavenia"""
        self.voice_engine.update_settings()