import time
import tkinter as tk
from PIL import Image, ImageTk

class VisualNovel:
    def __init__(self, root, escrever_texto):
        self.root = root
        self.root.title("Herdeiro do Destino")

        # Criando tela preta inicial
        self.frame_jogo = tk.Frame(root, bg="black")
        self.frame_jogo.pack(fill="both", expand=True)

        # Caixa de texto inferior
        self.text_widget = tk.Text(self.frame_jogo, wrap="word", height=5, width=60, bg="#1a1a1a", fg="white", font=("Arial", 14))
        self.text_widget.pack(side="bottom", fill="x", padx=20, pady=20)

        # Área da imagem
        self.image_label = tk.Label(self.frame_jogo, bg="black")
        self.image_label.pack(expand=True)

        self.escrever_texto = escrever_texto
        self.carregar_narrativa()

    def carregar_narrativa(self):
        """Carrega a narrativa do arquivo e inicia a cena"""
        with open("chapters/one/ato1/narration/narracao_ato1.txt", "r", encoding="utf-8") as file:
            self.narrativa = file.readlines()

        self.index_narrativa = 0
        self.mostrar_proximo_texto()

    def mostrar_proximo_texto(self):
        """Mostra o próximo trecho do texto"""
        if self.index_narrativa < len(self.narrativa):
            linha = self.narrativa[self.index_narrativa].strip()
            self.index_narrativa += 1

            if linha.startswith("[IMG]"):
                imagem = linha.replace("[IMG]", "").strip()
                self.mostrar_imagem(imagem)
            else:
                self.narrar(linha)

            self.root.after(2500, self.mostrar_proximo_texto)

    def mostrar_imagem(self, imagem):
        """Exibe a imagem da cena"""
        img = Image.open(imagem)
        img = img.resize((800, 600), Image.ANTIALIAS)
        img_tk = ImageTk.PhotoImage(img)
        self.image_label.config(image=img_tk)
        self.image_label.image = img_tk

    def narrar(self, texto):
        """Escreve a narrativa na caixa de texto"""
        self.escrever_texto(self.text_widget, texto)

def main():
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    visual_novel = VisualNovel(root, None)
    root.mainloop()

if __name__ == "__main__":
    main()
