import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from game_state import GameState

class LoadGameScreen:
    def __init__(self, root, on_load_game, on_back):
        self.root = root
        self.on_load_game = on_load_game
        self.on_back = on_back
        self.game_state = GameState()
        
        # Main frame
        self.frame = tk.Frame(root, bg="#1a1a1a")
        self.frame.pack(fill="both", expand=True)
        
        # Title
        title = tk.Label(self.frame, text="Carregar Jogo", font=("Arial", 24, "bold"), 
                        bg="#1a1a1a", fg="white")
        title.pack(pady=20)
        
        # Saves container
        saves_frame = tk.Frame(self.frame, bg="#1a1a1a")
        saves_frame.pack(fill="both", expand=True, padx=50, pady=20)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(saves_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Save files listbox
        self.saves_listbox = tk.Listbox(saves_frame, bg="#2a2a2a", fg="white",
                                      font=("Arial", 12), selectmode="single",
                                      yscrollcommand=scrollbar.set,
                                      height=10)
        self.saves_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.saves_listbox.yview)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.frame, bg="#1a1a1a")
        buttons_frame.pack(pady=20)
        
        # Load button
        load_btn = tk.Button(buttons_frame, text="Carregar", command=self.load_selected,
                            bg="#4a4a4a", fg="white", font=("Arial", 12),
                            width=15)
        load_btn.pack(side="left", padx=10)
        
        # Back button
        back_btn = tk.Button(buttons_frame, text="Voltar", command=self.on_back,
                            bg="#4a4a4a", fg="white", font=("Arial", 12),
                            width=15)
        back_btn.pack(side="left", padx=10)
        
        self.load_save_files()
        
    def load_save_files(self):
        """Load and display save files in the listbox"""
        self.saves_listbox.delete(0, tk.END)
        self.save_files = self.game_state.get_save_files()
        
        for save in self.save_files:
            display_text = f"{save['timestamp']} - Capítulo {save['chapter']}"
            if save['description']:
                display_text += f" - {save['description']}"
            self.saves_listbox.insert(tk.END, display_text)
            
    def load_selected(self):
        """Load the selected save file"""
        selection = self.saves_listbox.curselection()
        if selection:
            save_file = self.save_files[selection[0]]
            self.on_load_game(save_file['filepath'])

class CreditsScreen:
    def __init__(self, root, on_back):
        self.root = root
        self.frame = tk.Frame(root, bg="#1a1a1a")
        self.frame.pack(fill="both", expand=True)
        
        # Title
        title = tk.Label(self.frame, text="Créditos", font=("Arial", 24, "bold"),
                        bg="#1a1a1a", fg="white")
        title.pack(pady=20)
        
        # Credits text
        credits_text = """
        Herdeiro do Destino
        
        Desenvolvido por:
        [Seu Nome/Equipe]
        
        Programação:
        [Nome do Programador]
        
        Arte:
        [Nome do Artista]
        
        Narrativa:
        [Nome do Escritor]
        
        Música:
        [Nome do Compositor]
        
        Agradecimentos Especiais:
        [Lista de Agradecimentos]
        
        © 2024 Todos os direitos reservados
        """
        
        credits_label = tk.Label(self.frame, text=credits_text, font=("Arial", 12),
                               bg="#1a1a1a", fg="white", justify="left")
        credits_label.pack(pady=20)
        
        # Back button
        back_btn = tk.Button(self.frame, text="Voltar", command=on_back,
                            bg="#4a4a4a", fg="white", font=("Arial", 12),
                            width=15)
        back_btn.pack(pady=20)
