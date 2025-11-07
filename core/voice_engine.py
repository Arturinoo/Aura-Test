import threading
import queue
import time
from typing import Callable, Optional

try:
    import speechrecognition as sr
    import pyttsx3
    HAS_VOICE_DEPS = True
except ImportError:
    HAS_VOICE_DEPS = False
    print("❌ Hlasové knižnice nie sú nainštalované. Hlasové funkcie budú obmedzené.")

class VoiceEngine:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.command_queue = queue.Queue()
        self.is_listening = False
        self.is_speaking = False
        self.wake_word_detected = False
        self.current_theme = "dark"
        
        if HAS_VOICE_DEPS:
            self.setup_voice()
        else:
            print("⚠️  VoiceEngine beží v obmedzenom režime")
        
        self.setup_hotkeys()
        
    def setup_voice(self):
        """Nastaví hlasový engine ak sú knižnice dostupné"""
        if not HAS_VOICE_DEPS:
            return
            
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            self.tts_engine = pyttsx3.init()
            
            # Nastav hlas pre text-to-speech
            voices = self.tts_engine.getProperty('voices')
            if voices:
                self.tts_engine.setProperty('voice', voices[0].id)
            
            settings = self.config_manager.load_settings()
            speech_rate = settings.get("voice", {}).get("speech_rate", 150)
            self.tts_engine.setProperty('rate', speech_rate)
            self.tts_engine.setProperty('volume', 0.8)
            
            print("✅ VoiceEngine inicializovaný")
            
        except Exception as e:
            print(f"❌ Chyba pri inicializácii VoiceEngine: {e}")
    
    def setup_hotkeys(self):
        """Nastaví hlasové hotkeys"""
        self.hotkeys = {
            "stop": ["zastav", "stop", "prestaň", "koniec"],
            "cancel": ["zruš", "cancel", "zrušiť"],
            "help": ["pomoc", "help", "nápoveda"]
        }
    
    def listen(self, timeout: int = 5) -> str:
        """Počúva hlasový príkaz"""
        if not self.is_voice_enabled():
            return "Hlasové ovládanie je vypnuté"
        
        if not HAS_VOICE_DEPS:
            return "Hlasové knižnice nie sú nainštalované"
        
        try:
            with self.microphone as source:
                print("🎤 Prispôsobujem sa šumu...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("🎤 Počúvam...")
                
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                
            print("🔍 Prepisujem reč...")
            text = self.recognizer.recognize_google(audio, language="sk-SK")
            print(f"📝 Rozpoznané: {text}")
            
            return text
            
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return "❌ Nerozpoznal som reč"
        except sr.RequestError as e:
            return f"❌ Chyba služby: {e}"
        except Exception as e:
            return f"❌ Neočakávaná chyba: {e}"
    
    def process_hotkeys(self, text: str) -> str:
        """Spracuje hlasové hotkeys"""
        text_lower = text.lower()
        
        for action, keywords in self.hotkeys.items():
            if any(keyword in text_lower for keyword in keywords):
                return f"🔧 HOTKEY: {action}"
        
        return text
    
    def speak(self, text: str, wait: bool = False):
        """Prehovorí text"""
        if not text or self.is_speaking or not HAS_VOICE_DEPS:
            return
        
        self.is_speaking = True
        
        def speak_worker():
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"❌ Chyba pri prehováraní: {e}")
            finally:
                self.is_speaking = False
        
        thread = threading.Thread(target=speak_worker, daemon=True)
        thread.start()
        
        if wait:
            thread.join()
    
    def speak_async(self, text: str):
        """Prehovorí text asynchrónne"""
        self.speak(text, wait=False)
    
    def stop_speaking(self):
        """Zastaví prehováranie"""
        if not HAS_VOICE_DEPS:
            return
            
        try:
            self.tts_engine.stop()
            self.is_speaking = False
            print("🔇 Prehováranie zastavené")
        except:
            pass
    
    def is_voice_enabled(self) -> bool:
        """Skontroluje, či je hlasové ovládanie povolené"""
        if not HAS_VOICE_DEPS:
            return False
            
        settings = self.config_manager.load_settings()
        return settings.get("voice", {}).get("enabled", True)
    
    def update_settings(self):
        """Aktualizuje nastavenia z configu"""
        if not HAS_VOICE_DEPS:
            return
            
        settings = self.config_manager.load_settings()
        voice_settings = settings.get("voice", {})
        
        if "speech_rate" in voice_settings:
            self.tts_engine.setProperty('rate', voice_settings["speech_rate"])
        
        print("✅ Hlasové nastavenia aktualizované")
    
    def get_voice_status(self) -> dict:
        """Vráti stav hlasového engine"""
        return {
            "listening": self.is_listening,
            "speaking": self.is_speaking,
            "wake_word_detected": self.wake_word_detected,
            "enabled": self.is_voice_enabled(),
            "dependencies_available": HAS_VOICE_DEPS
        }