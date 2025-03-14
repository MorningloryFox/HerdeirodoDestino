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

def iniciar_tela_inicial(root):
    """Cria a tela inicial do jogo com fundo preto e nome do jogo"""
    tela_inicial = tk.Frame(root, bg="black")
    tela_inicial.pack(fill="both", expand=True)

    # Adicionar o nome do jogo centralizado
    tk.Label(
        tela_inicial,
        text="Herdeiro do Destino",
        font=("Arial", 48, "bold"),
        fg="white",
        bg="black"
    ).place(relx=0.5, rely=0.3, anchor="center")

    # Configurações dos botões
    botao_config = {
        "font": ("Arial", 16, "bold"),
        "bg": "#444444",  # Fundo cinza médio
        "fg": "white",    # Texto branco
        "activebackground": "#555555",  # Cor ao passar o mouse
        "activeforeground": "white",
        "borderwidth": 2,
        "relief": "ridge",
        "width": 20,
        "padx": 10,
        "pady": 5
    }

    try:
        # Layout dos botões
        btn_novo_jogo = tk.Button(
            tela_inicial,
            text="Novo Jogo",
            command=lambda: novo_jogo(root),
            **botao_config
        )
        btn_novo_jogo.place(relx=0.5, rely=0.45, anchor="center")

        btn_carregar_jogo = tk.Button(
            tela_inicial,
            text="Carregar Jogo",
            command=lambda: carregar_jogo(),
            **botao_config
        )
        btn_carregar_jogo.place(relx=0.5, rely=0.55, anchor="center")

        btn_configuracoes = tk.Button(
            tela_inicial,
            text="Configurações",
            command=lambda: abrir_configuracoes(),
            **botao_config
        )
        btn_configuracoes.place(relx=0.5, rely=0.65, anchor="center")

        btn_creditos = tk.Button(
            tela_inicial,
            text="Créditos",
            command=lambda: creditos(),
            **botao_config
        )
        btn_creditos.place(relx=0.5, rely=0.75, anchor="center")

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
        root.geometry("800x600")  # Define tamanho da janela para 800x600
        root.resizable(False, False)
        
        root.configure(bg="black")  # Fundo preto inicial
        iniciar_tela_inicial(root)
        root.mainloop()
    except Exception as e:
        print(f"Erro fatal: {e}")  # Fallback para erros críticos

if __name__ == "__main__":
    main()
