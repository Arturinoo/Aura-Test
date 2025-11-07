# gmail_setup.py - pomocný skript pre nastavenie
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.send',
          'https://www.googleapis.com/auth/gmail.modify']

def setup_gmail():
    creds = None
    if os.path.exists('gmail_token.json'):
        creds = Credentials.from_authorized_user_file('gmail_token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('gmail_credentials.json'):
                print("❌ Súbor gmail_credentials.json neexistuje!")
                print("📝 Postup:")
                print("1. Choď na https://console.cloud.google.com/")
                print("2. Vytvor nový projekt alebo vyber existujúci")
                print("3. Povoľ Gmail API")
                print("4. Vytvor OAuth 2.0 credentials (Desktop application)")
                print("5. Stiahni credentials.json a premenuj na gmail_credentials.json")
                return
            
            flow = InstalledAppFlow.from_client_secrets_file('gmail_credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('gmail_token.json', 'w') as token:
            token.write(creds.to_json())
    
    print("✅ Gmail úspešne nastavený!")

if __name__ == '__main__':
    setup_gmail()