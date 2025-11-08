# modules/help_module.py
import asyncio

class HelpModule:
    """Modul pre zobrazenie nápovedy a príkazov"""
    
    def __init__(self):
        self.supported_commands = [
            "pomoc", "help", "nápoveda", "príkazy", "commands",
            "zoznam príkazov", "list commands", "čo vieš", "what can you do",
            "moduly", "modules", "funkcie", "functions"
        ]
        print("✅ HelpModule inicializovaný")
    
    def can_handle(self, command: str) -> bool:
        return any(cmd in command.lower() for cmd in self.supported_commands)
    
    async def handle(self, command: str) -> str:
        try:
            command_lower = command.lower()
            
            if "modul" in command_lower or "module" in command_lower:
                return await self.show_modules_help()
            elif "príkaz" in command_lower or "command" in command_lower:
                return await self.show_commands_help()
            else:
                return await self.show_general_help()
                
        except Exception as e:
            return f"❌ Chyba pri zobrazení nápovedy: {str(e)}"
    
    async def show_general_help(self) -> str:
        """Zobrazí všeobecnú nápovedu"""
        help_text = """🎯 **VŠEOBECNÁ NÁPOVEDA - AURA AI ASSISTANT**

**Dostupné kategórie príkazov:**

📁 **SPRÁVA SÚBOROV**
• Vytváranie, mazanie, premenovávanie súborov a zložiek
• Čítanie a zápis do súborov
• Vyhľadávanie a analýza súborov

📧 **EMAIL FUNKCIE** 
• Pripojenie k Gmail účtu
• Čítanie a odosielanie emailov
• Organizácia a vyhľadávanie emailov

🖥️ **SYSTÉMOVÉ NÁSTROJE**
• Informácie o systéme a hardvéri
• Sledovanie výkonu a batérie
• Správa procesov a siete

🌐 **WEBOVÉ NÁSTROJE**
• Kontrola internetového pripojenia
• Testovanie serverov a webstránok

🤖 **AI A KÓD**
• Analýza Python kódu
• Komunikácia s AI modelom

**Špeciálne príkazy:**
• `pomoc` - Táto nápoveda
• `príkazy` - Zoznam všetkých príkazov
• `moduly` - Informácie o moduloch

Pre podrobný zoznam príkazov povedz 'príkazy' alebo navštív '🔮 MODULES' v aplikácii!"""
        
        return help_text
    
    async def show_commands_help(self) -> str:
        """Zobrazí podrobný zoznam príkazov"""
        # Tento text sa dynamicky naplní z modulov
        return "📚 Pre úplný zoznam príkazov navštív záložku '📚 Príkazová príručka' v MODULES sekcii aplikácie. Tam nájdeš všetky dostupné príkazy zoradené podľa modulov!"
    
    async def show_modules_help(self) -> str:
        """Zobrazí informácie o moduloch"""
        return "🔮 Pre prehľad modulov a ich funkcií navštív záložku '📦 Nainštalované' v MODULES sekcii aplikácie. Každý modul má zoznam svojich príkazov!"