import subprocess
import sys

def install_voice_dependencies():
    """Nainštaluje potrebné balíky pre hlasové ovládanie"""
    packages = [
        "speechrecognition",
        "pyttsx3",
        "pyaudio"
    ]
    
    print("🔧 Inštalácia hlasových závislostí...")
    
    for package in packages:
        try:
            print(f"📦 Inštalácia {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} nainštalovaný")
        except subprocess.CalledProcessError as e:
            print(f"❌ Chyba pri inštalácii {package}: {e}")
    
    print("🎉 Hlasové závislosti boli nainštalované!")
    print("🔊 Skontrolujte, či máte mikrofón a reproduktory zapojené.")

if __name__ == "__main__":
    install_voice_dependencies()
    input("Stlačte Enter pre ukončenie...")