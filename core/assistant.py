import ollama
from typing import Dict, Any, List, Callable
import importlib
import os
import time
from .voice_engine import VoiceEngine  # ✅ PRIDANÉ
try:
    from modules.gmail_manager import GmailManager
except ImportError:
    print("⚠️  GmailManager nie je dostupný")

class AIAssistant:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.model_name = "qwen3"  # Upravte podľa vášho modelu
        self.modules = {}
        self.voice_engine = VoiceEngine()  # ✅ PRIDANÉ

        self.gmail_manager = None
        try:
            self.gmail_manager = GmailManager()
        except Exception as e:
            print(f"⚠️  Nepodarilo sa inicializovať GmailManager: {e}")
        
        # PRIDANÉ: Konverzačný stav
        self.conversation_context = {
            'history': [],  # História konverzácie
            'current_topic': None,  # Aktuálna téma
            'mentioned_entities': set(),  # Spomenuté entity
            'user_preferences': {},  # Používateľské preferencie
            'last_intent': None  # Posledný rozpoznaný zámer
        }
        
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
        """Spracuj príkaz od používateľa s využitím kontextu"""
        try:
            print(f"🔍 Spracovávam príkaz: {command}")
            
            # Spracuj hlasové hotkeys
            if command.startswith("🔧 HOTKEY:"):
                return await self.process_hotkey(command)
            
            # Získaj kontextový súhrn
            context_summary = self.get_context_summary()
            
            # Najprv skús nájsť špecifický modul pre príkaz
            for module_name, module_instance in self.modules.items():
                if hasattr(module_instance, 'can_handle') and module_instance.can_handle(command):
                    print(f"🔧 Používam modul: {module_name}")
                    response = await module_instance.handle(command)
                    # Aktualizuj kontext
                    self.update_conversation_context(command, response, f"module_{module_name}")
                    return response
            
            # Ak žiaden modul nevie spracovať, použi AI s kontextom
            print("🤖 Používam AI model...")
            response = await self._ask_ai_with_context(command, context_summary)
            # Aktualizuj kontext
            self.update_conversation_context(command, response, "ai_general")
            return response
            
        except Exception as e:
            error_msg = f"❌ Chyba pri spracovaní príkazu: {str(e)}"
            self.update_conversation_context(command, error_msg, "error")
            return error_msg
    
    async def _ask_ai_with_context(self, prompt: str, context_summary: str) -> str:
        """Komunikácia s Ollama modelom s kontextom"""
        try:
            # Vytvor prompt s kontextom
            if context_summary:
                contextual_prompt = f"""Predchádzajúca konverzácia:
{context_summary}

Aktuálna otázka: {prompt}

Odpovedaj prirodzene, berúc do úvahy predchádzajúci kontext. Ak sa používateľ pýta na niečo, čo už bolo spomenuté, použij históriu."""
            else:
                contextual_prompt = prompt
            
            response = ollama.chat(
                model=self.model_name,
                messages=[{'role': 'user', 'content': contextual_prompt}]
            )
            return response['message']['content']
        except Exception as e:
            return f"❌ Chyba pri komunikácii s AI: {str(e)}"
    
    # PRIDANÉ: Metódy pre správu konverzačného stavu
    def update_conversation_context(self, user_input, ai_response, detected_intent=None):
        """
        Aktualizuje konverzačný kontext na základe novej výmeny
        """
        # Pridaj do histórie
        self.conversation_context['history'].append({
            'user': user_input,
            'ai': ai_response,
            'timestamp': time.time(),
            'intent': detected_intent
        })
        
        # Obmedz veľkosť histórie (zachová posledných 20 výmen)
        if len(self.conversation_context['history']) > 20:
            self.conversation_context['history'] = self.conversation_context['history'][-20:]
        
        # Aktualizuj posledný zámer
        if detected_intent:
            self.conversation_context['last_intent'] = detected_intent
        
        # Extrahuj entity (jednoduchá verzia)
        self._extract_entities(user_input)
        
        # Aktualizuj aktuálnu tému
        self._update_current_topic(user_input, ai_response)
    
    def _extract_entities(self, text):
        """
        Jednoduchá extrakcia entít z textu
        """
        words = text.split()
        
        # Jednoduchá detekcia mien (veľké písmeno na začiatku slova)
        for word in words:
            if (len(word) > 2 and word[0].isupper() and 
                word not in ['Ahoj', 'Čau', 'Dobrý', 'Dobrý', 'Deň', 'Večer', 'Ráno']):
                self.conversation_context['mentioned_entities'].add(word)
    
    def _update_current_topic(self, user_input, ai_response):
        """
        Aktualizuje aktuálnu tému konverzácie
        """
        # Jednoduchá detekcia témy na základe kľúčových slov
        topic_keywords = {
            'počasie': ['počasie', 'teplota', 'dážď', 'slnko', 'teplo', 'zima', 'teplota'],
            'systém': ['systém', 'pamäť', 'cpu', 'bateria', 'disk', 'procesor', 'ram'],
            'súbory': ['súbor', 'priečinok', 'otvor', 'čítaj', 'zapisovať', 'adresár'],
            'web': ['internet', 'hľadať', 'prehľadávať', 'stránka', 'web', 'vyhľadaj'],
            'kód': ['kód', 'program', 'script', 'python', 'funkcia', 'class']
        }
        
        input_lower = user_input.lower()
        for topic, keywords in topic_keywords.items():
            if any(keyword in input_lower for keyword in keywords):
                self.conversation_context['current_topic'] = topic
                return
        
        # Ak sa nenašla žiadna téma, ponechaj predchádzajúcu
    
    def get_context_summary(self):
        """
        Vráti súhrn kontextu pre AI model
        """
        if not self.conversation_context['history']:
            return ""
        
        # Zostav kontextový súhrn z posledných niekoľkých výmen
        recent_history = self.conversation_context['history'][-3:]  # Posledné 3 výmeny
        context_lines = []
        
        for exchange in recent_history:
            context_lines.append(f"Používateľ: {exchange['user']}")
            context_lines.append(f"Asistent: {exchange['ai']}")
        
        summary = "\n".join(context_lines)
        
        # Pridaj informácie o aktuálnej téme
        if self.conversation_context['current_topic']:
            summary += f"\nAktuálna téma: {self.conversation_context['current_topic']}"
        
        # Pridaj dôležité entity
        if self.conversation_context['mentioned_entities']:
            entities = ", ".join(list(self.conversation_context['mentioned_entities'])[:3])
            summary += f"\nSpomenuté: {entities}"
        
        return summary
    
    def get_conversation_stats(self):
        """Vráti štatistiky konverzácie pre UI"""
        return {
            'message_count': len(self.conversation_context['history']),
            'current_topic': self.conversation_context['current_topic'],
            'mentioned_entities': list(self.conversation_context['mentioned_entities'])[:5],
            'has_context': len(self.conversation_context['history']) > 0,
            'last_intent': self.conversation_context['last_intent']
        }
    
    def clear_conversation_context(self):
        """
        Vymaže konverzačný kontext (nová konverzácia)
        """
        self.conversation_context = {
            'history': [],
            'current_topic': None,
            'mentioned_entities': set(),
            'user_preferences': {},
            'last_intent': None
        }
        print("🔄 Konverzačný kontext vymazaný - nová konverzácia")
    
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
            elif action == "clear_context":
                self.clear_conversation_context()
                return "🔄 Kontext konverzácie vymazaný"
            else:
                return f"ℹ️  Neznámy hotkey: {action}"
                
        except Exception as e:
            return f"❌ Chyba pri spracovaní hotkey: {str(e)}"
    
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
        self.voice_engine.speak(text)
    
    def get_voice_status(self) -> dict:
        """Vráti stav hlasového engine"""
        return self.voice_engine.get_voice_status()
    
    def update_voice_settings(self):
        """Aktualizuje hlasové nastavenia"""
        # Táto metóda môže byť implementovaná neskôr
        pass