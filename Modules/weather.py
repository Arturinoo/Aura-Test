# modules/weather.py
import requests
import asyncio

class Weather:
    def __init__(self):
        self.supported_commands = [
            "počasie", "predpoveď počasia", "teplota", "vlhkosť", "dnes počasia"
        ]
        self.api_key = "YOUR_API_KEY"  # Zadarmo z openweathermap.org
    
    def can_handle(self, command: str) -> bool:
        return any(cmd in command.lower() for cmd in self.supported_commands)
    
    async def handle(self, command: str) -> str:
        try:
            # Jednoduchá extrakcia mesta
            city = "Bratislava"  # Default - mohli by sme extrahovať z príkazu
            if "v " in command.lower():
                parts = command.lower().split("v ")
                if len(parts) > 1:
                    city = parts[1].split()[0]
            
            return await self.get_weather(city)
        except Exception as e:
            return f"❌ Chyba pri získavaní počasia: {str(e)}"
    
    async def get_weather(self, city: str) -> str:
        """Získa informácie o počasí"""
        try:
            # Poznámka: Potrebuješ API kľúč z openweathermap.org
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric&lang=sk"
            
            response = await asyncio.get_event_loop().run_in_executor(
                None, lambda: requests.get(url, timeout=10)
            )
            
            if response.status_code == 200:
                data = response.json()
                temp = data['main']['temp']
                humidity = data['main']['humidity']
                description = data['weather'][0]['description']
                city_name = data['name']
                
                return f"🌤️ **Počasie v {city_name}:**\n- Teplota: {temp}°C\n- Vlivosť: {humidity}%\n- Stav: {description}"
            else:
                return "❌ Nepodarilo sa získať informácie o počasí"
                
        except Exception as e:
            return f"❌ Chyba pri komunikácii s weather API: {str(e)}"