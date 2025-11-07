import os
import shutil

class FileManager:
    def __init__(self):
        self.supported_commands = [
            "vytvor zložku", "vytvor priečinok", "zmaž súbor",
            "premenuj súbor", "zobraz obsah priečinka", "zoznam súborov"
        ]
        print("✅ FileManager inicializovaný")
    
    def can_handle(self, command: str) -> bool:
        return any(cmd in command.lower() for cmd in self.supported_commands)
    
    async def handle(self, command: str) -> str:
        command_lower = command.lower()
        
        if "vytvor zložku" in command_lower or "vytvor priečinok" in command_lower:
            return self.create_folder(command)
        elif "zobraz obsah" in command_lower or "zoznam súborov" in command_lower:
            return self.list_directory(command)
        elif "zmaž súbor" in command_lower:
            return self.delete_file(command)
        else:
            return f"ℹ️  Príkaz '{command}' ešte nie je implementovaný v FileManageri"
    
    def create_folder(self, command: str) -> str:
        try:
            parts = command.split()
            if len(parts) >= 3:
                folder_name = parts[2]
                os.makedirs(folder_name, exist_ok=True)
                return f"✅ Zložka '{folder_name}' bola úspešne vytvorená"
            else:
                return "❌ Zadaj názov zložky: 'vytvor zložku [názov]'"
        except Exception as e:
            return f"❌ Chyba pri vytváraní zložky: {str(e)}"
    
    def list_directory(self, command: str) -> str:
        try:
            current_dir = os.getcwd()
            items = os.listdir(current_dir)
            
            folders = [f"📁 {item}" for item in items if os.path.isdir(item)]
            files = [f"📄 {item}" for item in items if os.path.isfile(item)]
            
            response = f"📂 Obsah priečinka '{current_dir}':\n"
            response += "\n".join(folders + files)
            return response
        except Exception as e:
            return f"❌ Chyba pri zobrazovaní obsahu: {str(e)}"
    
    def delete_file(self, command: str) -> str:
        try:
            parts = command.split()
            if len(parts) >= 3:
                file_name = parts[2]
                if os.path.exists(file_name):
                    os.remove(file_name)
                    return f"✅ Súbor '{file_name}' bol úspešne vymazaný"
                else:
                    return f"❌ Súbor '{file_name}' neexistuje"
            else:
                return "❌ Zadaj názov súboru: 'zmaž súbor [názov]'"
        except Exception as e:
            return f"❌ Chyba pri mazaní súboru: {str(e)}"