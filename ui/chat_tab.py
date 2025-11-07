import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import asyncio
import threading
import time
from typing import Callable

class ChatTab:
    def __init__(self, parent, assistant, config_manager):
        self.parent = parent
        self.assistant = assistant
        self.config_manager = config_manager
        self.is_listening = False
        self.setup_ui()
        
    def setup_ui(self):
        # Hlavný kontejner
        self.main_frame = ctk.CTkFrame(self.parent)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Nadpis - menší a kompaktnejší
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Aura Chat", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.title_label.pack(pady=(0, 5))
        
        # Rám pre chat správu - VIAC MIESTA PRE CHAT
        self.chat_container = ctk.CTkFrame(self.main_frame)
        self.chat_container.pack(fill="both", expand=True, pady=(0, 5))
        
        # Scrollovateľný rám pre správy - VYŠŠI
        self.chat_frame = ctk.CTkScrollableFrame(
            self.chat_container, 
            scrollbar_button_color="#2b2b2b",
            scrollbar_button_hover_color="#3b3b3b",
            height=600  # ZVÝŠENÁ VÝŠKA
        )
        self.chat_frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Indikátor "AI premýšľa" - kompaktnejší
        self.thinking_indicator = ctk.CTkFrame(self.chat_frame, height=20, fg_color="transparent")
        self.thinking_label = ctk.CTkLabel(
            self.thinking_indicator,
            text="🤔 AI premýšľa...",
            font=ctk.CTkFont(size=11),
            text_color="#888888"
        )
        self.thinking_label.pack(pady=2)
        self.thinking_indicator.pack_forget()
        
        # Vstupný rám - VYŠŠI pre väčšie tlačidlá
        self.input_frame = ctk.CTkFrame(self.main_frame, height=90)  # Zvýšené na 90
        self.input_frame.pack(fill="x", pady=(0, 5))
        self.input_frame.pack_propagate(False)
        
        # Textové pole pre vstup
        self.input_text = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Napíšte svoju správu...",
            height=35,
            font=ctk.CTkFont(size=12)
        )
        self.input_text.pack(fill="x", padx=10, pady=(10, 8))
        self.input_text.bind("<Return>", self.send_message)
        
        # Tlačidlový rám - VIAC PRIESTORU PRE TLAČIDLÁ
        self.button_frame = ctk.CTkFrame(self.input_frame, fg_color="transparent", height=40)
        self.button_frame.pack(fill="x", padx=10, pady=(0, 10))
        self.button_frame.pack_propagate(False)
        
        # Stav hlasového ovládania - POSUNUTÉ DOĽAVA
        self.voice_status = ctk.CTkLabel(
            self.button_frame,
            text="Hlas: Vypnutý",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#666666"
        )
        self.voice_status.pack(side="left", padx=(0, 10))
        
        # Tlačidlo hlasového ovládania - VÄČŠIE A LEPŠIE VIDITEĽNÉ
        self.voice_button = ctk.CTkButton(
            self.button_frame,
            text="🎤 Zapnut hlas",
            command=self.toggle_voice_listening,
            width=140,  # Širšie
            height=36,  # Vyššie
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#2b5b7c",
            hover_color="#1e4159",
            corner_radius=8
        )
        self.voice_button.pack(side="right", padx=(8, 0))
        
        # Tlačidlo odoslať - VÄČŠIE A LEPŠIE VIDITEĽNÉ
        self.send_button = ctk.CTkButton(
            self.button_frame,
            text="Odoslať",
            command=self.send_message,
            width=110,  # Širšie
            height=36,  # Vyššie
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#2b7c5b",
            hover_color="#1e5941",
            corner_radius=8
        )
        self.send_button.pack(side="right", padx=(8, 0))
        
        # Inicializácia chatu
        self.add_welcome_message()
        
    def add_welcome_message(self):
        """Pridá uvítaciu správu do chatu"""
        welcome_text = """👋 Vitajte v Aura Assistant!

Môžete:
- Pýtať sa na systémové informácie
- Prehľadávať súbory
- Čítať PDF dokumenty
- Zisťovať počasie
- Používať hlasové ovládanie

Jednoducho napíšte svoju otázku..."""
        
        self.add_message("assistant", welcome_text, is_welcome=True)
    
    def add_message(self, sender: str, text: str, is_welcome: bool = False):
        """Pridá správu do chatu - NOVÉ FARBY"""
        message_frame = ctk.CTkFrame(
            self.chat_frame, 
            fg_color="transparent",
            corner_radius=12
        )
        message_frame.pack(fill="x", padx=3, pady=1)
        
        # NOVÉ FARBY BUBLÍN:
        if sender == "user":
            # SIVÁ pre používateľa
            bg_color = "#4A5568"  # Elegantná sivá
            text_color = "white"
            justify = "right"
            padx_config = (40, 8)
        else:
            # FIALOVÁ AURA pre AI
            if is_welcome:
                bg_color = "#2b7c5b"  # Zelená pre uvítaciu správu
            else:
                bg_color = "#6D28D9"  # Krásna fialovo-modrá pre AI
            text_color = "white"
            justify = "left"
            padx_config = (8, 40)
        
        # Text správy
        message_label = ctk.CTkLabel(
            message_frame,
            text=text,
            wraplength=500,
            justify=justify,
            font=ctk.CTkFont(size=11),
            fg_color=bg_color,
            text_color=text_color,
            corner_radius=12,
            padx=12,
            pady=6
        )
        message_label.pack(side="top", padx=padx_config, pady=1)
        
        # Časová pečiatka
        timestamp = time.strftime("%H:%M")
        timestamp_label = ctk.CTkLabel(
            message_frame,
            text=timestamp,
            font=ctk.CTkFont(size=8),
            text_color="#666666"
        )
        
        if sender == "user":
            timestamp_label.pack(side="right", padx=(0, 12))
        else:
            timestamp_label.pack(side="left", padx=(12, 0))
        
        # Auto-scroll na najnovšiu správu
        self.scroll_to_bottom()
    
    def scroll_to_bottom(self):
        """Automatický scroll na spodok chatu"""
        self.chat_frame.update_idletasks()
        self.chat_frame._parent_canvas.yview_moveto(1.0)
    
    def show_thinking_indicator(self):
        """Zobrazí indikátor, že AI premýšľa"""
        self.thinking_indicator.pack(fill="x", pady=3)
        self.scroll_to_bottom()
    
    def hide_thinking_indicator(self):
        """Skryje indikátor premýšľania"""
        self.thinking_indicator.pack_forget()
    
    def send_message(self, event=None):
        """Spracuje a odošle správu"""
        message = self.input_text.get().strip()
        if not message:
            return
        
        # Pridaj správu používateľa
        self.add_message("user", message)
        self.input_text.delete(0, "end")
        
        # Zobraz indikátor premýšľania
        self.show_thinking_indicator()
        
        # Spracuj správu asynchrónne
        threading.Thread(target=self.process_message, args=(message,), daemon=True).start()
    
    def process_message(self, message: str):
        """Spracuje správu v samostatnom vlákne"""
        try:
            # Použij asyncio pre async funkcie
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            response = loop.run_until_complete(self.assistant.process_command(message))
            loop.close()
            
            # Skry indikátor a pridaj odpoveď
            self.hide_thinking_indicator()
            self.add_message("assistant", response)
            
        except Exception as e:
            self.hide_thinking_indicator()
            error_msg = f"❌ Chyba pri spracovaní: {str(e)}"
            self.add_message("assistant", error_msg)
    
    def toggle_voice_listening(self):
        """Prepína hlasové počúvanie"""
        if self.is_listening:
            self.stop_voice_listening()
        else:
            self.start_voice_listening()
    
    def start_voice_listening(self):
        """Spustí hlasové počúvanie"""
        self.is_listening = True
        self.voice_button.configure(
            text="🔴 Vypnut hlas", 
            fg_color="#7c2b2b",
            hover_color="#591e1e"
        )
        self.voice_status.configure(text="Hlas: Počúvam...", text_color="#4CAF50")
        self.assistant.start_voice_listening(self.voice_callback)
    
    def stop_voice_listening(self):
        """Zastaví hlasové počúvanie"""
        self.is_listening = False
        self.voice_button.configure(
            text="🎤 Zapnut hlas",
            fg_color="#2b5b7c", 
            hover_color="#1e4159"
        )
        self.voice_status.configure(text="Hlas: Vypnutý", text_color="#666666")
        self.assistant.stop_voice_listening()
    
    def voice_callback(self, text: str):
        """Callback pre hlasové príkazy"""
        if text:
            self.input_text.delete(0, "end")
            self.input_text.insert(0, text)
            self.send_message()
    
    def update_voice_status(self):
        """Aktualizuje stav hlasového ovládania"""
        voice_status = self.assistant.get_voice_status()
        
        if voice_status.get("listening", False):
            self.voice_status.configure(text="Hlas: Počúvam...", text_color="#4CAF50")
            self.is_listening = True
            self.voice_button.configure(
                text="🔴 Vypnut hlas",
                fg_color="#7c2b2b",
                hover_color="#591e1e"
            )
        else:
            self.voice_status.configure(text="Hlas: Vypnutý", text_color="#666666")
            self.is_listening = False
            self.voice_button.configure(
                text="🎤 Zapnut hlas",
                fg_color="#2b5b7c",
                hover_color="#1e4159"
            )

    # Metódy pre správu zobrazenia
    def pack(self, **kwargs):
        """Zabali hlavný rám pre zobrazenie"""
        self.main_frame.pack(**kwargs)

    def pack_forget(self):
        """Skryje hlavný rám"""
        self.main_frame.pack_forget()