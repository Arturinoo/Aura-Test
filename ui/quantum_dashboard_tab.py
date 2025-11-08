# ui/quantum_dashboard_tab.py
import customtkinter as ctk
from .themes import theme_manager
import psutil
import time
import threading
from datetime import datetime
import os

class QuantumDashboardTab(ctk.CTkFrame):
    def __init__(self, parent, assistant, config_manager):
        self.theme = theme_manager.get_theme("quantum_green")
        super().__init__(parent, fg_color=self.theme["bg"], corner_radius=0, border_width=0)
        
        self.assistant = assistant
        self.config_manager = config_manager
        self.running = True
        self.metrics_data = {
            'cpu': 0,
            'memory': 0,
            'disk': 0,
            'battery': 0,
            'temperature': 0
        }
        
        self.setup_dashboard_ui()
        self.start_dashboard_updates()
        print("✅ Quantum Dashboard inicializovaný")
    
    def setup_dashboard_ui(self):
        """Vytvorí dashboard UI"""
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
        self.setup_dashboard_header(main_container)
        
        # Obsah dashboardu
        self.setup_dashboard_content(main_container)
    
    def setup_dashboard_header(self, parent):
        """Vytvorí header dashboardu"""
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
            text="📊 QUANTUM DASHBOARD",
            font=("Segoe UI", 20, "bold"),
            text_color=self.theme["accent_glow"]
        ).pack(anchor="w")
        
        self.dashboard_status = ctk.CTkLabel(
            title_frame,
            text="Live systémové metriky",
            font=("Consolas", 10),
            text_color=self.theme["success"]
        )
        self.dashboard_status.pack(anchor="w")
        
        # Rýchle akcie
        action_frame = ctk.CTkFrame(header, fg_color="transparent", border_width=0)
        action_frame.pack(side="right", padx=30, pady=20)
        
        ctk.CTkButton(
            action_frame,
            text="🔄 Obnoviť",
            command=self.refresh_dashboard,
            width=100,
            height=35,
            fg_color=self.theme["accent_secondary"],
            hover_color=self.theme["accent_glow"],
            font=("Segoe UI", 11)
        ).pack(side="left", padx=5)
    
    def setup_dashboard_content(self, parent):
        """Vytvorí obsah dashboardu"""
        content_frame = ctk.CTkFrame(parent, fg_color="transparent", border_width=0)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Scrollovateľný obsah
        self.dashboard_scroll = ctk.CTkScrollableFrame(
            content_frame,
            fg_color=self.theme["bg_secondary"],
            scrollbar_button_color=self.theme["accent_secondary"],
            scrollbar_button_hover_color=self.theme["accent_glow"]
        )
        self.dashboard_scroll.grid(row=0, column=0, sticky="nsew")
        
        # Nastavenie mriežky pre widgety
        self.dashboard_scroll.grid_columnconfigure(0, weight=1)
        self.dashboard_scroll.grid_columnconfigure(1, weight=1)
        
        # Vytvorenie widgetov
        self.setup_system_widgets()
        self.setup_quick_commands()
        self.setup_modules_status()
        self.setup_recent_activity()
    
    def setup_system_widgets(self):
        """Vytvorí widgety systémových metrík"""
        # Rám pre systémové metriky
        system_frame = ctk.CTkFrame(
            self.dashboard_scroll,
            fg_color=self.theme["bg_tertiary"],
            corner_radius=15,
            border_width=2,
            border_color=self.theme["accent_secondary"]
        )
        system_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        
        ctk.CTkLabel(
            system_frame,
            text="🖥️ SYSTÉMOVÉ METRIKY",
            font=("Segoe UI", 16, "bold"),
            text_color=self.theme["accent_glow"]
        ).pack(anchor="w", padx=20, pady=15)
        
        # Metriky v mriežke
        metrics_grid = ctk.CTkFrame(system_frame, fg_color="transparent", border_width=0)
        metrics_grid.pack(fill="x", padx=20, pady=(0, 15))
        metrics_grid.grid_columnconfigure(0, weight=1)
        metrics_grid.grid_columnconfigure(1, weight=1)
        
        # CPU
        cpu_frame = ctk.CTkFrame(metrics_grid, fg_color=self.theme["bg_secondary"], corner_radius=10)
        cpu_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        cpu_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            cpu_frame,
            text="⚡ CPU:",
            font=("Segoe UI", 12, "bold"),
            text_color=self.theme["text_primary"]
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.cpu_label = ctk.CTkLabel(
            cpu_frame,
            text="0%",
            font=("Consolas", 12),
            text_color=self.theme["accent_glow"]
        )
        self.cpu_label.grid(row=0, column=1, padx=10, pady=10, sticky="e")
        
        # CPU Progress bar
        self.cpu_progress = ctk.CTkProgressBar(
            cpu_frame,
            height=8,
            fg_color=self.theme["bg_tertiary"],
            progress_color=self.theme["accent_glow"]
        )
        self.cpu_progress.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))
        self.cpu_progress.set(0)
        
        # RAM
        ram_frame = ctk.CTkFrame(metrics_grid, fg_color=self.theme["bg_secondary"], corner_radius=10)
        ram_frame.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        ram_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            ram_frame,
            text="🧠 RAM:",
            font=("Segoe UI", 12, "bold"),
            text_color=self.theme["text_primary"]
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.ram_label = ctk.CTkLabel(
            ram_frame,
            text="0%",
            font=("Consolas", 12),
            text_color=self.theme["accent_glow"]
        )
        self.ram_label.grid(row=0, column=1, padx=10, pady=10, sticky="e")
        
        # RAM Progress bar
        self.ram_progress = ctk.CTkProgressBar(
            ram_frame,
            height=8,
            fg_color=self.theme["bg_tertiary"],
            progress_color=self.theme["accent_glow"]
        )
        self.ram_progress.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))
        self.ram_progress.set(0)
        
        # Disk
        disk_frame = ctk.CTkFrame(metrics_grid, fg_color=self.theme["bg_secondary"], corner_radius=10)
        disk_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        disk_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            disk_frame,
            text="💾 Disk:",
            font=("Segoe UI", 12, "bold"),
            text_color=self.theme["text_primary"]
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.disk_label = ctk.CTkLabel(
            disk_frame,
            text="0%",
            font=("Consolas", 12),
            text_color=self.theme["accent_glow"]
        )
        self.disk_label.grid(row=0, column=1, padx=10, pady=10, sticky="e")
        
        # Disk Progress bar
        self.disk_progress = ctk.CTkProgressBar(
            disk_frame,
            height=8,
            fg_color=self.theme["bg_tertiary"],
            progress_color=self.theme["accent_glow"]
        )
        self.disk_progress.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))
        self.disk_progress.set(0)
        
        # Batéria
        battery_frame = ctk.CTkFrame(metrics_grid, fg_color=self.theme["bg_secondary"], corner_radius=10)
        battery_frame.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        battery_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            battery_frame,
            text="🔋 Batéria:",
            font=("Segoe UI", 12, "bold"),
            text_color=self.theme["text_primary"]
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.battery_label = ctk.CTkLabel(
            battery_frame,
            text="N/A",
            font=("Consolas", 12),
            text_color=self.theme["accent_glow"]
        )
        self.battery_label.grid(row=0, column=1, padx=10, pady=10, sticky="e")
        
        # Battery Progress bar
        self.battery_progress = ctk.CTkProgressBar(
            battery_frame,
            height=8,
            fg_color=self.theme["bg_tertiary"],
            progress_color=self.theme["accent_glow"]
        )
        self.battery_progress.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))
        self.battery_progress.set(0)
    
    def setup_quick_commands(self):
        """Vytvorí widget rýchlych príkazov"""
        commands_frame = ctk.CTkFrame(
            self.dashboard_scroll,
            fg_color=self.theme["bg_tertiary"],
            corner_radius=15,
            border_width=2,
            border_color=self.theme["accent_secondary"]
        )
        commands_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(
            commands_frame,
            text="🚀 RÝCHLE PRÍKAZY",
            font=("Segoe UI", 16, "bold"),
            text_color=self.theme["accent_glow"]
        ).pack(anchor="w", padx=20, pady=15)
        
        # Zoznam rýchlych príkazov
        quick_commands = [
            ("📁 Vypíš zložku", "vypíš zložku .", "Zobrazí obsah aktuálnej zložky"),
            ("🖥️ Systém info", "systémové info", "Zobrazí informácie o systéme"),
            ("📧 Skontroluj emaily", "skontroluj emaily", "Zobrazí najnovšie emaily"),
            ("🌤️ Počasie", "počasie", "Zobrazí predpoveď počasia"),
            ("🔍 Nájdi súbor", "nájdi súbor", "Vyhľadá súbory podľa názvu"),
            ("📊 Analýza kódu", "analyzuj kód", "Analyzuje Python súbory v priečinku")
        ]
        
        for text, command, description in quick_commands:
            cmd_frame = ctk.CTkFrame(commands_frame, fg_color=self.theme["bg_secondary"], corner_radius=8)
            cmd_frame.pack(fill="x", padx=20, pady=5)
            
            btn = ctk.CTkButton(
                cmd_frame,
                text=text,
                command=lambda cmd=command: self.execute_quick_command(cmd),
                height=35,
                fg_color=self.theme["accent_secondary"],
                hover_color=self.theme["accent_glow"],
                font=("Segoe UI", 12),
                corner_radius=6
            )
            btn.pack(fill="x", padx=5, pady=5)
            
            ctk.CTkLabel(
                cmd_frame,
                text=description,
                font=("Segoe UI", 9),
                text_color=self.theme["text_secondary"]
            ).pack(pady=(0, 5))
    
    def setup_modules_status(self):
        """Vytvorí widget stavu modulov"""
        modules_frame = ctk.CTkFrame(
            self.dashboard_scroll,
            fg_color=self.theme["bg_tertiary"],
            corner_radius=15,
            border_width=2,
            border_color=self.theme["accent_secondary"]
        )
        modules_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(
            modules_frame,
            text="🔧 STAV MODULOV",
            font=("Segoe UI", 16, "bold"),
            text_color=self.theme["accent_glow"]
        ).pack(anchor="w", padx=20, pady=15)
        
        # Zoznam modulov
        self.modules_list_frame = ctk.CTkFrame(modules_frame, fg_color="transparent", border_width=0)
        self.modules_list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        self.refresh_modules_status()
    
    def setup_recent_activity(self):
        """Vytvorí widget posledných aktivít"""
        activity_frame = ctk.CTkFrame(
            self.dashboard_scroll,
            fg_color=self.theme["bg_tertiary"],
            corner_radius=15,
            border_width=2,
            border_color=self.theme["accent_secondary"]
        )
        activity_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        
        ctk.CTkLabel(
            activity_frame,
            text="📈 POSLEDNÉ AKTIVITY",
            font=("Segoe UI", 16, "bold"),
            text_color=self.theme["accent_glow"]
        ).pack(anchor="w", padx=20, pady=15)
        
        # Zoznam aktivít
        self.activity_text = ctk.CTkTextbox(
            activity_frame,
            height=120,
            font=("Consolas", 10),
            fg_color=self.theme["bg_secondary"],
            text_color=self.theme["text_secondary"],
            wrap="word"
        )
        self.activity_text.pack(fill="x", padx=20, pady=(0, 15))
        self.activity_text.insert("1.0", "Žiadne aktivity...\n")
        self.activity_text.configure(state="disabled")
    
    def refresh_modules_status(self):
        """Obnoví stav modulov"""
        # Vymaž starý obsah
        for widget in self.modules_list_frame.winfo_children():
            widget.destroy()
        
        if hasattr(self.assistant, 'modules') and self.assistant.modules:
            for module_name, module_instance in self.assistant.modules.items():
                module_frame = ctk.CTkFrame(self.modules_list_frame, fg_color=self.theme["bg_secondary"], corner_radius=8)
                module_frame.pack(fill="x", pady=2)
                
                ctk.CTkLabel(
                    module_frame,
                    text=f"🔧 {module_name}",
                    font=("Segoe UI", 10, "bold"),
                    text_color=self.theme["accent_glow"]
                ).pack(side="left", padx=10, pady=5)
                
                status_label = ctk.CTkLabel(
                    module_frame,
                    text="✅ AKTÍVNY",
                    font=("Segoe UI", 8, "bold"),
                    text_color=self.theme["success"]
                )
                status_label.pack(side="right", padx=10, pady=5)
                
                # Zobraz počet príkazov
                if hasattr(module_instance, 'supported_commands'):
                    commands_count = len(module_instance.supported_commands)
                    commands_label = ctk.CTkLabel(
                        module_frame,
                        text=f"{commands_count} príkazov",
                        font=("Segoe UI", 8),
                        text_color=self.theme["text_secondary"]
                    )
                    commands_label.pack(side="right", padx=5, pady=5)
        else:
            ctk.CTkLabel(
                self.modules_list_frame,
                text="Žiadne moduly",
                font=("Segoe UI", 11),
                text_color=self.theme["text_secondary"]
            ).pack(pady=10)
    
    def execute_quick_command(self, command):
        """Spustí rýchly príkaz"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.add_activity(f"Spustený príkaz: {command}")
        
        # Spustenie príkazu v samostatnom vlákne
        def run_command():
            try:
                response = self.assistant.process_command_sync(command)
                self.after(0, lambda: self.add_activity(f"Odpoveď: {response[:100]}..."))
            except Exception as e:
                self.after(0, lambda: self.add_activity(f"Chyba: {str(e)}"))
        
        threading.Thread(target=run_command, daemon=True).start()
    
    def add_activity(self, activity_text):
        """Pridá aktivitu do histórie"""
        try:
            self.activity_text.configure(state="normal")
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.activity_text.insert("1.0", f"[{timestamp}] {activity_text}\n")
            # Obmedzíme na posledných 15 aktivít
            lines = self.activity_text.get("1.0", "end-1c").split('\n')
            if len(lines) > 15:
                self.activity_text.delete("1.0", "2.0")
            self.activity_text.configure(state="disabled")
        except Exception as e:
            print(f"Chyba pri pridávaní aktivity: {e}")
    
    def update_system_metrics(self):
        """Aktualizuje systémové metriky"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=0.5)
            self.cpu_label.configure(text=f"{cpu_percent:.1f}%")
            self.cpu_progress.set(cpu_percent / 100)
            
            # RAM
            memory = psutil.virtual_memory()
            ram_percent = memory.percent
            self.ram_label.configure(text=f"{ram_percent:.1f}%")
            self.ram_progress.set(ram_percent / 100)
            
            # Disk
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            self.disk_label.configure(text=f"{disk_percent:.1f}%")
            self.disk_progress.set(disk_percent / 100)
            
            # Batéria
            try:
                battery = psutil.sensors_battery()
                if battery:
                    battery_percent = battery.percent
                    self.battery_label.configure(text=f"{battery_percent:.1f}%")
                    self.battery_progress.set(battery_percent / 100)
                    
                    # Zobraziť stav nabíjania
                    if battery.power_plugged:
                        self.battery_label.configure(text=f"{battery_percent:.1f}% (nabíja sa)")
                    else:
                        self.battery_label.configure(text=f"{battery_percent:.1f}%")
                else:
                    self.battery_label.configure(text="N/A")
                    self.battery_progress.set(0)
            except:
                self.battery_label.configure(text="N/A")
                self.battery_progress.set(0)
                
        except Exception as e:
            print(f"Chyba pri aktualizácii metrík: {e}")
    
    def start_dashboard_updates(self):
        """Spustí aktualizáciu dashboardu"""
        def update_loop():
            while self.running:
                try:
                    self.after(0, self.update_system_metrics)
                    time.sleep(2)  # Aktualizácia každé 2 sekundy
                except:
                    break
        
        self.update_thread = threading.Thread(target=update_loop, daemon=True)
        self.update_thread.start()
    
    def refresh_dashboard(self):
        """Obnoví celý dashboard"""
        self.update_system_metrics()
        self.refresh_modules_status()
        self.add_activity("Dashboard obnovený")
        self.dashboard_status.configure(text="✅ Aktualizované")
        
        # Reset status po 2 sekundách
        def reset_status():
            time.sleep(2)
            self.after(0, lambda: self.dashboard_status.configure(text="Live systémové metriky"))
        
        threading.Thread(target=reset_status, daemon=True).start()
    
    def destroy(self):
        """Zastaví aktualizácie pri zničení"""
        self.running = False
        super().destroy()