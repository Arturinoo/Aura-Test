import customtkinter as ctk
import tkinter as tk
from typing import Callable, List, Dict
import threading
import asyncio

class GmailTab:
    def __init__(self, parent, assistant, config_manager):
        self.parent = parent
        self.assistant = assistant
        self.config_manager = config_manager
        self.setup_ui()
        
    def setup_ui(self):
        # Hlavný kontejner
        self.main_frame = ctk.CTkFrame(self.parent)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Nadpis
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="📧 Gmail Manager", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(pady=(0, 10))
        
        # Stavové informácie
        self.status_frame = ctk.CTkFrame(self.main_frame)
        self.status_frame.pack(fill="x", pady=(0, 10))
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="🔒 Gmail nie je pripojený",
            font=ctk.CTkFont(size=12),
            text_color="#ff6b6b"
        )
        self.status_label.pack(side="left", padx=10, pady=5)
        
        # Tlačidlá pre operácie
        self.buttons_frame = ctk.CTkFrame(self.main_frame)
        self.buttons_frame.pack(fill="x", pady=(0, 10))
        
        self.connect_button = ctk.CTkButton(
            self.buttons_frame,
            text="🔗 Pripoj Gmail",
            command=self.connect_gmail,
            width=120,
            height=35,
            fg_color="#2b7c5b",
            hover_color="#1e5941"
        )
        self.connect_button.pack(side="left", padx=(0, 10))
        
        self.refresh_button = ctk.CTkButton(
            self.buttons_frame,
            text="🔄 Obnoviť",
            command=self.refresh_emails,
            width=100,
            height=35
        )
        self.refresh_button.pack(side="left", padx=(0, 10))
        
        self.compose_button = ctk.CTkButton(
            self.buttons_frame,
            text="📝 Nový Email",
            command=self.open_compose_window,
            width=120,
            height=35,
            fg_color="#6D28D9",
            hover_color="#5B21B6"
        )
        self.compose_button.pack(side="left", padx=(0, 10))
        
        # Vyhľadávací panel
        self.search_frame = ctk.CTkFrame(self.main_frame)
        self.search_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(self.search_frame, text="🔍 Hľadať:").pack(side="left", padx=(10, 5))
        self.search_entry = ctk.CTkEntry(self.search_frame, width=200, placeholder_text="Zadajte hľadaný výraz...")
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<Return>", lambda e: self.search_emails())
        
        self.search_button = ctk.CTkButton(
            self.search_frame,
            text="Hľadať",
            command=self.search_emails,
            width=80,
            height=30
        )
        self.search_button.pack(side="left", padx=5)
        
        # Zobrazenie emailov
        self.emails_container = ctk.CTkFrame(self.main_frame)
        self.emails_container.pack(fill="both", expand=True)
        
        self.emails_frame = ctk.CTkScrollableFrame(
            self.emails_container,
            scrollbar_button_color="#2b2b2b",
            scrollbar_button_hover_color="#3b3b3b"
        )
        self.emails_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Indikátor načítania
        self.loading_indicator = ctk.CTkFrame(self.emails_frame, height=30, fg_color="transparent")
        self.loading_label = ctk.CTkLabel(
            self.loading_indicator,
            text="⏳ Načítavam emaily...",
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        )
        self.loading_label.pack(pady=5)
        
        # Na začiatok skontrolujeme stav
        self.check_gmail_status()
    
    def check_gmail_status(self):
        """Skontroluje stav Gmail pripojenia"""
        if hasattr(self.assistant, 'gmail_manager'):
            if self.assistant.gmail_manager.authenticated:
                self.status_label.configure(text="✅ Gmail pripojený", text_color="#4CAF50")
                self.connect_button.configure(text="🔗 Pripojené", state="disabled")
                self.refresh_emails()
            else:
                self.status_label.configure(text="🔒 Gmail nie je pripojený", text_color="#ff6b6b")
    
    def connect_gmail(self):
        """Pripojí Gmail"""
        def connect_thread():
            try:
                result = self.assistant.gmail_manager.authenticate()
                self.parent.after(0, lambda: self.on_connect_result(result))
            except Exception as e:
                self.parent.after(0, lambda: self.on_connect_result(f"❌ Chyba: {str(e)}"))
        
        threading.Thread(target=connect_thread, daemon=True).start()
        self.status_label.configure(text="🔗 Pripája sa...", text_color="#FFA500")
    
    def on_connect_result(self, result: str):
        """Spracuje výsledok pripojenia"""
        if "úspešne" in result.lower():
            self.status_label.configure(text="✅ Gmail pripojený", text_color="#4CAF50")
            self.connect_button.configure(text="🔗 Pripojené", state="disabled")
            self.refresh_emails()
        else:
            self.status_label.configure(text=result, text_color="#ff6b6b")
    
    def refresh_emails(self):
        """Obnoví zoznam emailov"""
        if not hasattr(self.assistant, 'gmail_manager') or not self.assistant.gmail_manager.authenticated:
            return
        
        self.show_loading()
        
        def refresh_thread():
            try:
                emails_text = self.assistant.gmail_manager.get_recent_emails(15)
                self.parent.after(0, lambda: self.display_emails(emails_text))
            except Exception as e:
                self.parent.after(0, lambda: self.display_emails(f"❌ Chyba pri načítaní: {str(e)}"))
        
        threading.Thread(target=refresh_thread, daemon=True).start()
    
    def search_emails(self):
        """Vyhľadá emaily"""
        search_term = self.search_entry.get().strip()
        if not search_term:
            return
        
        if not hasattr(self.assistant, 'gmail_manager') or not self.assistant.gmail_manager.authenticated:
            return
        
        self.show_loading()
        
        def search_thread():
            try:
                search_command = f"nájdi email {search_term}"
                result = self.assistant.gmail_manager.search_emails(search_command)
                self.parent.after(0, lambda: self.display_emails(result))
            except Exception as e:
                self.parent.after(0, lambda: self.display_emails(f"❌ Chyba pri vyhľadávaní: {str(e)}"))
        
        threading.Thread(target=search_thread, daemon=True).start()
    
    def show_loading(self):
        """Zobrazí indikátor načítania"""
        for widget in self.emails_frame.winfo_children():
            widget.destroy()
        
        self.loading_indicator.pack(fill="x", pady=10)
    
    def display_emails(self, emails_text: str):
        """Zobrazí emaily v UI"""
        for widget in self.emails_frame.winfo_children():
            widget.destroy()
        
        if not emails_text:
            emails_text = "📭 Žiadne emaily na zobrazenie"
        
        emails_label = ctk.CTkLabel(
            self.emails_frame,
            text=emails_text,
            justify="left",
            font=ctk.CTkFont(size=12),
            wraplength=600
        )
        emails_label.pack(anchor="w", padx=10, pady=5)
    
    def open_compose_window(self):
        """Otvorie okna pre vytvorenie nového emailu"""
        if not hasattr(self.assistant, 'gmail_manager') or not self.assistant.gmail_manager.authenticated:
            self.status_label.configure(text="❌ Najprv pripojte Gmail", text_color="#ff6b6b")
            return
        
        compose_window = ctk.CTkToplevel(self.main_frame)
        compose_window.title("📝 Nový Email")
        compose_window.geometry("600x500")
        compose_window.transient(self.parent)
        compose_window.grab_set()
        
        # Hlavný rám
        main_frame = ctk.CTkFrame(compose_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Polia formulára
        ctk.CTkLabel(main_frame, text="Pre:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(0, 5))
        to_entry = ctk.CTkEntry(main_frame, width=400, height=35)
        to_entry.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(main_frame, text="Predmet:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(0, 5))
        subject_entry = ctk.CTkEntry(main_frame, width=400, height=35)
        subject_entry.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(main_frame, text="Správa:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(0, 5))
        body_text = ctk.CTkTextbox(main_frame, width=400, height=200)
        body_text.pack(fill="both", expand=True, pady=(0, 20))
        
        # Tlačidlá
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x")
        
        def send_email():
            recipient = to_entry.get().strip()
            subject = subject_entry.get().strip()
            body = body_text.get("1.0", "end-1c").strip()
            
            if not recipient:
                self.show_message(compose_window, "❌ Zadajte príjemcu")
                return
            
            if not subject:
                subject = "Bez predmetu"
            
            if not body:
                body = " "
            
            # Odoslanie emailu
            def send_thread():
                try:
                    result = asyncio.run(
                        self.assistant.gmail_manager.send_email(recipient, subject, body)
                    )
                    compose_window.after(0, lambda: self.on_send_result(compose_window, result))
                except Exception as e:
                    compose_window.after(0, lambda: self.on_send_result(compose_window, f"❌ Chyba: {str(e)}"))
            
            threading.Thread(target=send_thread, daemon=True).start()
            self.show_message(compose_window, "⏳ Odosielam email...")
        
        send_button = ctk.CTkButton(
            button_frame,
            text="📤 Odoslať",
            command=send_email,
            width=100,
            height=35,
            fg_color="#2b7c5b",
            hover_color="#1e5941"
        )
        send_button.pack(side="right", padx=(10, 0))
        
        cancel_button = ctk.CTkButton(
            button_frame,
            text="❌ Zrušiť",
            command=compose_window.destroy,
            width=100,
            height=35,
            fg_color="#7c2b2b",
            hover_color="#591e1e"
        )
        cancel_button.pack(side="right")
    
    def on_send_result(self, window, result: str):
        """Spracuje výsledok odoslania emailu"""
        window.destroy()
        if "úspešne" in result.lower():
            self.status_label.configure(text="✅ Email odoslaný", text_color="#4CAF50")
        else:
            self.status_label.configure(text=result, text_color="#ff6b6b")
        
        # Obnovíme emaily
        self.refresh_emails()
    
    def show_message(self, window, message: str):
        """Zobrazí správu v okne"""
        for widget in window.winfo_children():
            if isinstance(widget, ctk.CTkLabel) and "message" in widget.cget("text").lower():
                widget.destroy()
        
        message_label = ctk.CTkLabel(
            window,
            text=message,
            text_color="#FFA500"
        )
        message_label.pack(pady=10)
    
    def pack(self, **kwargs):
        """Zabali hlavný rám pre zobrazenie"""
        self.main_frame.pack(**kwargs)
    
    def pack_forget(self):
        """Skryje hlavný rám"""
        self.main_frame.pack_forget()