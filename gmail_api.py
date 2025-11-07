import os
import json
import threading
from flask import Flask, request, jsonify, session, redirect
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
from dotenv import load_dotenv
import logging

# 🔒 OPRAVA PRE OAUTH NA LOCALHOST - povoliť HTTP
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Načítaj environment premenné
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'fallback-secret-key-for-dev')

# Konfigurácia Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
GMAIL_CREDENTIALS_PATH = os.getenv('GMAIL_CREDENTIALS_PATH', './credentials/gmail-credentials.json')
GMAIL_TOKEN_PATH = './credentials/gmail-token.json'

# Nastavenie loggera
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Globálna premenná pre Gmail service
gmail_service = None
service_lock = threading.Lock()

def init_gmail_service():
    """Inicializuje Gmail API službu"""
    global gmail_service
    
    with service_lock:
        if gmail_service is not None:
            return gmail_service
            
        try:
            # Skús načítať uložený token (ak už prebehla autorizácia)
            if os.path.exists(GMAIL_TOKEN_PATH):
                with open(GMAIL_TOKEN_PATH, 'r') as token_file:
                    creds_data = json.load(token_file)
                
                creds = Credentials(
                    token=creds_data.get('token'),
                    refresh_token=creds_data.get('refresh_token'),
                    token_uri=creds_data.get('token_uri', 'https://oauth2.googleapis.com/token'),
                    client_id=creds_data.get('client_id'),
                    client_secret=creds_data.get('client_secret'),
                    scopes=creds_data.get('scopes', SCOPES)
                )
                
                # Obnov token ak je expirovaný
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                    # Ulož obnovený token
                    with open(GMAIL_TOKEN_PATH, 'w') as token_file:
                        json.dump({
                            'token': creds.token,
                            'refresh_token': creds.refresh_token,
                            'token_uri': creds.token_uri,
                            'client_id': creds.client_id,
                            'client_secret': creds.client_secret,
                            'scopes': creds.scopes
                        }, token_file)
            else:
                # Ak nie je token, vráť None - používateľ musí prejsť autorizáciou
                logger.warning("No Gmail token found. User needs to authorize.")
                return None
            
            gmail_service = build('gmail', 'v1', credentials=creds)
            logger.info("✅ Gmail API initialized successfully")
            return gmail_service
            
        except Exception as e:
            logger.error(f"❌ Error initializing Gmail API: {e}")
            return None

def get_gmail_labels(service):
    """Získa zoznam labelov z Gmailu"""
    try:
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        return labels
    except Exception as e:
        logger.error(f"Error getting labels: {e}")
        return []

def get_recent_emails(service, max_results=10):
    """Získa posledné emaily"""
    try:
        results = service.users().messages().list(
            userId='me', 
            maxResults=max_results,
            labelIds=['INBOX']
        ).execute()
        
        messages = []
        messages_list = results.get('messages', [])
        
        for msg in messages_list:
            try:
                message = service.users().messages().get(
                    userId='me', 
                    id=msg['id'],
                    format='metadata',
                    metadataHeaders=['Subject', 'From']
                ).execute()
                
                headers = message.get('payload', {}).get('headers', [])
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
                
                messages.append({
                    'id': msg['id'],
                    'subject': subject,
                    'from': sender,
                    'snippet': message.get('snippet', ''),
                    'internalDate': message.get('internalDate', '')
                })
            except Exception as e:
                logger.error(f"Error processing message {msg['id']}: {e}")
                continue
        
        return messages
    except Exception as e:
        logger.error(f"Error getting emails: {e}")
        return []

@app.before_request
def initialize_gmail_before_request():
    """Inicializuje Gmail službu pred prvou požiadavkou"""
    if not hasattr(app, 'gmail_initialized'):
        logger.info("Checking Gmail service...")
        init_gmail_service()
        app.gmail_initialized = True

@app.route('/')
def index():
    """Hlavná stránka"""
    return '''
    <h1>Aura Test - Gmail API</h1>
    <p>Backend služba pre Gmail integráciu</p>
    <ul>
        <li><a href="/gmail-setup">Nastavenie Gmail</a></li>
        <li><a href="/gmail-status">Stav služby</a></li>
        <li><a href="/gmail-test">Test Gmail API</a></li>
    </ul>
    '''

@app.route('/authorize')
def authorize():
    """Začína OAuth flow"""
    try:
        flow = Flow.from_client_secrets_file(
            GMAIL_CREDENTIALS_PATH,
            scopes=SCOPES,
            redirect_uri='http://localhost:5001/oauth2callback'
        )
        
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='select_account'
        )
        
        session['oauth_state'] = state
        return redirect(authorization_url)
        
    except Exception as e:
        return jsonify({'error': f'Authorization failed: {str(e)}'}), 500

