import speech_recognition as sr
import pyttsx3
import threading

class VoiceEngine:
    def __init__(self):
        self.is_available = False
        self.is_listening = False
        self.listening_thread = None
        
        # Skús inicializovať rozpoznávanie reči
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            self.is_available = True
            print("✅ Hlasové knižnice sú nainštalované.")
        except Exception as e:
            print("❌ Hlasové knižnice nie sú nainštalované. Hlasové funkcie budú obmedzené.")
            self.is_available = False

        # Inicializácia text-to-speech
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 150)
            self.tts_engine.setProperty('volume', 0.8)
        except:
            self.tts_engine = None

    def speak(self, text):
        if not self.is_available or self.tts_engine is None:
            print(f"🔊 (TTS) {text}")
            return
        
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"❌ Chyba pri prehrávaní hlasu: {e}")

    def listen(self):
        if not self.is_available:
            print("❌ Hlasové knižnice nie sú nainštalované. Nepodporuje sa rozpoznávanie reči.")
            return None
        
        try:
            with self.microphone as source:
                print("🎤 Počúvam...")
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=5)
            
            text = self.recognizer.recognize_google(audio, language="sk-SK")
            print(f"🎤 Rozpoznané: {text}")
            return text
        except sr.WaitTimeoutError:
            print("❌ Časový limit pre počúvanie vypršal.")
            return None
        except Exception as e:
            print(f"❌ Chyba pri rozpoznávaní reči: {e}")
            return None

    def listen_continuous(self, callback, wake_word="aura"):
        """
        Spustí nepretržité počúvanie s wake word
        """
        if not self.is_available:
            print("❌ Hlasové knižnice nie sú nainštalované. Nepodporuje sa nepretržité počúvanie.")
            return
        
        def listening_loop():
            self.is_listening = True
            print("🎤 Nepretržité počúvanie spustené... Povedz 'aura' pre aktiváciu.")
            
            while self.is_listening:
                try:
                    # Počúvaj pre wake word
                    with self.microphone as source:
                        self.recognizer.adjust_for_ambient_noise(source)
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                    
                    try:
                        text = self.recognizer.recognize_google(audio, language="sk-SK").lower()
                        print(f"🔍 Rozpoznané: {text}")
                        
                        # Skontroluj wake word
                        if wake_word.lower() in text:
                            print("✅ Wake word rozpoznané! Počúvam príkaz...")
                            # Počúvaj príkaz
                            with self.microphone as source:
                                self.recognizer.adjust_for_ambient_noise(source)
                                audio = self.recognizer.listen(source, timeout=5)
                            command = self.recognizer.recognize_google(audio, language="sk-SK")
                            callback(command)
                            
                    except Exception as e:
                        # Ignoruj chyby rozpoznávania
                        continue
                        
                except Exception as e:
                    # Timeout je normálny, pokračuj v slučke
                    if "timeout" not in str(e).lower():
                        print(f"❌ Chyba pri počúvaní: {e}")
        
        # Spusti počúvanie v samostatnom vlákne
        self.listening_thread = threading.Thread(target=listening_loop, daemon=True)
        self.listening_thread.start()

    def stop_listening(self):
        self.is_listening = False
        if self.listening_thread:
            self.listening_thread.join(timeout=1)

    def get_voice_status(self):
        """
        Vráti stav hlasového engine pre UI
        """
        if not self.is_available:
            return {
                "status": "nedostupné",
                "message": "Hlasové knižnice nie sú nainštalované",
                "listening": False,
                "wake_word_detected": False,
                "speaking": False
            }
        elif self.is_listening:
            return {
                "status": "počúva",
                "message": "Nepretržité počúvanie aktívne",
                "listening": True,
                "wake_word_detected": False,
                "speaking": False
            }
        else:
            return {
                "status": "dostupné",
                "message": "Hlasové funkcie pripravené",
                "listening": False,
                "wake_word_detected": False,
                "speaking": False
            }