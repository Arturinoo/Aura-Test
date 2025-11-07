@echo off
echo Inštalácia závislostí pre AI Assistant...
echo.

cd /d "C:\Aura Test"

"c:/Users/Milujem Štetky/AppData/Local/Programs/Python/Python314/python.exe" -m pip install --upgrade pip

echo Inštalácia customtkinter...
"c:/Users/Milujem Štetky/AppData/Local/Programs/Python/Python314/python.exe" -m pip install customtkinter

echo Inštalácia ostatných závislostí...
"c:/Users/Milujem Štetky/AppData/Local/Programs/Python/Python314/python.exe" -m pip install ollama speechrecognition pyttsx3 requests pillow psutil watchdog python-dotenv pyyaml

echo.
echo ✅ Inštalácia dokončená!
echo.
pause