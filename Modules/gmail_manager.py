import os
import base64
import re
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from email.mime.base import MimeBase
from email import encoders
import mimetypes
from typing import List, Dict, Any, Optional
import json
from datetime import datetime
import threading

class GmailManager:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
                      'https://www.googleapis.com/auth/gmail.send',
                      'https://www.googleapis.com/auth/gmail.modify',
                      'https://www.googleapis.com/auth/gmail.labels']
        self.service = None
        self.authenticated = False
        self.email_categories = {
            'dôležité': ['urgent', 'important', 'dôležité', 'priority'],
            'pracovné': ['work', 'job', 'career', 'praca', 'práca'],
            'osobné': ['personal', 'family', 'friends', 'osobné'],
            'notifikácie': ['notification', 'alert', 'update', 'notifikácia'],
            'nakupovanie': ['purchase', 'order', 'nakup', 'nákup'],
            'socialne': ['social', 'facebook', 'twitter', 'instagram']
        }
        
        self.supported_commands = [
            "skontroluj emaily", "prečítaj emaily", "check emails", 
            "pošli email", "send email", "odosli email", "napíš email",
            "nájdi email", "find email", "vyhľadaj email",
            "označ email", "mark email", "označ ako prečítané",
            "vymaž email", "delete email", "zmaž email",
            "zoznam emailov", "list emails", "zobraz emaily",
            "kategórie emailov", "email categories", "triediť emaily",
            "automatické triedenie", "auto sort", "nastav triedenie",
            "pripoj gmail", "connect gmail", "gmail prihlásenie"
        ]
        
        self.load_config()
        print("✅ GmailManager inicializovaný")
    
    def load_config(self):
        """Načíta konfiguráciu Gmail"""
        self.config_file = "gmail_config.json"
        self.config = {
            'auto_sort': True,
            'categories': self.email_categories,
            'signature': "\n\nOdoslané pomocou Aura Assistant",
            'default_priority': 'normal'
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    self.config.update(saved_config)
            except:
                pass
    
    def save_config(self):
        """Uloží konfiguráciu Gmail"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except:
            pass
    
    def can_handle(self, command: str) -> bool:
        return any(cmd in command.lower() for cmd in self.supported_commands)
    
    async def handle(self, command: str) -> str:
        command_lower = command.lower()
        
        try:
            if not self.authenticated:
                if "pripoj gmail" in command_lower or "connect gmail" in command_lower:
                    return self.authenticate()
                else:
                    return "🔐 Gmail nie je pripojený. Povedz 'pripoj gmail' pre autentifikáciu."
            
            if "skontroluj emaily" in command_lower or "prečítaj emaily" in command_lower:
                return self.get_recent_emails(10)
            elif "pošli email" in command_lower or "odosli email" in command_lower:
                return await self.send_email_from_command(command)
            elif "nájdi email" in command_lower or "find email" in command_lower:
                return self.search_emails(command)
            elif "zoznam emailov" in command_lower or "list emails" in command_lower:
                return self.list_emails_by_category(command)
            elif "kategórie emailov" in command_lower or "email categories" in command_lower:
                return self.get_email_categories()
            elif "automatické triedenie" in command_lower or "auto sort" in command_lower:
                return self.toggle_auto_sort(command)
            elif "označ email" in command_lower or "mark email" in command_lower:
                return self.mark_email(command)
            elif "vymaž email" in command_lower or "delete email" in command_lower:
                return self.delete_email(command)
            else:
                return f"ℹ️  Príkaz '{command}' nie je plne implementovaný v GmailManager"
                
        except Exception as e:
            return f"❌ Chyba pri práci s Gmail: {str(e)}"
    
    def authenticate(self) -> str:
        """Autentifikácia s Gmail API"""
        try:
            creds = None
            # token.json ukladá refresh token
            if os.path.exists('gmail_token.json'):
                creds = Credentials.from_authorized_user_file('gmail_token.json', self.SCOPES)
            
            # Ak neexistujú platné credencialy, spýtaj sa používateľa na povolenie
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secret_file(
                        'gmail_credentials.json', self.SCOPES)
                    creds = flow.run_local_server(port=0)
                
                # Ulož credencialy pre budúce použitie
                with open('gmail_token.json', 'w') as token:
                    token.write(creds.to_json())
            
            self.service = build('gmail', 'v1', credentials=creds)
            self.authenticated = True
            return "✅ Gmail úspešne pripojený! Môžete používať email funkcie."
            
        except Exception as e:
            return f"❌ Chyba pri pripájaní Gmail: {str(e)}\nUistite sa, že máte súbor gmail_credentials.json"
    
    def get_recent_emails(self, max_results: int = 10) -> str:
        """Získa najnovšie emaily"""
        try:
            results = self.service.users().messages().list(
                userId='me', 
                maxResults=max_results,
                labelIds=['INBOX']
            ).execute()
            
            messages = results.get('messages', [])
            if not messages:
                return "📭 Žiadne nové emaily."
            
            emails_info = []
            for message in messages:
                msg = self.service.users().messages().get(
                    userId='me', 
                    id=message['id'],
                    format='metadata'
                ).execute()
                
                headers = msg['payload'].get('headers', [])
                subject = self._get_header(headers, 'Subject')
                sender = self._get_header(headers, 'From')
                date = self._get_header(headers, 'Date')
                
                # Kategorizácia
                category = self._categorize_email(subject + " " + sender)
                
                emails_info.append(f"📨 **{subject}**\n"
                                 f"   👤 Od: {sender}\n"
                                 f"   📅 {date}\n"
                                 f"   🏷️  Kategória: {category}\n")
            
            return "📧 **Najnovšie emaily:**\n" + "\n".join(emails_info)
            
        except HttpError as error:
            return f"❌ Chyba API: {error}"
    
    def _categorize_email(self, text: str) -> str:
        """Automaticky kategorizuje email"""
        text_lower = text.lower()
        for category, keywords in self.config['categories'].items():
            if any(keyword in text_lower for keyword in keywords):
                return category
        return "ostatné"
    
    async def send_email_from_command(self, command: str) -> str:
        """Pošle email na základe príkazu"""
        # Parsovanie príkazu
        parts = command.split()
        recipient = None
        subject = ""
        body = ""
        
        # Jednoduché parsovanie - môžeme vylepšiť
        for i, part in enumerate(parts):
            if part in ["pre", "to"] and i + 1 < len(parts):
                recipient = parts[i + 1]
            elif part in ["predmet", "subject"] and i + 1 < len(parts):
                subject = parts[i + 1]
            elif part in ["obsah", "body", "správa"]:
                body = " ".join(parts[i + 1:])
                break
        
        if not recipient:
            return "❌ Zadajte príjemcu: 'pošli email pre email@example.com predmet 'Ahoj' obsah 'Správa''"
        
        # Ak chýba obsah, spýtajme sa
        if not body:
            body = "Správa odoslaná pomocou Aura Assistant"
        
        try:
            return await self.send_email(recipient, subject, body)
        except Exception as e:
            return f"❌ Chyba pri odosielaní: {str(e)}"
    
    async def send_email(self, to: str, subject: str, body: str) -> str:
        """Pošle email"""
        try:
            message = MimeMultipart()
            message['to'] = to
            message['subject'] = subject
            
            # Pridaj podpis
            full_body = body + self.config['signature']
            message.attach(MimeText(full_body, 'plain'))
            
            # Encode message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            message_body = {'raw': raw_message}
            
            # Send message
            message = self.service.users().messages().send(
                userId='me', 
                body=message_body
            ).execute()
            
            return f"✅ Email úspešne odoslaný!\n📨 Pre: {to}\n📝 Predmet: {subject}"
            
        except HttpError as error:
            return f"❌ Chyba pri odosielaní: {error}"
    
    def search_emails(self, command: str) -> str:
        """Vyhľadá emaily"""
        search_term = command.lower().replace("nájdi email", "").replace("find email", "").strip()
        
        if not search_term:
            return "❌ Zadajte hľadaný výraz: 'nájdi email dôležitý'"
        
        try:
            results = self.service.users().messages().list(
                userId='me',
                q=search_term,
                maxResults=10
            ).execute()
            
            messages = results.get('messages', [])
            if not messages:
                return f"🔍 Nenašli sa žiadne emaily pre '{search_term}'"
            
            emails_info = [f"🔍 **Výsledky pre '{search_term}':**"]
            
            for message in messages:
                msg = self.service.users().messages().get(
                    userId='me', 
                    id=message['id'],
                    format='metadata'
                ).execute()
                
                headers = msg['payload'].get('headers', [])
                subject = self._get_header(headers, 'Subject')
                sender = self._get_header(headers, 'From')
                
                emails_info.append(f"📨 {subject}\n   👤 Od: {sender}")
            
            return "\n".join(emails_info)
            
        except HttpError as error:
            return f"❌ Chyba pri vyhľadávaní: {error}"
    
    def get_email_categories(self) -> str:
        """Zobrazí kategórie emailov"""
        categories_info = ["🏷️ **Kategórie emailov:**"]
        for category, keywords in self.config['categories'].items():
            categories_info.append(f"   **{category}**: {', '.join(keywords)}")
        
        categories_info.append(f"\n🔧 **Automatické triedenie:** {'ZAPNUTÉ' if self.config['auto_sort'] else 'VYPNUTÉ'}")
        return "\n".join(categories_info)
    
    def toggle_auto_sort(self, command: str) -> str:
        """Prepína automatické triedenie"""
        if "zapni" in command.lower() or "on" in command.lower():
            self.config['auto_sort'] = True
            self.save_config()
            return "✅ Automatické triedenie ZAPNUTÉ"
        else:
            self.config['auto_sort'] = False
            self.save_config()
            return "✅ Automatické triedenie VYPNUTÉ"
    
    def _get_header(self, headers: List[Dict], name: str) -> str:
        """Získa hodnotu hlavičky"""
        for header in headers:
            if header['name'] == name:
                return header['value']
        return "Neznáme"
    
    def mark_email(self, command: str) -> str:
        """Označí email ako prečítaný"""
        return "ℹ️  Funkcia označovania emailov bude čoskoro dostupná"
    
    def delete_email(self, command: str) -> str:
        """Vymaže email"""
        return "ℹ️  Funkcia mazania emailov bude čoskoro dostupná"
    
    def list_emails_by_category(self, command: str) -> str:
        """Zobrazí emaily podľa kategórie"""
        category = command.lower().replace("zoznam emailov", "").replace("list emails", "").strip()
        
        if not category:
            return self.get_recent_emails(10)
        
        # Hľadaj emaily v danej kategórii
        return f"ℹ️  Zobrazenie emailov pre kategóriu '{category}' bude čoskoro dostupné"