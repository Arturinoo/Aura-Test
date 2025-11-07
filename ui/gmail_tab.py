import requests
import json
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTextEdit, QListWidget, QLabel, QLineEdit, QListWidgetItem,
                             QMessageBox, QProgressBar, QSplitter)
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, Qt
from PyQt5.QtGui import QFont, QColor

class EmailWorker(QThread):
    """Worker thread pre načítavanie emailov"""
    finished = pyqtSignal(object)
    error = pyqtSignal(str)
    
    def __init__(self, endpoint, params=None):
        super().__init__()
        self.endpoint = endpoint
        self.params = params or {}
        
    def run(self):
        try:
            response = requests.get(f'http://localhost:5001/{self.endpoint}', 
                                  params=self.params, timeout=10)
            if response.status_code == 200:
                self.finished.emit(response.json())
            else:
                self.error.emit(f"Server error: {response.status_code}")
        except Exception as e:
            self.error.emit(f"Connection error: {str(e)}")

class GmailTab(QWidget):
    def __init__(self):
        super().__init__()
        self.current_emails = []
        self.init_ui()
        # Timer pre automatické obnovovanie stavu
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.check_status)
        self.status_timer.start(1)  # Kontrola každých 5 sekúnd
        
    def init_ui(self):
        main_layout = QVBoxLayout()
        
        # Status panel
        status_layout = QHBoxLayout()
        
        self.status_label = QLabel("Stav: Kontrolujem pripojenie...")
        status_font = QFont()
        status_font.setBold(True)
        self.status_label.setFont(status_font)
        status_layout.addWidget(self.status_label)
        
        self.email_label = QLabel("Email: Neznámy")
        status_layout.addWidget(self.email_label)
        
        status_layout.addStretch()
        
        main_layout.addLayout(status_layout)
        
        # Progress bar pre načítavanie
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # Tlačidlá
        btn_layout = QHBoxLayout()
        
        self.connect_btn = QPushButton("🔗 Pripojiť Gmail")
        self.connect_btn.clicked.connect(self.connect_gmail)
        self.connect_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; }")
        
        self.refresh_btn = QPushButton("🔄 Obnoviť emaily")
        self.refresh_btn.clicked.connect(self.refresh_emails)
        self.refresh_btn.setEnabled(False)
        self.refresh_btn.setStyleSheet("QPushButton { background-color: #2196F3; color: white; }")
        
        self.test_btn = QPushButton("🧪 Test pripojenia")
        self.test_btn.clicked.connect(self.test_connection)
        self.test_btn.setStyleSheet("QPushButton { background-color: #FF9800; color: white; }")
        
        btn_layout.addWidget(self.connect_btn)
        btn_layout.addWidget(self.refresh_btn)
        btn_layout.addWidget(self.test_btn)
        btn_layout.addStretch()
        
        main_layout.addLayout(btn_layout)
        
        # Vyhľadávanie
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("🔍 Vyhľadávanie:"))
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Zadajte hľadaný výraz...")
        self.search_input.returnPressed.connect(self.search_emails)
        search_layout.addWidget(self.search_input)
        
        self.search_btn = QPushButton("Hľadať")
        self.search_btn.clicked.connect(self.search_emails)
        search_layout.addWidget(self.search_btn)
        
        self.clear_search_btn = QPushButton("Zrušiť")
        self.clear_search_btn.clicked.connect(self.clear_search)
        self.clear_search_btn.setEnabled(False)
        search_layout.addWidget(self.clear_search_btn)
        
        main_layout.addLayout(search_layout)
        
        # Splitter pre emaily a detail
        splitter = QSplitter(Qt.Horizontal)
        
        # Ľavý panel - zoznam emailov
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        left_layout.addWidget(QLabel("📧 Posledné emaily:"))
        self.emails_list = QListWidget()
        self.emails_list.itemClicked.connect(self.show_email_detail)
        left_layout.addWidget(self.emails_list)
        
        # Pravý panel - detail emailu
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        right_layout.addWidget(QLabel("📄 Detail emailu:"))
        self.email_detail = QTextEdit()
        self.email_detail.setReadOnly(True)
        self.email_detail.setStyleSheet("QTextEdit { background-color: #f5f5f5; }")
        right_layout.addWidget(self.email_detail)
        
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([400, 600])
        
        main_layout.addWidget(splitter)
        
        # Štatistika
        stats_layout = QHBoxLayout()
        self.stats_label = QLabel("Načítavam štatistiky...")
        stats_layout.addWidget(self.stats_label)
        stats_layout.addStretch()
        
        self.last_update_label = QLabel("")
        stats_layout.addWidget(self.last_update_label)
        
        main_layout.addLayout(stats_layout)
        
        self.setLayout(main_layout)
        self.check_status()
        
    def check_status(self):
        """Skontroluje stav Gmail pripojenia"""
        try:
            response = requests.get('http://localhost:1/gmail-status', timeout=5)
            data = response.json()
            
            if data.get('status') == 'connected':
                self.status_label.setText("✅ Stav: Pripojené")
                self.status_label.setStyleSheet("color: green; font-weight: bold;")
                self.email_label.setText(f"📭 Email: {data.get('email_address', 'Neznámy')}")
                self.refresh_btn.setEnabled(True)
                self.connect_btn.setEnabled(False)
                # Automaticky načítaj emaily pri prvom pripojení
                if not self.current_emails:
                    self.refresh_emails()
            else:
                self.status_label.setText("❌ Stav: Nepripojené")
                self.status_label.setStyleSheet("color: red; font-weight: bold;")
                self.email_label.setText("📭 Email: Neznámy")
                self.refresh_btn.setEnabled(False)
                self.connect_btn.setEnabled(True)
                
        except Exception as e:
            self.status_label.setText("⚠️ Stav: Chyba pripojenia")
            self.status_label.setStyleSheet("color: orange; font-weight: bold;")
            self.email_label.setText("📭 Email: Nedostupný")
    
    def connect_gmail(self):
        """Spustí OAuth autorizáciu"""
        import webbrowser
        webbrowser.open('http://localhost:1/authorize')
        self.status_label.setText("🔄 Stav: Prebieha autorizácia... Otvor prehliadač.")
        self.status_label.setStyleSheet("color: blue; font-weight: bold;")
        
        # Spusti timer pre častejšiu kontrolu stavu počas autorizácie
        self.status_timer.start(2000)
        
    def refresh_emails(self):
        """Načítaje emaily z Gmail API"""
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        
        # Použi worker thread
        self.email_worker = EmailWorker('gmail-emails', {'max': 20})
        self.email_worker.finished.connect(self.on_emails_loaded)
        self.email_worker.error.connect(self.on_emails_error)
        self.email_worker.start()
    
    def on_emails_loaded(self, data):
        """Spracuje načítané emaily"""
        self.progress_bar.setVisible(False)
        self.emails_list.clear()
        self.current_emails = data.get('emails', [])
        
        for email in self.current_emails:
            # Skrátený odosielateľ a predmet
            sender = email['from'].split('<')[0].strip()[:30]
            subject = email['subject'][:50] + "..." if len(email['subject']) > 50 else email['subject']
            item_text = f"{sender}: {subject}"
            item = QListWidgetItem(item_text)
            
            # Ulož celý email ako data
            item.setData(Qt.UserRole, email)
            
            # Farba pre dôležité emaily
            if any(keyword in email['subject'].lower() for keyword in ['important', 'urgent', 'dôležité']):
                item.setBackground(QColor(255, 255, 200))  # Žltá pre dôležité
            
            self.emails_list.addItem(item)
        
        # Aktualizuj štatistiky
        self.update_stats()
        
        # Zobraz prvý email v detaile
        if self.current_emails:
            self.emails_list.setCurrentRow(0)
            self.show_email_detail(self.emails_list.item(0))
    
    def on_emails_error(self, error_msg):
        """Spracuje chybu pri načítavaní emailov"""
        self.progress_bar.setVisible(False)
        QMessageBox.warning(self, "Chyba", f"Chyba pri načítaní emailov: {error_msg}")
    
    def show_email_detail(self, item):
        """Zobrazí detail vybraného emailu"""
        if not item:
            return
            
        email_data = item.data(Qt.UserRole)
        if email_data:
            # Formátovanie dátumu
            from datetime import datetime
            try:
                timestamp = int(email_data.get('internalDate', '0')) / 1000
                date_str = datetime.fromtimestamp(timestamp).strftime('%d.%m.%Y %H:%M')
            except:
                date_str = "Neznámy dátum"
            
            detail_text = f"""
📧 OD: {email_data['from']}
📋 PREDMET: {email_data['subject']}
🕒 DÁTUM: {date_str}

📝 SNIPPET:
{email_data['snippet']}

🔗 ID: {email_data['id']}
            """
            self.email_detail.setText(detail_text.strip())
    
    def search_emails(self):
        """Vyhľadáva v emailoch"""
        search_term = self.search_input.text().strip()
        if not search_term:
            QMessageBox.information(self, "Vyhľadávanie", "Zadajte hľadaný výraz")
            return
        
        self.progress_bar.setVisible(True)
        
        # Použi worker thread pre vyhľadávanie
        self.search_worker = EmailWorker('gmail-search', {'q': search_term, 'max': 20})
        self.search_worker.finished.connect(self.on_search_loaded)
        self.search_worker.error.connect(self.on_search_error)
        self.search_worker.start()
        
        self.clear_search_btn.setEnabled(True)
    
    def on_search_loaded(self, data):
        """Spracuje výsledky vyhľadávania"""
        self.progress_bar.setVisible(False)
        self.emails_list.clear()
        self.current_emails = data.get('emails', [])
        
        query = data.get('query', '')
        
        for email in self.current_emails:
            sender = email['from'].split('<')[0].strip()[:30]
            subject = email['subject'][:50] + "..." if len(email['subject']) > 50 else email['subject']
            item_text = f"{sender}: {subject}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, email)
            item.setBackground(QColor(200, 255, 200))  # Zelená pre výsledky vyhľadávania
            self.emails_list.addItem(item)
        
        self.update_stats()
        self.stats_label.setText(f"📊 Nájdených emailov: {len(self.current_emails)} pre výraz: '{query}'")
        
        if self.current_emails:
            self.emails_list.setCurrentRow(0)
            self.show_email_detail(self.emails_list.item(0))
        else:
            self.email_detail.setText("Žiadne emaily nevyhovujú vyhľadávaniu.")
    
    def on_search_error(self, error_msg):
        """Spracuje chybu pri vyhľadávaní"""
        self.progress_bar.setVisible(False)
        QMessageBox.warning(self, "Chyba vyhľadávania", f"Chyba pri vyhľadávaní: {error_msg}")
    
    def clear_search(self):
        """Zruší vyhľadávanie a vráti pôvodné emaily"""
        self.search_input.clear()
        self.refresh_emails()
        self.clear_search_btn.setEnabled(False)
        self.stats_label.setText("Štatistiky")
    
    def test_connection(self):
        """Testuje Gmail API pripojenie"""
        self.progress_bar.setVisible(True)
        
        self.test_worker = EmailWorker('gmail-test')
        self.test_worker.finished.connect(self.on_test_loaded)
        self.test_worker.error.connect(self.on_test_error)
        self.test_worker.start()
    
    def on_test_loaded(self, data):
        """Spracuje výsledok testu"""
        self.progress_bar.setVisible(False)
        
        if data.get('status') == 'success':
            QMessageBox.information(self, "✅ Test pripojenia", 
                                  f"Gmail API funguje správne!\n\n"
                                  f"📂 Počet labelov: {data.get('labels_count', 0)}\n"
                                  f"📧 Počet emailov: {data.get('recent_emails_count', 0)}\n"
                                  f"💬 Správa: {data.get('message', 'OK')}")
        else:
            QMessageBox.warning(self, "❌ Test pripojenia", 
                              f"Chyba: {data.get('message', 'Neznáma chyba')}")
    
    def on_test_error(self, error_msg):
        """Spracuje chybu testu"""
        self.progress_bar.setVisible(False)
        QMessageBox.critical(self, "❌ Test pripojenia", f"Chyba: {error_msg}")
    
    def update_stats(self):
        """Aktualizuje štatistiky"""
        from datetime import datetime
        total_emails = len(self.current_emails)
        self.stats_label.setText(f"📊 Počet načítaných emailov: {total_emails}")
        self.last_update_label.setText(f"🕒 Posledná aktualizácia: {datetime.now().strftime('%H:%M:%S')}")

    def closeEvent(self, event):
        """Zastaví timer pri zatvorení"""
        self.status_timer.stop()
        super().closeEvent(event)

# Testovací kód
if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    window = GmailTab()
    window.setWindowTitle("Aura Test - Gmail Tab")
    window.resize(1000, 700)
    window.show()
    sys.exit(app.exec_())