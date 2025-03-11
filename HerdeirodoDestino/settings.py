import json
import os
import tkinter as tk
from tkinter import ttk

class Settings:
    def __init__(self):
        self.config_file = "config.json"
        self.default_settings = {
            "audio": {
                "music_volume": 0.5,
                "sound_volume": 0.7
            },
            "text": {
                "speed": 0.05,  # Segundos por caractere
                "auto_advance": False,
                "skip_unread": False
            },
            "display": {
                "fullscreen": True,
                "window_size": "1024x768"
            },
            "auto_save": {
                "enabled": True,
                "interval": 300  # Segundos (5 minutos)
            }
        }
        self.load_settings()
        
    def load_settings(self):
        """Carrega as configurações do arquivo"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, "r", encoding="utf-8") as f:
                    self.settings = json.load(f)
            else:
                self.settings = self.default_settings
                self.save_settings()
        except Exception as e:
            print(f"Erro ao carregar configurações: {e}")
            self.settings = self.default_settings
            
    def save_settings(self):
        """Salva as configurações no arquivo"""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            print(f"Erro ao salvar configurações: {e}")
            
    def get_setting(self, category, key):
        """Obtém uma configuração específica"""
        return self.settings.get(category, {}).get(key, self.default_settings[category][key])
        
    def set_setting(self, category, key, value):
        """Define uma configuração específica"""
        if category not in self.settings:
            self.settings[category] = {}
        self.settings[category][key] = value
        self.save_settings()

class SettingsScreen:
    def __init__(self, root, settings, audio_manager, on_back):
        self.root = root
        self.settings = settings
        self.audio_manager = audio_manager
        self.on_back = on_back
        
        self.frame = tk.Frame(root, bg="#1a1a1a")
        self.frame.pack(fill="both", expand=True)
        
        # Título
        title = tk.Label(self.frame, text="Configurações", font=("Arial", 24, "bold"),
                        bg="#1a1a1a", fg="white")
        title.pack(pady=20)
        
        # Container principal
        main_frame = tk.Frame(self.frame, bg="#1a1a1a")
        main_frame.pack(fill="both", expand=True, padx=50)
        
        # Seção de Áudio
        self.create_audio_section(main_frame)
        
        # Seção de Texto
        self.create_text_section(main_frame)
        
        # Seção de Display
        self.create_display_section(main_frame)
        
        # Seção de Auto-save
        self.create_autosave_section(main_frame)
        
        # Botões
        self.create_buttons()
        
    def create_audio_section(self, parent):
        """Cria a seção de configurações de áudio"""
        section = tk.LabelFrame(parent, text="Áudio", bg="#2a2a2a", fg="white",
                              font=("Arial", 12), padx=10, pady=10)
        section.pack(fill="x", pady=10)
        
        # Volume da música
        tk.Label(section, text="Volume da Música:", bg="#2a2a2a", fg="white").pack()
        music_scale = ttk.Scale(section, from_=0, to=100,
                              value=self.settings.get_setting("audio", "music_volume") * 100,
                              command=lambda v: self.update_music_volume(float(v)))
        music_scale.pack(fill="x")
        
        # Volume dos efeitos
        tk.Label(section, text="Volume dos Efeitos:", bg="#2a2a2a", fg="white").pack()
        sound_scale = ttk.Scale(section, from_=0, to=100,
                              value=self.settings.get_setting("audio", "sound_volume") * 100,
                              command=lambda v: self.update_sound_volume(float(v)))
        sound_scale.pack(fill="x")
        
    def create_text_section(self, parent):
        """Cria a seção de configurações de texto"""
        section = tk.LabelFrame(parent, text="Texto", bg="#2a2a2a", fg="white",
                              font=("Arial", 12), padx=10, pady=10)
        section.pack(fill="x", pady=10)
        
        # Velocidade do texto
        tk.Label(section, text="Velocidade do Texto:", bg="#2a2a2a", fg="white").pack()
        speed_scale = ttk.Scale(section, from_=1, to=10,
                              value=1/self.settings.get_setting("text", "speed"),
                              command=lambda v: self.update_text_speed(float(v)))
        speed_scale.pack(fill="x")
        
        # Auto-advance
        auto_advance_var = tk.BooleanVar(value=self.settings.get_setting("text", "auto_advance"))
        auto_advance = ttk.Checkbutton(section, text="Avanço Automático",
                                     variable=auto_advance_var,
                                     command=lambda: self.update_setting("text", "auto_advance", auto_advance_var.get()))
        auto_advance.pack()
        
        # Skip unread
        skip_unread_var = tk.BooleanVar(value=self.settings.get_setting("text", "skip_unread"))
        skip_unread = ttk.Checkbutton(section, text="Permitir Pular Texto Não Lido",
                                    variable=skip_unread_var,
                                    command=lambda: self.update_setting("text", "skip_unread", skip_unread_var.get()))
        skip_unread.pack()
        
    def create_display_section(self, parent):
        """Cria a seção de configurações de display"""
        section = tk.LabelFrame(parent, text="Display", bg="#2a2a2a", fg="white",
                              font=("Arial", 12), padx=10, pady=10)
        section.pack(fill="x", pady=10)
        
        # Fullscreen
        fullscreen_var = tk.BooleanVar(value=self.settings.get_setting("display", "fullscreen"))
        fullscreen = ttk.Checkbutton(section, text="Tela Cheia",
                                   variable=fullscreen_var,
                                   command=lambda: self.update_setting("display", "fullscreen", fullscreen_var.get()))
        fullscreen.pack()
        
    def create_autosave_section(self, parent):
        """Cria a seção de configurações de auto-save"""
        section = tk.LabelFrame(parent, text="Auto-Save", bg="#2a2a2a", fg="white",
                              font=("Arial", 12), padx=10, pady=10)
        section.pack(fill="x", pady=10)
        
        # Enable auto-save
        autosave_var = tk.BooleanVar(value=self.settings.get_setting("auto_save", "enabled"))
        autosave = ttk.Checkbutton(section, text="Ativar Auto-Save",
                                 variable=autosave_var,
                                 command=lambda: self.update_setting("auto_save", "enabled", autosave_var.get()))
        autosave.pack()
        
        # Auto-save interval
        tk.Label(section, text="Intervalo (minutos):", bg="#2a2a2a", fg="white").pack()
        interval_scale = ttk.Scale(section, from_=1, to=30,
                                 value=self.settings.get_setting("auto_save", "interval") / 60,
                                 command=lambda v: self.update_setting("auto_save", "interval", int(float(v) * 60)))
        interval_scale.pack(fill="x")
        
    def create_buttons(self):
        """Cria os botões de controle"""
        buttons_frame = tk.Frame(self.frame, bg="#1a1a1a")
        buttons_frame.pack(pady=20)
        
        # Botão Voltar
        back_btn = tk.Button(buttons_frame, text="Voltar", command=self.on_back,
                            bg="#4a4a4a", fg="white", font=("Arial", 12),
                            width=15)
        back_btn.pack(side="left", padx=10)
        
    def update_music_volume(self, value):
        """Atualiza o volume da música"""
        volume = value / 100
        self.settings.set_setting("audio", "music_volume", volume)
        if self.audio_manager:
            self.audio_manager.set_music_volume(volume)
            
    def update_sound_volume(self, value):
        """Atualiza o volume dos efeitos sonoros"""
        volume = value / 100
        self.settings.set_setting("audio", "sound_volume", volume)
        if self.audio_manager:
            self.audio_manager.set_sound_volume(volume)
            
    def update_text_speed(self, value):
        """Atualiza a velocidade do texto"""
        speed = 1 / value  # Converte a escala para segundos por caractere
        self.settings.set_setting("text", "speed", speed)
            
    def update_setting(self, category, key, value):
        """Atualiza uma configuração genérica"""
        self.settings.set_setting(category, key, value)
