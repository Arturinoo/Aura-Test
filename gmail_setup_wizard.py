# gmail_setup_wizard.py
import os
import json
import webbrowser
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import customtkinter as ctk
from tkinter import messagebox

class GmailSetupWizard:
    def __init__(self, parent):
        self.parent = parent
        self.SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
                      'https://www.googleapis.com/auth/gmail.send',
                      'https://www.googleapis.com/auth/gmail.modify']
        
        self.setup_ui()
    
    def setup_ui(self):
        """Vytvorí GUI pre Gmail setup"""
        self.window = ctk.CTkToplevel(self.parent)
        self.window.title("Gmail Setup Wizard")
        self.window.geometry("500x400")
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Centrovanie
        self.window.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - 250
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - 200
        self.window.geometry(f"+{x}+{y}")
        
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            main_frame,
            text="🔧 Gmail Setup Wizard",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=20)
        
        # Krok 1: Kontrola credentials
        self.step1_frame = ctk.CTkFrame(main_frame)
        self.step1_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            self.step1_frame,
            text="1. Kontrola Gmail Credentials",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", pady=5)
        
        self.credentials_status = ctk.CTkLabel(
            self.step1_frame,
            text="🔍 Kontrolujem credentials...",
            font=("Segoe UI", 12)
        )
        self.credentials_status.pack(anchor="w", pady=5)
        
        # Krok 2: Autorizácia
        self.step2_frame = ctk.CTkFrame(main_frame)
        self.step2_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            self.step2_frame,
            text="2. Autorizácia Gmail API",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", pady=5)
        
        self.auth_status = ctk.CTkLabel(
            self.step2_frame,
            text="Čaká na autorizáciu...",
            font=("Segoe UI", 12)
        )
        self.auth_status.pack(anchor="w", pady=5)
        
        auth_btn = ctk.CTkButton(
            self.step2_frame,
            text="🌐 Autorizovať Gmail",
            command=self.authorize_gmail,
            state="disabled"
        )
        auth_btn.pack(pady=5)
        self.auth_btn = auth_btn
        
        # Krok 3: Test spojenia
        self.step3_frame = ctk.CTkFrame(main_frame)
        self.step3_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            self.step3_frame,
            text="3. Test spojenia",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", pady=5)
        
        self.test_status = ctk.CTkLabel(
            self.step3_frame,
            text="Čaká na test...",
            font=("Segoe UI", 12)
        )
        self.test_status.pack(anchor="w", pady=5)
        
        test_btn = ctk.CTkButton(
            self.step3_frame,
            text="🔗 Testovať spojenie",
            command=self.test_connection,
            state="disabled"
        )
        test_btn.pack(pady=5)
        self.test_btn = test_btn
        
        # Spusti kontrolu credentials
        self.window.after(100, self.check_credentials)
    
    def check_credentials(self):
        """Skontroluje existenciu credentials súborov"""
        credentials_file = 'gmail_credentials.json'
        token_file = 'gmail_token.json'
        
        if os.path.exists(credentials_file):
            self.credentials_status.configure(
                text="✅ Gmail credentials nájdené",
                text_color="green"
            )
            self.auth_btn.configure(state="normal")
        else:
            self.credentials_status.configure(
                text="❌ Chýbajú credentials (gmail_credentials.json)",
                text_color="red"
            )
            self.create_credentials_help()
    
    def create_credentials_help(self):
        """Vytvorí pomoc pre získanie credentials"""
        help_text = """
📋 Ako získať Gmail credentials:

1. Choď na https://console.cloud.google.com/
2. Vytvor nový projekt alebo vyber existujúci
3. Povoľ Gmail API
4. Vytvor OAuth 2.0 credentials (Desktop application)
5. Stiahni credentials.json a premenuj na gmail_credentials.json
6. Ulož súbor do priečinka s aplikáciou
"""
        
        help_label = ctk.CTkLabel(
            self.step1_frame,
            text=help_text,
            font=("Segoe UI", 10),
            justify="left"
        )
        help_label.pack(anchor="w", pady=10)
    
    def authorize_gmail(self):
        """Spustí OAuth autorizáciu"""
        try:
            self.auth_status.configure(text="🔄 Spúšťam autorizáciu...")
            
            # Spusti autorizáciu v samostatnom vlákne
            import threading
            thread = threading.Thread(target=self._authorize_thread)
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            self.auth_status.configure(
                text=f"❌ Chyba pri autorizácii: {str(e)}",
                text_color="red"
            )
    
    def _authorize_thread(self):
        """Autorizácia v samostatnom vlákne"""
        try:
            creds = None
            if os.path.exists('gmail_token.json'):
                creds = Credentials.from_authorized_user_file('gmail_token.json', self.SCOPES)
            
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'gmail_credentials.json', self.SCOPES)
                    creds = flow.run_local_server(port=0)
                
                with open('gmail_token.json', 'w') as token:
                    token.write(creds.to_json())
            
            self.window.after(0, lambda: self.on_auth_success())
            
        except Exception as e:
            self.window.after(0, lambda: self.on_auth_error(str(e)))
    
    def on_auth_success(self):
        """Callback pre úspešnú autorizáciu"""
        self.auth_status.configure(
            text="✅ Autorizácia úspešná!",
            text_color="green"
        )
        self.test_btn.configure(state="normal")
    
    def on_auth_error(self, error_msg):
        """Callback pre chybu autorizácie"""
        self.auth_status.configure(
            text=f"❌ Chyba autorizácie: {error_msg}",
            text_color="red"
        )
    
    def test_connection(self):
        """Otestuje spojenie s Gmail API"""
        try:
            self.test_status.configure(text="🔄 Testujem spojenie...")
            
            import threading
            thread = threading.Thread(target=self._test_connection_thread)
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            self.test_status.configure(
                text=f"❌ Chyba testu: {str(e)}",
                text_color="red"
            )
    
    def _test_connection_thread(self):
        """Test spojenia v samostatnom vlákne"""
        try:
            from googleapiclient.discovery import build
            from google.auth.transport.requests import Request
            from google.oauth2.credentials import Credentials
            
            creds = Credentials.from_authorized_user_file('gmail_token.json', self.SCOPES)
            service = build('gmail', 'v1', credentials=creds)
            
            # Testovacie volanie
            profile = service.users().getProfile(userId='me').execute()
            email = profile.get('emailAddress', 'Unknown')
            
            self.window.after(0, lambda: self.on_test_success(email))
            
        except Exception as e:
            self.window.after(0, lambda: self.on_test_error(str(e)))
    
    def on_test_success(self, email):
        """Callback pre úspešný test"""
        self.test_status.configure(
            text=f"✅ Spojenie úspešné! Pripojené ako: {email}",
            text_color="green"
        )
        
        # Ulož nastavenia
        self.save_gmail_config()
        
        # Zatvor wizard po 2 sekundách
        self.window.after(2000, self.window.destroy)
        
        messagebox.showinfo("Gmail Setup", "Gmail bol úspešne nastavený! 🎉")
    
    def on_test_error(self, error_msg):
        """Callback pre chybu testu"""
        self.test_status.configure(
            text=f"❌ Chyba spojenia: {error_msg}",
            text_color="red"
        )
    
    def save_gmail_config(self):
        """Uloží Gmail konfiguráciu"""
        config = {
            'gmail_configured': True,
            'gmail_enabled': True
        }
        
        try:
            with open('gmail_config.json', 'w') as f:
                json.dump(config, f, indent=2)
        except:
            pass