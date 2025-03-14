# Ensure you have the PIL library installed
# You can install it using: pip install pillow
import time
import tkinter as tk
from PIL import Image, ImageTk
from breakout_game import BreakoutGame
from screens import LoadGameScreen, CreditsScreen
from game_state import GameState
from settings import Settings, SettingsScreen
from audio_manager import AudioManager

# Initialize systems
game_state = GameState()
settings = Settings()
audio_manager = AudioManager()

# Define the variable ato1
ato1 = "Some value"  # Replace "Some value" with the appropriate value

def escrever_texto(text_widget, texto):
    """Anima a escrita do texto letra por letra"""
    text_widget.delete("1.0", tk.END)  # Limpa o texto anterior
    for letra in texto:
        text_widget.insert(tk.END, letra)
        text_widget.see(tk.END)  # Rola para o final
        text_widget.update()
        time.sleep(0.05)  # Tempo entre as letras

from colorama import Fore, Style, init
import pygame
from PIL import Image, ImageFont, ImageDraw
import time

def fade_in(widget, duration=0.5):
    """Animação de fade-in para widgets"""
    alpha = 0
    while alpha < 1:
        alpha += 0.05
        widget.config(fg=f"#{int(255*alpha):02x}{int(255*alpha):02x}{int(255*alpha):02x}")
        widget.update()
        time.sleep(duration/20)

def animate_title(label, duration=2):
    """Animação de movimento sutil para o título"""
    import math
    start_time = time.time()
    while time.time() - start_time < duration:
        offset = math.sin(time.time() * 3) * 5
        label.place(relx=0.5, rely=0.2 + offset/1000, anchor="center")
        label.update()
        time.sleep(0.02)

def iniciar_tela_inicial(root):
    """Cria a tela inicial do jogo com tema wuxia e animações"""
    init()  # Inicializa o Colorama
    
    # Carrega fonte temática
    try:
        font_path = "assets/fonts/Cinzel-Bold.ttf"
        title_font = ImageFont.truetype(font_path, 64)
        button_font = ImageFont.truetype(font_path, 24)
    except:
        # Fallback para fontes padrão
        title_font = ("Arial", 64, "bold")
        button_font = ("Arial", 24)
    
    # Configurações da janela
    root.geometry("1024x768")
    root.configure(bg="#0a0a0a")
    
    # Frame principal
    tela_inicial = tk.Frame(root, bg="#0a0a0a")
    tela_inicial.pack(fill="both", expand=True)

    # Título do jogo com animação
    title_label = tk.Label(
        tela_inicial,
        text="Herdeiro do Destino",
        font=title_font,
        fg="#ffffff",
        bg="#0a0a0a"
    )
    title_label.place(relx=0.5, rely=0.2, anchor="center")
    fade_in(title_label)
    animate_title(title_label)

    # Função para criar botões minimalistas com animação
    def criar_botao(texto, comando, posicao_y):
        btn = tk.Label(
            tela_inicial,
            text=texto,
            font=button_font,
            fg="#ffffff",
            bg="#0a0a0a",
            cursor="hand2"
        )
        btn.place(relx=0.5, rely=posicao_y, anchor="center")
        fade_in(btn)
        
        # Efeitos de hover
        btn.bind("<Enter>", lambda e: btn.config(fg="yellow"))
        btn.bind("<Leave>", lambda e: btn.config(fg="#ffffff"))
        btn.bind("<Button-1>", lambda e: comando())
        return btn

    try:
        # Botões com design minimalista
        criar_botao("Novo Jogo", lambda: novo_jogo(root), 0.5)
        criar_botao("Carregar Jogo", lambda: carregar_jogo(), 0.58)
        criar_botao("Configurações", lambda: abrir_configuracoes(), 0.66)
        criar_botao("Créditos", lambda: creditos(), 0.74)

        # Rodapé
        footer = tk.Label(
            tela_inicial,
            text="© 2024 Herdeiro do Destino",
            font=button_font,
            fg="#666666",
            bg="#0a0a0a"
        )
        footer.place(relx=0.5, rely=0.95, anchor="center")
        fade_in(footer)

    except Exception as e:
        mostrar_erro("Erro ao criar interface", str(e))

def mostrar_erro(titulo, mensagem):
    """Mostra uma janela de erro"""
    error_window = tk.Toplevel(root)
    error_window.title(titulo)
    error_window.geometry("400x200")
    
    tk.Label(error_window, text=mensagem, wraplength=350).pack(pady=20)
    tk.Button(error_window, text="OK", command=error_window.destroy).pack()

def novo_jogo(root):
    """Inicia o jogo e abre a primeira cena"""
    try:
        for widget in root.winfo_children():
            widget.destroy()  # Remove a tela inicial

        visual_novel = ato1.VisualNovel(root, escrever_texto, settings, audio_manager)
        visual_novel.iniciar_narrativa()
    except Exception as e:
        mostrar_erro("Erro ao iniciar jogo", str(e))

def carregar_jogo():
    """Abre a tela de carregar jogo"""
    for widget in root.winfo_children():
        widget.destroy()
    
    def on_load_game(save_file):
        """Callback quando um jogo é carregado"""
        save_data = game_state.load_game(save_file)
        if save_data:
            for widget in root.winfo_children():
                widget.destroy()
            
            # Iniciar o jogo no ponto salvo
            visual_novel = ato1.VisualNovel(root, escrever_texto)
            visual_novel.carregar_estado(save_data)
    
    LoadGameScreen(root, on_load_game, lambda: iniciar_tela_inicial(root))

def creditos():
    """Abre a tela de créditos"""
    for widget in root.winfo_children():
        widget.destroy()
    
    CreditsScreen(root, lambda: iniciar_tela_inicial(root))

def abrir_configuracoes():
    """Abre a tela de configurações"""
    try:
        for widget in root.winfo_children():
            widget.destroy()
        
        SettingsScreen(root, settings, audio_manager, lambda: iniciar_tela_inicial(root))
    except Exception as e:
        mostrar_erro("Erro ao abrir configurações", str(e))

def main():
    try:
        global root
        root = tk.Tk()
        root.title("Herdeiro do Destino")  # Define título da janela
        
        # Aplica configurações de display
        root.geometry("1024x768")  # Define tamanho da janela para 1024x768
        root.resizable(False, False)
        
        root.configure(bg="#0a0a0a")  # Fundo escuro inicial
        iniciar_tela_inicial(root)
        root.mainloop()
    except Exception as e:
        print(f"Erro fatal: {e}")  # Fallback para erros críticos

if __name__ == "__main__":
    main()
