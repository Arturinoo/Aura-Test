import requests

class WebTools:
    def __init__(self):
        self.supported_commands = [
            "skontroluj internet", "ping server", "webová stránka", "http status"
        ]
        print("✅ WebTools inicializovaný")
    
    def can_handle(self, command: str) -> bool:
        return any(cmd in command.lower() for cmd in self.supported_commands)
    
    async def handle(self, command: str) -> str:
        try:
            if "skontroluj internet" in command.lower():
                return await self.check_internet_connection()
            elif "ping server" in command.lower():
                return await self.ping_website(command)
            else:
                return f"ℹ️  Príkaz '{command}' ešte nie je implementovaný v WebTools"
        except Exception as e:
            return f"❌ Chyba v WebTools: {str(e)}"
    
    async def check_internet_connection(self) -> str:
        try:
            response = requests.get("https://www.google.com", timeout=5)
            if response.status_code == 200:
                return "✅ Internetové pripojenie je funkčné"
            else:
                return "⚠️  Internetové pripojenie môže mať problémy"
        except Exception:
            return "❌ Nie je dostupné internetové pripojenie"
    
    async def ping_website(self, command: str) -> str:
        try:
            parts = command.split()
            url = None
            for i, part in enumerate(parts):
                if part in ["ping", "server"] and i + 1 < len(parts):
                    url = parts[i + 1]
                    if not url.startswith(('http://', 'https://')):
                        url = 'https://' + url
                    break
            
            if not url:
                return "❌ Zadajte URL: 'ping server example.com'"
            
            response = requests.get(url, timeout=10)
            return f"🌐 **Stav servera {url}:**\\n- HTTP Status: {response.status_code}\\n- Čas odozvy: {response.elapsed.total_seconds():.2f}s"
            
        except requests.exceptions.Timeout:
            return f"❌ Časový limit pre URL {url} vypršal"
        except Exception as e:
            return f"❌ Chyba pri pingovaní servera: {str(e)}"