@app.route('/oauth2callback')
def oauth2callback():
    """Spracuje OAuth callback"""
    try:
        if 'oauth_state' not in session:
            return jsonify({'error': 'No OAuth state found in session. Start authorization from /authorize'}), 400
            
        flow = Flow.from_client_secrets_file(
            GMAIL_CREDENTIALS_PATH,
            scopes=SCOPES,
            state=session['oauth_state'],
            redirect_uri='http://localhost:5001/oauth2callback'
        )
        
        flow.fetch_token(authorization_response=request.url)
        
        credentials = flow.credentials
        creds_data = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
        
        os.makedirs(os.path.dirname(GMAIL_TOKEN_PATH), exist_ok=True)
        
        with open(GMAIL_TOKEN_PATH, 'w') as token_file:
            json.dump(creds_data, token_file)
        
        session.pop('oauth_state', None)
        
        global gmail_service
        gmail_service = None
        
        return '''
        <h1>Autorizácia úspešná! 🎉</h1>
        <p>Gmail API je teraz pripojené k vášmu účtu.</p>
        <p><a href="/gmail-test">Otestovať Gmail API</a></p>
        <p><a href="/">Späť na hlavnú stránku</a></p>
        '''
        
    except Exception as e:
        return jsonify({'error': f'OAuth callback failed: {str(e)}'}), 500

@app.route('/gmail-setup')
def gmail_setup():
    """Stránka pre nastavenie Gmailu"""
    return '''
    <h1>Nastavenie Gmail API</h1>
    <p>Pre pripojenie k Gmailu je potrebná autorizácia.</p>
    <p><a href="/authorize">Autorizovať Gmail</a></p>
    <p><a href="/gmail-status">Skontrolovať stav</a></p>
    '''

@app.route('/gmail-test')
def gmail_test():
    """Testovacia route pre Gmail API"""
    service = init_gmail_service()
    
    if not service:
        return jsonify({
            'status': 'error',
            'message': 'Gmail service not available. Please authorize first at /authorize'
        }), 500
    
    try:
        labels = get_gmail_labels(service)
        recent_emails = get_recent_emails(service, 5)
        
        return jsonify({
            'status': 'success',
            'message': 'Gmail API is working!',
            'labels_count': len(labels),
            'recent_emails_count': len(recent_emails),
            'labels': [label['name'] for label in labels[:10]],
            'recent_emails': recent_emails
        })
        
    except Exception as e:
        logger.error(f"Gmail test error: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Gmail API error: {str(e)}'
        }), 500

@app.route('/gmail-status')
def gmail_status():
    """Stav Gmail služby"""
    service = init_gmail_service()
    
    if service:
        try:
            profile = service.users().getProfile(userId='me').execute()
            return jsonify({
                'status': 'connected',
                'message': 'Gmail API is connected and working',
                'email_address': profile.get('emailAddress', 'Unknown')
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'Gmail connection error: {str(e)}'
            }), 500
    else:
        return jsonify({
            'status': 'disconnected',
            'message': 'Gmail service not initialized. Please authorize at /authorize'
        }), 500

@app.route('/gmail-emails')
def gmail_emails():
    """Získa posledné emaily"""
    service = init_gmail_service()
    
    if not service:
        return jsonify({'error': 'Gmail service not available'}), 500
    
    try:
        max_results = request.args.get('max', 20, type=int)
        emails = get_recent_emails(service, max_results)
        return jsonify({'emails': emails})
    except Exception as e:
        logger.error(f"Error in gmail-emails endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/gmail-search')
def gmail_search():
    """Vyhľadáva emaily"""
    service = init_gmail_service()
    
    if not service:
        return jsonify({'error': 'Gmail service not available'}), 500
    
    try:
        query = request.args.get('q', '')
        max_results = request.args.get('max', 20, type=int)
        
        if not query:
            return jsonify({'error': 'Query parameter "q" is required'}), 400
        
        results = service.users().messages().list(
            userId='me', 
            q=query,
            maxResults=max_results
        ).execute()
        
        messages = []
        messages_list = results.get('messages', [])
        
        for msg in messages_list:
            try:
                message = service.users().messages().get(
                    userId='me', 
                    id=msg['id'],
                    format='metadata',
                    metadataHeaders=['Subject', 'From']
                ).execute()
                
                headers = message.get('payload', {}).get('headers', [])
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
                
                messages.append({
                    'id': msg['id'],
                    'subject': subject,
                    'from': sender,
                    'snippet': message.get('snippet', '')
                })
            except Exception as e:
                logger.error(f"Error processing search result {msg['id']}: {e}")
                continue
        
        return jsonify({'emails': messages, 'query': query})
        
    except Exception as e:
        logger.error(f"Error in gmail-search: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    if not os.path.exists(GMAIL_CREDENTIALS_PATH):
        logger.warning(f"Gmail credentials not found at {GMAIL_CREDENTIALS_PATH}")
    
    os.makedirs(os.path.dirname(GMAIL_TOKEN_PATH), exist_ok=True)
    
    print("🚀 Starting Aura Test Gmail API server on port 5001...")
    app.run(debug=True, host='0.0.0.0', port=5001)