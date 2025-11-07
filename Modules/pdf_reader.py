import os
import asyncio

class PdfReader:
    def __init__(self):
        self.supported_commands = [
            "čítaj pdf", "otvor pdf", "analyzuj pdf", "pdf informácie"
        ]
        print("✅ PdfReader inicializovaný")
    
    def can_handle(self, command: str) -> bool:
        return any(cmd in command.lower() for cmd in self.supported_commands)
    
    async def handle(self, command: str) -> str:
        try:
            if "čítaj pdf" in command.lower() or "otvor pdf" in command.lower():
                return self.find_pdf_files()
            elif "analyzuj pdf" in command.lower():
                return "🔧 Analýza PDF bude dostupná po nainštalovaní PyPDF2"
            else:
                return f"ℹ️  Príkaz '{command}' ešte nie je implementovaný v PdfReadere"
        except Exception as e:
            return f"❌ Chyba v PdfReadere: {str(e)}"
    
    def find_pdf_files(self) -> str:
        """Nájde PDF súbory v aktuálnom priečinku"""
        try:
            current_dir = os.getcwd()
            pdf_files = [f for f in os.listdir(current_dir) if f.lower().endswith('.pdf')]
            
            if not pdf_files:
                return "📁 V aktuálnom priečinku nie sú žiadne PDF súbory."
            
            result = f"📄 **PDF súbory v '{current_dir}':**\n"
            for pdf in pdf_files:
                size = os.path.getsize(pdf)
                result += f"- {pdf} ({size} bajtov)\n"
            
            result += "\n💡 Pre čítanie PDF nainštalujte: pip install PyPDF2"
            return result
            
        except Exception as e:
            return f"❌ Chyba pri hľadaní PDF súborov: {str(e)}"