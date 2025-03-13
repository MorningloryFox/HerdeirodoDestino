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
    """Cria a tela inicial do jogo com imagem expandida e botões transparentes"""
    tela_inicial = tk.Frame(root)
    tela_inicial.pack(fill="both", expand=True)

    # Carregar e redimensionar a imagem para ocupar toda a tela
    img = Image.open("assets/imagens/001_tela_inicial.webp")  # Carregar a imagem de fundo




    img = img.resize((1024, 768), Image.Resampling.LANCZOS)  # Ajuste para o tamanho da janela
    img_tk = ImageTk.PhotoImage(img)
    
    label_img = tk.Label(tela_inicial, image=img_tk)
    label_img.image = img_tk
    label_img.place(x=0, y=0, relwidth=1, relheight=1)  # Ocupa toda a tela

    # Criando botões transparentes
    botao_config = {
        "text": "",
        "bg": "white",  # Fundo branco como padrão
        "borderwidth": 0,
        "highlightthickness": 0,
        "relief": "flat",  # Remove bordas 3D
        "activebackground": "white",  # Remove cor ao passar o mouse
    }

    try:
        # Ajuste das coordenadas para a posição correta
        btn_novo_jogo = tk.Button(tela_inicial, command=lambda: novo_jogo(root), **botao_config)
        btn_novo_jogo.place(relx=0.5, rely=0.5, anchor='center', width=20)  # Centraliza o botão e define largura

        btn_carregar_jogo = tk.Button(tela_inicial, command=lambda: carregar_jogo(), **botao_config)
        btn_carregar_jogo.place(relx=0.5, rely=0.6, anchor='center', width=20)  # Centraliza o botão e define largura

        btn_configuracoes = tk.Button(tela_inicial, command=lambda: abrir_configuracoes(), **botao_config)
        btn_configuracoes.place(relx=0.5, rely=0.7, anchor='center', width=20)  # Centraliza o botão e define largura

        btn_creditos = tk.Button(tela_inicial, command=lambda: creditos(), **botao_config)
        btn_creditos.place(relx=0.5, rely=0.8, anchor='center', width=20)  # Centraliza o botão e define largura

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
