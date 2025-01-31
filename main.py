import time
import os
import tkinter as tk
from PIL import Image, ImageTk
from chapters.one.ato1 import ato1

def escrever_texto(text_widget, texto):
    """Anima a escrita do texto letra por letra"""
    text_widget.delete("1.0", tk.END)  # Limpa o texto anterior
    for letra in texto:
        text_widget.insert(tk.END, letra)
        text_widget.see(tk.END)  # Rola para o final
        text_widget.update()
        time.sleep(0.05)  # Tempo entre as letras

def iniciar_tela_inicial(root):
    """Cria a tela inicial do jogo com a imagem de fundo expandida"""
    tela_inicial = tk.Frame(root)
    tela_inicial.pack(fill="both", expand=True)

    # Carregar e redimensionar a imagem para ocupar toda a tela
    img = Image.open("assets/imagens/001_tela_inicial.webp")
    img = img.resize((1024, 768), Image.Resampling.LANCZOS)  # Redimensiona para o tamanho da janela
    img_tk = ImageTk.PhotoImage(img)
    
    label_img = tk.Label(tela_inicial, image=img_tk)
    label_img.image = img_tk
    label_img.place(x=0, y=0, relwidth=1, relheight=1)  # Ocupa toda a tela

    # Criando botões invisíveis sobre a imagem
    botao_config = {
        "text": "",
        "bg": "#000000",  # Fundo transparente
        "activebackground": "#000000",
        "borderwidth": 0,
        "highlightthickness": 0
    }

    btn_novo_jogo = tk.Button(tela_inicial, command=lambda: novo_jogo(root), **botao_config)
    btn_novo_jogo.place(x=240, y=419, width=118, height=20)  # Subindo 3px

    btn_carregar_jogo = tk.Button(tela_inicial, command=lambda: carregar_jogo(), **botao_config)
    btn_carregar_jogo.place(x=239, y=467, width=119, height=20)  # Subindo 3px

    btn_creditos = tk.Button(tela_inicial, command=lambda: creditos(), **botao_config)
    btn_creditos.place(x=246, y=511, width=112, height=20)  # Subindo 3px

def novo_jogo(root):
    """Inicia o jogo e abre a primeira cena"""
    for widget in root.winfo_children():
        widget.destroy()  # Remove a tela inicial

    visual_novel = ato1.VisualNovel(root, escrever_texto)
    visual_novel.iniciar_narrativa()

def carregar_jogo():
    print("Carregar Jogo clicado")  # Implementar lógica futuramente

def creditos():
    print("Créditos clicados")  # Implementar lógica futuramente

def main():
    root = tk.Tk()
    root.title("Herdeiro do Destino")  # Define título da janela
    root.geometry("1024x768")  # Define tamanho fixo da janela
    root.configure(bg="black")  # Fundo preto inicial
    root.resizable(False, False)  # Impede redimensionamento
    iniciar_tela_inicial(root)
    root.mainloop()

if __name__ == "__main__":
    main()
