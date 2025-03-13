import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont
from game_state import GameState

class ButtonManager:
    """Gerenciador de botões com cache e fallback melhorado"""
    _buttons = {}

    @classmethod
    def get_button(cls, text, image_path="assets/imagens/button.png"):
        key = (text, image_path)
        if key not in cls._buttons:
            cls._buttons[key] = cls._create_button_image(text, image_path)
        return cls._buttons[key]

    @staticmethod
    def _create_button_image(text, image_path):
        try:
            base = Image.open(image_path).convert("RGB")  # Usar RGB em vez de RGBA
        except (FileNotFoundError, AttributeError):
            # Fallback aprimorado com borda visível
            base = Image.new('RGB', (160, 40), (74, 74, 74))
            draw = ImageDraw.Draw(base)
            draw.rounded_rectangle(
                [(0, 0), (159, 39)],
                radius=10,
                fill="#4a4a4a",
                outline="#666666",
                width=2
            )

        draw = ImageDraw.Draw(base)
        
        try:
            font = ImageFont.truetype("arial.ttf", 14)
        except:
            font = ImageFont.load_default(size=14)

        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = (base.width - text_width) / 2
        text_y = (base.height - text_height) / 2 - 2  # Ajuste fino de posição

        # Efeito de sombra mais pronunciado
        draw.text((text_x+1, text_y+1), text, font=font, fill="#333333")
        draw.text((text_x, text_y), text, font=font, fill="white")

        return ImageTk.PhotoImage(base)

class EnhancedButton(tk.Button):
    """Botão com efeitos visuais aprimorados"""
    def __init__(self, master, text, command=None, **kwargs):
        self.image = ButtonManager.get_button(text)
        super().__init__(
            master,
            image=self.image,
            command=command,
            borderwidth=0,
            highlightthickness=0,
            activebackground="#5a5a5a",
            bg="#2a2a2a",  # Cor de fundo combinando com o tema
            **kwargs
        )
        self.bind("<Enter>", self._on_hover)
        self.bind("<Leave>", self._on_leave)

    def _on_hover(self, e):
        self.config(background="#4a4a4a")

    def _on_leave(self, e):
        self.config(background="#2a2a2a")

class LoadGameScreen:
    def __init__(self, root, on_load_game, on_back):
        self.root = root
        self.on_load_game = on_load_game
        self.on_back = on_back
        self.game_state = GameState()

        # Configuração principal
        self.frame = tk.Frame(root, bg="#1a1a1a")
        self.frame.pack(fill="both", expand=True)

        # Layout grid
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # Título
        tk.Label(self.frame, text="Carregar Jogo", font=("Arial", 24, "bold"),
                bg="#1a1a1a", fg="white").grid(row=0, column=0, pady=20)

        # Lista de saves
        self._create_saves_list()

        # Botões
        button_frame = tk.Frame(self.frame, bg="#1a1a1a")
        button_frame.grid(row=2, column=0, pady=20)
        
        EnhancedButton(button_frame, text="Carregar", command=self.load_selected).pack(side="left", padx=10)
        EnhancedButton(button_frame, text="Voltar", command=self.on_back).pack(side="left", padx=10)

    def _create_saves_list(self):
        container = tk.Frame(self.frame, bg="#1a1a1a")
        container.grid(row=1, column=0, sticky="nsew", padx=50, pady=10)

        # Scrollbar
        scrollbar = ttk.Scrollbar(container)
        scrollbar.pack(side="right", fill="y")

        # Listbox estilizada
        self.saves_listbox = tk.Listbox(
            container,
            bg="#2a2a2a",
            fg="white",
            selectbackground="#3a3a3a",
            font=("Arial", 12),
            yscrollcommand=scrollbar.set,
            height=8,
            relief="flat"
        )
        self.saves_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.saves_listbox.yview)

    def load_save_files(self):
        self.saves_listbox.delete(0, tk.END)
        self.save_files = self.game_state.get_save_files()
        for save in self.save_files:
            display_text = f"{save['timestamp']} - Capítulo {save['chapter']}"
            if save['description']:
                display_text += f" - {save['description']}"
            self.saves_listbox.insert(tk.END, display_text)

    def load_selected(self):
        if selection := self.saves_listbox.curselection():
            self.on_load_game(self.save_files[selection[0]]['filepath'])

class CreditsScreen:
    def __init__(self, root, on_back):
        self.root = root
        self.frame = tk.Frame(root, bg="#1a1a1a")
        self.frame.pack(fill="both", expand=True)

        # Conteúdo principal
        tk.Label(self.frame, text="Créditos", font=("Arial", 24, "bold"),
                bg="#1a1a1a", fg="white").pack(pady=20)

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
        
        tk.Label(self.frame, text=credits_text, font=("Arial", 12),
                bg="#1a1a1a", fg="white", justify="left").pack(pady=10)

        EnhancedButton(self.frame, text="Voltar", command=on_back).pack(pady=20)