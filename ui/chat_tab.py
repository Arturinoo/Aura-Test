import customtkinter as ctk
import threading
import asyncio
from datetime import datetime
from .styles import AppStyles
from .themes import ThemeManager

class ChatTab(ctk.CTkFrame):
    def __init__(self, parent, assistant, config_manager):
        super().__init__(parent)
        self.parent = parent
        self.assistant = assistant
        self.config_manager = config_manager
        self.messages = []
        self.current_theme = "dark"
        self.voice_listening = False
        
        self.setup_ui()
        
    def setup_ui(self):
        """Nastaví moderné chatovacie rozhranie s hlasovým ovládaním"""
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Hlavný chat kontajner
        main_chat_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_chat_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_chat_frame.grid_rowconfigure(0, weight=1)
        main_chat_frame.grid_columnconfigure(0, weight=1)
        
        # Chat history s kartovým vzhľadom
        chat_card = AppStyles.create_card(main_chat_frame)
        chat_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        chat_card.grid_rowconfigure(0, weight=1)
        chat_card.grid_columnconfigure(0, weight=1)
        
        # Nadpis chatu s hlasovými kontrolami
        header_frame = ctk.CTkFrame(chat_card, fg_color="transparent", height=60)
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        header_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(
            header_frame,
            text="💬 Konverzácia s AI",
            font=("Segoe UI", 18, "bold")
        ).grid(row=0, column=0, sticky="w")
        
        # Hlasové ovládanie
        voice_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        voice_frame.grid(row=0, column=1, sticky="e")
        
        self.voice_status_label = ctk.CTkLabel(
            voice_frame,
            text="🎤 Hlas: Vypnutý",
            font=("Segoe UI", 10),
            text_color="gray"
        )
        self.voice_status_label.pack(side="left", padx=5)
        
        self.voice_btn = ctk.CTkButton(
            voice_frame,
            text="🎤 Zapnúť Hlas",
            command=self.toggle_voice_listening,
            width=120,
            height=30,
            fg_color="#107c10",
            hover_color="#0a5a0a"
        )
        self.voice_btn.pack(side="left", padx=5)
        
        # Scrollable chat area
        self.chat_container = ctk.CTkScrollableFrame(
            chat_card,
            fg_color=ThemeManager.get_theme(self.current_theme)["bg_tertiary"]
        )
        self.chat_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        # Input area
        input_card = AppStyles.create_card(main_chat_frame)
        input_card.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        
        self.setup_input_area(input_card)
        
        # Sidebar s rýchlymi príkazmi
        self.setup_quick_commands(main_chat_frame)
        
        # Úvodná správa
        self.add_welcome_message()
        
        # Spusti aktualizáciu hlasového stavu
        self.update_voice_status()
    
    def setup_input_area(self, parent):
        """Nastaví vstupnú oblasť s hlasovými funkciami"""
        input_frame = ctk.CTkFrame(parent, fg_color="transparent")
        input_frame.pack(fill="x", padx=15, pady=15)
        
        # Vstupné pole
        self.input_entry = AppStyles.create_modern_entry(
            input_frame,
            placeholder="Napíšte príkaz alebo použite hlas...",
            height=45
        )
        self.input_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.input_entry.bind("<Return>", self.on_enter_pressed)
        
        # Tlačidlo pre odoslanie
        self.send_btn = AppStyles.create_rounded_button(
            input_frame,
            text="Odoslať",
            command=self.process_input,
            width=100,
            height=45
        )
        self.send_btn.pack(side="right", padx=(0, 10))
        
        # Tlačidlo pre hlasový vstup
        self.voice_input_btn = ctk.CTkButton(
            input_frame,
            text="🎤",
            width=50,
            height=45,
            command=self.start_voice_input,
            corner_radius=10,
            fg_color=ThemeManager.get_theme(self.current_theme)["bg_tertiary"],
            hover_color=ThemeManager.get_theme(self.current_theme)["accent"]
        )
        self.voice_input_btn.pack(side="right")
    
    def setup_quick_commands(self, parent):
        """Nastaví sidebar s rýchlymi príkazmi"""
        quick_commands_card = AppStyles.create_card(parent)
        quick_commands_card.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=(10, 0))
        
        ctk.CTkLabel(
            quick_commands_card,
            text="⚡ Rýchle Príkazy",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=15)
        
        # Hlasové príkazy
        ctk.CTkLabel(
            quick_commands_card,
            text="🎙️ Hlasové Príkazy:",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))
        
        voice_commands = [
            "Zastav - stop speaking",
            "Zruš - cancel listening", 
            "Pomoc - voice help"
        ]
        
        for cmd in voice_commands:
            ctk.CTkLabel(
                quick_commands_card,
                text=f"• {cmd}",
                font=("Segoe UI", 10),
                justify="left"
            ).pack(anchor="w", padx=15, pady=2)
        
        # Separátor
        ctk.CTkFrame(quick_commands_card, height=1).pack(fill="x", padx=10, pady=10)
        
        # AI Príkazy
        quick_commands = [
            "Vytvor zložku projektu",
            "Analyzuj aktuálny kód",
            "Systémové informácie", 
            "Zobraz bežiace procesy",
            "Test rýchlosti internetu"
        ]
        
        for cmd in quick_commands:
            btn = ctk.CTkButton(
                quick_commands_card,
                text=cmd,
                command=lambda c=cmd: self.send_quick_command(c),
                height=35,
                corner_radius=8,
                fg_color=ThemeManager.get_theme(self.current_theme)["bg_tertiary"],
                hover_color=ThemeManager.get_theme(self.current_theme)["accent"],
                text_color=ThemeManager.get_theme(self.current_theme)["text_primary"],
                anchor="w"
            )
            btn.pack(fill="x", padx=10, pady=3)
    
    def add_welcome_message(self):
        """Pridá úvodnú správu do chatu"""
        welcome_msg = """
🤖 **Vitajte v AI Assistente!**

Môžete ma požiadať o:
• 📁 **Správa súborov** - vytváranie, mazanie, premenovávanie
• 💻 **Systémové úlohy** - informácie o systéme, procesy, sieť
• 🔍 **Analýza kódu** - kontrola a optimalizácia kódu
• 🌐 **Webové úlohy** - vyhľadávanie, sťahovanie

Alebo mi jednoducho položte otázku!
"""
        self.add_message("AI Asistent", welcome_msg, "assistant")
    
    def add_message(self, sender, message, message_type="user"):
        """Pridá správu do chatu s formátovaním"""
        message_frame = ctk.CTkFrame(
            self.chat_container,
            fg_color="transparent"
        )
        message_frame.pack(fill="x", pady=8)
        
        # Urči farbu podľa typu správy
        colors = ThemeManager.get_theme(self.current_theme)
        bg_color = colors["accent"] if message_type == "user" else colors["bg_secondary"]
        text_color = colors["text_primary"]
        
        # Hlavný frame správy
        msg_card = ctk.CTkFrame(
            message_frame,
            fg_color=bg_color,
            corner_radius=15
        )
        
        if message_type == "user":
            msg_card.pack(anchor="e", fill="x", padx=(50, 0))
        else:
            msg_card.pack(anchor="w", fill="x", padx=(0, 50))
        
        # Hlavička správy
        header_frame = ctk.CTkFrame(msg_card, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(10, 5))
        
        # Meno a čas
        ctk.CTkLabel(
            header_frame,
            text=sender,
            font=("Segoe UI", 12, "bold"),
            text_color=text_color
        ).pack(side="left")
        
        ctk.CTkLabel(
            header_frame,
            text=datetime.now().strftime("%H:%M"),
            font=("Segoe UI", 10),
            text_color=ThemeManager.get_theme(self.current_theme)["text_secondary"]
        ).pack(side="right")
        
        # Text správy
        ctk.CTkLabel(
            msg_card,
            text=message,
            font=("Segoe UI", 12),
            text_color=text_color,
            wraplength=600,
            justify="left"
        ).pack(fill="x", padx=15, pady=(0, 10))
        
        # Ulož do histórie
        self.messages.append({
            "sender": sender,
            "message": message,
            "type": message_type,
            "timestamp": datetime.now()
        })
        
        # Scroll na koniec
        self.chat_container._parent_canvas.yview_moveto(1.0)
    
    # ✅ PRIDANÉ CHÝBAJÚCE METÓDY
    def on_enter_pressed(self, event):
        """Spracuje stlačenie Enter"""
        self.process_input()
        
    def process_input(self):
        """Spracuje vstup od používateľa"""
        command = self.input_entry.get().strip()
        if not command:
            return
            
        self.input_entry.delete(0, "end")
        self.add_message("Ty", command, "user")
        
        threading.Thread(target=self.process_command, args=(command,), daemon=True).start()
        
    def process_command(self, command):
        """Spracuje príkaz a zobrazí odpoveď"""
        try:
            # Vytvor nový event loop pre asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            response = loop.run_until_complete(self.assistant.process_command(command))
            loop.close()
            
            # Zobraz odpoveď v GUI vlákne
            self.after(0, lambda: self.add_message("AI Asistent", response, "assistant"))
            
        except Exception as e:
            error_msg = f"Chyba: {str(e)}"
            self.after(0, lambda: self.add_message("Systém", error_msg, "system"))
    
    def send_quick_command(self, command):
        """Pošle rýchly príkaz"""
        self.input_entry.delete(0, "end")
        self.input_entry.insert(0, command)
        self.process_input()
    
    def toggle_voice_listening(self):
        """Prepína nepretržité hlasové počúvanie"""
        if not self.voice_listening:
            self.start_continuous_listening()
        else:
            self.stop_continuous_listening()
    
    def start_continuous_listening(self):
        """Spustí nepretržité hlasové počúvanie"""
        self.voice_listening = True
        self.voice_btn.configure(
            text="🔴 Vypnúť Hlas", 
            fg_color="#e81123",
            hover_color="#a00d19"
        )
        self.voice_status_label.configure(text="🎤 Hlas: Počúva...", text_color="green")
        
        def voice_callback(command):
            if command and command not in ["", "❌ Nerozpoznal som reč"]:
                self.after(0, lambda: self.process_voice_command(command))
        
        self.assistant.start_voice_listening(voice_callback)
        self.add_message("Systém", "🎙️ Nepretržité hlasové počúvanie spustené. Povedz 'asistent' pre aktiváciu.", "system")
    
    def stop_continuous_listening(self):
        """Zastaví nepretržité hlasové počúvanie"""
        self.voice_listening = False
        self.voice_btn.configure(
            text="🎤 Zapnúť Hlas",
            fg_color="#107c10", 
            hover_color="#0a5a0a"
        )
        self.voice_status_label.configure(text="🎤 Hlas: Vypnutý", text_color="gray")
        
        self.assistant.stop_voice_listening()
        self.add_message("Systém", "🔇 Nepretržité hlasové počúvanie zastavené.", "system")
    
    def start_voice_input(self):
        """Spustí jednorazový hlasový vstup"""
        if self.voice_listening:
            self.add_message("Systém", "🎤 Už počúvam... povedz príkaz", "system")
            return
        
        self.add_message("Systém", "🎤 Počúvam... povedz príkaz", "system")
        
        def voice_worker():
            command = self.assistant.voice_engine.listen(timeout=10)
            if command and command not in ["", "❌ Nerozpoznal som reč"]:
                self.after(0, lambda: self.process_voice_command(command))
        
        threading.Thread(target=voice_worker, daemon=True).start()
    
    def process_voice_command(self, command):
        """Spracuje hlasový príkaz"""
        self.add_message("Ty (hlas)", command, "user")
        
        # Spracuj príkaz v samostatnom vlákne
        threading.Thread(
            target=self.process_command, 
            args=(command,),
            daemon=True
        ).start()
    
    def update_voice_status(self):
        """Aktualizuje stav hlasového ovládania"""
        voice_status = self.assistant.get_voice_status()
        
        status_text = "🎤 Hlas: "
        status_color = "gray"
        
        if voice_status["listening"]:
            status_text += "Počúva..."
            status_color = "green"
        elif voice_status["speaking"]:
            status_text += "Hovorí..."
            status_color = "blue"
        elif voice_status["wake_word_detected"]:
            status_text += "Aktívny"
            status_color = "orange"
        else:
            status_text += "Vypnutý"
            status_color = "gray"
        
        self.voice_status_label.configure(text=status_text, text_color=status_color)
        
        # Pokračuj v aktualizácii každú sekundu
        self.after(1000, self.update_voice_status)
    
    def clear_chat(self):
        """Vymaže chat"""
        for widget in self.chat_container.winfo_children():
            widget.destroy()
        self.messages.clear()
        self.add_welcome_message()
    
    def export_chat(self):
        """Exportuje chat (placeholder)"""
        self.add_message("Systém", "💾 Funkcia exportu bude dostupná čoskoro...", "system")