# ui/quantum_chat_tab.py - VYLEPŠENÁ VERZIA
import customtkinter as ctk
from customtkinter import CTkScrollableFrame
from .themes import theme_manager
import time
import threading
import asyncio
import json
import os
from datetime import datetime

class QuantumChatTab(ctk.CTkFrame):
    def __init__(self, parent, assistant, config_manager):
        self.theme = theme_manager.get_theme("quantum_green")
        super().__init__(parent, fg_color=self.theme["bg"], corner_radius=0, border_width=0)
        
        self.assistant = assistant
        self.config_manager = config_manager
        self.is_listening = False
        self.message_history = []
        self.conversation_context = []
        
        self.setup_quantum_chat_ui()
        self.setup_chat_animations()
        self.load_chat_history()
    
    def setup_quantum_chat_ui(self):
        """Vytvorí kompletný quantum chat interface"""
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Hlavný kontajner
        main_container = ctk.CTkFrame(
            self,
            fg_color=self.theme["bg"],
            corner_radius=0,
            border_width=0
        )
        main_container.grid(row=0, column=0, sticky="nsew")
        main_container.grid_rowconfigure(1, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        
        # Header
        self.setup_chat_header(main_container)
        
        # Chat obsah
        self.setup_chat_content(main_container)
        
        # Vstupná časť
        self.setup_chat_input(main_container)
    
    def setup_chat_header(self, parent):
        """Vytvorí header chatu"""
        header = ctk.CTkFrame(
            parent,
            height=80,
            fg_color=self.theme["bg_secondary"],
            corner_radius=0,
            border_width=0
        )
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        
        # Názov a stav
        title_frame = ctk.CTkFrame(header, fg_color="transparent", border_width=0)
        title_frame.pack(side="left", padx=30, pady=20)
        
        ctk.CTkLabel(
            title_frame,
            text="🌌 QUANTUM CHAT",
            font=("Segoe UI", 20, "bold"),
            text_color=self.theme["accent_glow"]
        ).pack(anchor="w")
        
        self.chat_status = ctk.CTkLabel(
            title_frame,
            text="🟢 Connected to Quantum AI",
            font=("Consolas", 10),
            text_color=self.theme["success"]
        )
        self.chat_status.pack(anchor="w")
        
        # Rýchle akcie
        action_frame = ctk.CTkFrame(header, fg_color="transparent", border_width=0)
        action_frame.pack(side="right", padx=30, pady=20)
        
        quick_actions = [
            ("🧹 Clear", self.clear_chat_memory),
            ("💾 Save", self.save_chat_history),
            ("📊 Stats", self.show_chat_analytics)
        ]
        
        for text, command in quick_actions:
            btn = ctk.CTkButton(
                action_frame,
                text=text,
                command=command,
                width=80,
                height=30,
                fg_color=self.theme["accent_secondary"],
                hover_color=self.theme["accent_glow"],
                font=("Segoe UI", 10),
                corner_radius=8
            )
            btn.pack(side="left", padx=5)
    
    def setup_chat_content(self, parent):
        """Vytvorí obsahovú časť chatu"""
        content_frame = ctk.CTkFrame(parent, fg_color="transparent", border_width=0)
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=3)
        content_frame.grid_columnconfigure(1, weight=1)
        
        # Hlavný chat
        self.setup_chat_messages(content_frame)
        
        # Sidebar
        self.setup_chat_sidebar(content_frame)
    
    def setup_chat_messages(self, parent):
        """Vytvorí priestor pre správy"""
        chat_container = ctk.CTkFrame(
            parent,
            fg_color=self.theme["bg_tertiary"],
            corner_radius=20,
            border_width=2,
            border_color=self.theme["accent_secondary"]
        )
        chat_container.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        chat_container.grid_rowconfigure(0, weight=1)
        chat_container.grid_columnconfigure(0, weight=1)
        
        # Scrollovateľná oblasť správ
        self.messages_frame = ctk.CTkScrollableFrame(
            chat_container,
            fg_color="transparent",
            scrollbar_button_color=self.theme["accent_secondary"],
            scrollbar_button_hover_color=self.theme["accent_glow"]
        )
        self.messages_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Úvodná správa
        self.add_welcome_message()
    
    def setup_chat_sidebar(self, parent):
        """Vytvorí sidebar s nástrojmi"""
        sidebar = ctk.CTkFrame(
            parent,
            fg_color=self.theme["bg_secondary"],
            corner_radius=20,
            border_width=2,
            border_color=self.theme["accent_secondary"]
        )
        sidebar.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
        
        ctk.CTkLabel(
            sidebar,
            text="QUANTUM TOOLS",
            font=("Segoe UI", 16, "bold"),
            text_color=self.theme["accent_glow"]
        ).pack(pady=20)
        
        # Rýchle príkazy
        quick_commands = [
            ("📁 File Manager", "Otvoriť správcu súborov"),
            ("🖥️ System Info", "Zobraziť systémové informácie"),
            ("🌤️ Počasie", "Zobraziť predpoveď počasia"),
            ("📧 Emaily", "Skontrolovať emaily")
        ]
        
        for cmd_text, cmd_desc in quick_commands:
            cmd_frame = ctk.CTkFrame(sidebar, fg_color=self.theme["bg_tertiary"], corner_radius=10)
            cmd_frame.pack(fill="x", padx=15, pady=8)
            
            ctk.CTkButton(
                cmd_frame,
                text=cmd_text,
                command=lambda ct=cmd_text: self.send_quick_command(ct),
                height=40,
                fg_color="transparent",
                hover_color=self.theme["accent_secondary"],
                font=("Segoe UI", 12),
                corner_radius=8
            ).pack(fill="x", padx=5, pady=5)
            
            ctk.CTkLabel(
                cmd_frame,
                text=cmd_desc,
                font=("Segoe UI", 9),
                text_color=self.theme["text_secondary"]
            ).pack(pady=(0, 5))
    
    def setup_chat_input(self, parent):
        """Vytvorí vstupnú časť"""
        input_frame = ctk.CTkFrame(
            parent,
            height=120,
            fg_color=self.theme["bg_secondary"],
            corner_radius=0,
            border_width=0
        )
        input_frame.grid(row=2, column=0, sticky="ew")
        input_frame.grid_propagate(False)
        input_frame.grid_columnconfigure(0, weight=1)
        
        # Vstupné pole
        self.message_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Napíšte svoju správu... alebo použite hlasové príkazy",
            height=50,
            font=("Segoe UI", 14),
            border_color=self.theme["accent_secondary"],
            fg_color=self.theme["bg_tertiary"],
            text_color=self.theme["text_primary"],
            corner_radius=15
        )
        self.message_entry.grid(row=0, column=0, padx=20, pady=15, sticky="ew")
        self.message_entry.bind("<Return>", self.send_message)
        
        # Tlačidlá
        button_frame = ctk.CTkFrame(input_frame, fg_color="transparent", border_width=0)
        button_frame.grid(row=0, column=1, padx=20, pady=15)
        
        # Hlasové tlačidlo
        self.voice_button = ctk.CTkButton(
            button_frame,
            text="🎤 Hlas",
            command=self.toggle_voice,
            width=100,
            height=50,
            fg_color=self.theme["accent_secondary"],
            hover_color=self.theme["accent_glow"],
            font=("Segoe UI", 14, "bold"),
            corner_radius=10
        )
        self.voice_button.pack(side="left", padx=5)
        
        # Odoslať tlačidlo
        self.send_button = ctk.CTkButton(
            button_frame,
            text="🚀 Odoslať",
            command=self.send_message,
            width=100,
            height=50,
            fg_color=self.theme["accent"],
            hover_color=self.theme["accent_glow"],
            font=("Segoe UI", 14, "bold"),
            corner_radius=10
        )
        self.send_button.pack(side="left", padx=5)
    
    def add_welcome_message(self):
        """Pridá uvítaciu správu"""
        welcome_text = """🌌 VITAJTE V QUANTUM CHATE

Som váš Quantum AI asistent, pripravený pomôcť s:

• 🤖 Pokročilé AI konverzácie
• 📧 Správa emailov  
• 🔧 Systémové operácie
• 📁 Správa súborov
• 🎨 Tvorivé úlohy

Čo by ste chceli preskúmať?"""
        
        self.add_message("assistant", welcome_text, is_welcome=True)
    
    def add_message(self, sender, text, is_welcome=False):
        """Pridá správu do chatu"""
        message_frame = ctk.CTkFrame(
            self.messages_frame,
            fg_color="transparent",
            corner_radius=15,
            border_width=0
        )
        message_frame.pack(fill="x", padx=10, pady=8)
        
        if sender == "user":
            bg_color = self.theme["accent_secondary"]
            text_color = self.theme["text_primary"]
            justify = "right"
            padx_config = (100, 20)
        else:
            if is_welcome:
                bg_color = self.theme["accent"]
            else:
                bg_color = self.theme["bg_secondary"]
            text_color = self.theme["text_primary"]
            justify = "left"
            padx_config = (20, 100)
        
        # Správa
        message_bubble = ctk.CTkFrame(
            message_frame,
            fg_color=bg_color,
            corner_radius=20,
            border_width=2,
            border_color=self.theme["accent_glow"] if is_welcome else self.theme["border"]
        )
        
        if sender == "user":
            message_bubble.pack(side="right", padx=padx_config)
        else:
            message_bubble.pack(side="left", padx=padx_config)
        
        message_label = ctk.CTkLabel(
            message_bubble,
            text=text,
            wraplength=600,
            justify=justify,
            font=("Segoe UI", 12),
            text_color=text_color
        )
        message_label.pack(padx=20, pady=15)
        
        # Časová pečiatka
        timestamp = datetime.now().strftime("%H:%M:%S")
        time_label = ctk.CTkLabel(
            message_frame,
            text=timestamp,
            font=("Consolas", 9),
            text_color=self.theme["text_secondary"]
        )
        
        if sender == "user":
            time_label.pack(side="right", padx=(0, 30))
        else:
            time_label.pack(side="left", padx=(30, 0))
        
        # Ulož do histórie
        self.message_history.append({
            "sender": sender,
            "text": text,
            "timestamp": timestamp,
            "is_welcome": is_welcome,
            "datetime": datetime.now().isoformat()
        })
        
        # Auto-scroll
        self.messages_frame._parent_canvas.yview_moveto(1.0)
        
        # Animácia príchodu
        self.animate_message_appear(message_bubble)
        
        # Ulož históriu
        self.save_chat_history()
    
    def animate_message_appear(self, widget):
        """Animácia objavenia správy"""
        def animate(step=0):
            if step >= 10:
                return
            try:
                alpha = step * 25
                widget.configure(fg_color=widget.cget("fg_color"))
                widget.after(50, lambda: animate(step + 1))
            except:
                pass
        
        animate()
    
    def send_message(self, event=None):
        """Odošle správu"""
        message = self.message_entry.get().strip()
        if not message:
            return
        
        # Pridaj správu používateľa
        self.add_message("user", message)
        self.message_entry.delete(0, "end")
        
        # Zobraz indikátor premýšľania
        self.show_thinking_indicator()
        
        # Spracuj správu
        threading.Thread(target=self.process_message, args=(message,), daemon=True).start()
    
    def send_quick_command(self, command):
        """Odošle rýchly príkaz"""
        self.message_entry.delete(0, "end")
        self.message_entry.insert(0, command)
        self.send_message()
    
    def show_thinking_indicator(self):
        """Zobrazí indikátor premýšľania"""
        thinking_frame = ctk.CTkFrame(
            self.messages_frame,
            fg_color=self.theme["bg_secondary"],
            corner_radius=20,
            border_width=2,
            border_color=self.theme["accent_glow"]
        )
        thinking_frame.pack(fill="x", padx=20, pady=10)
        
        thinking_text = ctk.CTkLabel(
            thinking_frame,
            text="🌀 Quantum AI premýšľa...",
            font=("Segoe UI", 12, "italic"),
            text_color=self.theme["accent_glow"]
        )
        thinking_text.pack(pady=15)
        
        self.thinking_indicator = thinking_frame
        self.animate_thinking(thinking_text)
    
    def animate_thinking(self, widget):
        """Animácia premýšľania"""
        def animate(dots=0):
            try:
                text = "🌀 Quantum AI premýšľa" + "." * (dots % 4)
                widget.configure(text=text)
                widget.after(500, lambda: animate(dots + 1))
            except:
                pass
        
        animate()
    
    def process_message(self, message):
        """Spracuje správu pomocou AI assistant"""
        try:
            # Použij existujúci assistant na spracovanie
            if hasattr(self.assistant, 'process_command_sync'):
                response = self.assistant.process_command_sync(message)
            else:
                # Fallback ak metóda neexistuje
                response = f"🤖 AI Response to: {message}\n\nToto je simulovaná odpoveď. Skutočná AI integrácia bude čoskoro dostupná."
            
            # Skry indikátor a pridaj odpoveď
            self.after(0, self.hide_thinking)
            self.after(0, lambda: self.add_message("assistant", response))
            
        except Exception as e:
            error_msg = f"❌ Chyba pri spracovaní: {str(e)}"
            self.after(0, self.hide_thinking)
            self.after(0, lambda: self.add_message("assistant", error_msg))
    
    def hide_thinking(self):
        """Skryje indikátor premýšľania"""
        try:
            self.thinking_indicator.destroy()
        except:
            pass
    
    def toggle_voice(self):
        """Prepne hlasové ovládanie"""
        self.is_listening = not self.is_listening
        
        if self.is_listening:
            self.voice_button.configure(
                text="🔴 Počúva",
                fg_color=self.theme["error"],
                hover_color="#FF6666"
            )
            self.add_message("assistant", "🎤 Hlasová aktivácia povolená. Počúvam...")
        else:
            self.voice_button.configure(
                text="🎤 Hlas",
                fg_color=self.theme["accent_secondary"],
                hover_color=self.theme["accent_glow"]
            )
            self.add_message("assistant", "🔇 Hlasová aktivácia vypnutá.")
    
    def clear_chat_memory(self):
        """Vymaže históriu chatu"""
        for widget in self.messages_frame.winfo_children():
            widget.destroy()
        self.message_history.clear()
        self.add_welcome_message()
        self.add_message("assistant", "🧠 História chatu bola vymazaná!")
    
    def save_chat_history(self):
        """Uloží históriu chatu"""
        try:
            chat_data = {
                "timestamp": datetime.now().isoformat(),
                "messages": self.message_history
            }
            
            # Vytvor priečinok pre históriu ak neexistuje
            os.makedirs("chat_history", exist_ok=True)
            
            filename = f"chat_history/quantum_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(chat_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"Chyba pri ukladaní histórie: {e}")
    
    def load_chat_history(self):
        """Načíta históriu chatu"""
        try:
            # Tu by sa načítala posledná história
            pass
        except:
            pass
    
    def show_chat_analytics(self):
        """Zobrazí štatistiky chatu"""
        user_messages = len([m for m in self.message_history if m["sender"] == "user"])
        assistant_messages = len([m for m in self.message_history if m["sender"] == "assistant"])
        total_chars = sum(len(m["text"]) for m in self.message_history)
        
        analytics_text = f"""📊 ŠTATISTIKY CHATU

• Celkom správ: {len(self.message_history)}
• Vaše správy: {user_messages}
• AI odpovede: {assistant_messages}
• Celkový počet znakov: {total_chars}
• Dĺžka konverzácie: Aktívna

Quantum analýza dokončená!"""
        
        self.add_message("assistant", analytics_text)
    
    def setup_chat_animations(self):
        """Nastaví animácie chatu"""
        self.animate_chat_status()
    
    def animate_chat_status(self):
        """Animácia stavu chatu"""
        def animate():
            try:
                current_color = self.chat_status.cget("text_color")
                if current_color == self.theme["success"]:
                    new_color = self.theme["accent_glow"]
                else:
                    new_color = self.theme["success"]
                
                self.chat_status.configure(text_color=new_color)
                self.after(1000, animate)
            except:
                pass
        
        animate()