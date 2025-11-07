import os

class CodeAnalyzer:
    def __init__(self):
        self.supported_commands = [
            "analyzuj kód", "skontroluj kód", "optimalizuj kód", "code analysis"
        ]
        print("✅ CodeAnalyzer inicializovaný")
    
    def can_handle(self, command: str) -> bool:
        return any(cmd in command.lower() for cmd in self.supported_commands)
    
    async def handle(self, command: str) -> str:
        try:
            if "analyzuj kód" in command.lower() or "skontroluj kód" in command.lower():
                return self.analyze_current_directory()
            elif "optimalizuj kód" in command.lower():
                return "🔧 Optimalizácia kódu bude dostupná čoskoro..."
            else:
                return f"ℹ️  Príkaz '{command}' ešte nie je implementovaný v CodeAnalyzere"
        except Exception as e:
            return f"❌ Chyba v CodeAnalyzere: {str(e)}"
    
    def analyze_current_directory(self) -> str:
        try:
            current_dir = os.getcwd()
            python_files = [f for f in os.listdir(current_dir) if f.endswith('.py')]
            
            if not python_files:
                return "📁 V aktuálnom priečinku nie sú žiadne Python súbory na analýzu."
            
            analysis = f"📊 **Analýza Python súborov v '{current_dir}':**\\n"
            analysis += f"- Nájdených {len(python_files)} Python súborov\\n"
            
            for file in python_files:
                file_path = os.path.join(current_dir, file)
                size = os.path.getsize(file_path)
                lines = self.count_lines(file_path)
                analysis += f"  - {file}: {lines} riadkov, {size} bajtov\\n"
            
            analysis += "\\n🔍 Funkcia pre hlbšiu analýzu kódu bude dostupná čoskoro..."
            return analysis
            
        except Exception as e:
            return f"❌ Chyba pri analýze kódu: {str(e)}"
    
    def count_lines(self, file_path: str) -> int:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return len(f.readlines())
        except:
            return 0
