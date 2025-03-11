import tkinter as tk
from PIL import Image, ImageTk
from ..image_cache import ImageCache

class BaseChapter:
    def __init__(self, root, settings, audio_manager, chapter_info):
        """
        Base class for all chapters
        
        Args:
            root: Tkinter root window
            settings: Settings instance
            audio_manager: AudioManager instance
            chapter_info: Dictionary with chapter information
                - name: Chapter name
                - narration_file: Path to narration file
                - number: Chapter number
        """
        self.root = root
        self.settings = settings
        self.audio = audio_manager
        self.chapter_info = chapter_info
        
        # Initialize image cache
        self.image_cache = ImageCache()
        
        # Initialize UI
        self.setup_ui()
        
        # Text control
        self.text_animation_running = False
        self.current_text = ""
        self.text_history = []
        self.max_history = 100
        
        # Skip mode control
        self.skip_mode = False
        self.skip_speed = 50
        
        # Load narration
        self.carregar_narrativa()
        
    def setup_ui(self):
        """Setup the basic UI elements"""
        # Main frame
        self.frame_jogo = tk.Frame(self.root, bg="#000000")
        self.frame_jogo.pack(fill="both", expand=True)

        # Text area
        self.text_widget = tk.Text(self.frame_jogo, wrap="word", height=5, width=60,
                                 bg="#1a1a1a", fg="white", font=("Arial", 14))
        self.text_widget.pack(side="bottom", fill="x", padx=20, pady=20)

        # Image area
        self.image_label = tk.Label(self.frame_jogo, bg="black")
        self.image_label.pack(expand=True)

        # Buttons
        self.setup_buttons()
        
        # Continue indicator
        self.continue_indicator = tk.Label(self.frame_jogo, text="▼",
                                        fg="white", bg="black",
                                        font=("Arial", 16))
        self.continue_indicator.place(x=980, y=680)
        self.continue_indicator.visible = True
        
        # Bind events
        self.setup_bindings()
        
    def setup_buttons(self):
        """Setup control buttons"""
        # Save button
        self.save_button = tk.Button(self.frame_jogo, text="Salvar",
                                   command=self.salvar_jogo,
                                   bg="#4a4a4a", fg="white",
                                   font=("Arial", 12))
        self.save_button.place(x=20, y=20)
        
        # History button
        self.history_button = tk.Button(self.frame_jogo, text="Histórico",
                                      command=self.mostrar_historico,
                                      bg="#4a4a4a", fg="white",
                                      font=("Arial", 12))
        self.history_button.place(x=120, y=20)
        
        # Skip button
        self.skip_button = tk.Button(self.frame_jogo, text="Pular",
                                   command=self.toggle_skip_mode,
                                   bg="#4a4a4a", fg="white",
                                   font=("Arial", 12))
        self.skip_button.place(x=220, y=20)
        
    def setup_bindings(self):
        """Setup keyboard and mouse bindings"""
        self.frame_jogo.bind("<Button-1>", self.on_click)
        self.root.bind("<space>", self.on_click)
        self.root.bind("<Return>", self.on_click)
        self.root.bind("<Control-s>", lambda e: self.toggle_skip_mode())
        
    def carregar_narrativa(self):
        """Load chapter narration"""
        try:
            with open(self.chapter_info["narration_file"], "r", encoding="utf-8") as file:
                self.narrativa = file.readlines()
            self.index_narrativa = 0
            self.mostrar_proximo_texto()
        except Exception as e:
            self.mostrar_erro("Erro ao carregar narrativa", str(e))
            
    def mostrar_proximo_texto(self):
        """Show next text or image"""
        try:
            if self.index_narrativa < len(self.narrativa):
                linha = self.narrativa[self.index_narrativa].strip()
                self.index_narrativa += 1

                if linha.startswith("[IMG]"):
                    imagem = linha.replace("[IMG]", "").strip()
                    self.mostrar_imagem(imagem)
                    self.mostrar_proximo_texto()
                else:
                    if self.skip_mode and not self.settings.get_setting("text", "skip_unread"):
                        if linha not in self.text_history:
                            self.toggle_skip_mode()
                            self.narrar(linha)
                            return
                    
                    self.narrar(linha)
                    
                    if self.skip_mode:
                        self.root.after(self.skip_speed, self.mostrar_proximo_texto)
        except Exception as e:
            self.mostrar_erro("Erro ao mostrar texto", str(e))
            
    def narrar(self, texto):
        """Display text with animation"""
        try:
            self.current_text = texto
            self.text_animation_running = True
            self.text_widget.delete("1.0", tk.END)
            self.animar_texto(texto, 0)
            
            self.text_history.append(texto)
            if len(self.text_history) > self.max_history:
                self.text_history.pop(0)
        except Exception as e:
            self.mostrar_erro("Erro ao narrar texto", str(e))
            
    def animar_texto(self, texto, index):
        """Animate text typing"""
        try:
            if index < len(texto):
                self.text_widget.insert(tk.END, texto[index])
                self.text_widget.see(tk.END)
                if texto[index] not in [' ', '\n']:
                    self.audio.play_sound("type.wav")
                
                delay = int(self.settings.get_setting("text", "speed") * 1000)
                self.root.after(delay, self.animar_texto, texto, index + 1)
            else:
                self.text_animation_running = False
                if self.settings.get_setting("text", "auto_advance"):
                    self.root.after(2000, self.mostrar_proximo_texto)
        except Exception as e:
            self.mostrar_erro("Erro na animação de texto", str(e))
            
    def mostrar_imagem(self, imagem):
        """Display image with transition"""
        try:
            def carregar_nova_imagem():
                img_tk = self.image_cache.get_image(imagem)
                if img_tk:
                    self.image_label.configure(image=img_tk, bg="black")
                    self.image_label.image = img_tk  # Keep a reference
                    self.fade_in(self.image_label)
                    self.audio.play_sound("transition.wav")
                else:
                    self.mostrar_erro("Erro ao carregar imagem", f"Não foi possível carregar {imagem}")
                
            self.fade_out(self.image_label, carregar_nova_imagem)
        except Exception as e:
            self.mostrar_erro("Erro ao carregar imagem", str(e))
            
    def fade_out(self, widget, callback=None, step=0):
        """Fade out transition"""
        try:
            opacity = 1.0 - (step * 0.1)
            if opacity > 0:
                widget.configure(bg=f"#{int(opacity * 255):02x}{int(opacity * 255):02x}{int(opacity * 255):02x}")
                self.root.after(50, lambda: self.fade_out(widget, callback, step + 1))
            elif callback:
                callback()
        except Exception as e:
            print(f"Erro no fade out: {e}")
            
    def fade_in(self, widget, callback=None, step=0):
        """Fade in transition"""
        try:
            opacity = step * 0.1
            if opacity < 1:
                widget.configure(bg=f"#{int(opacity * 255):02x}{int(opacity * 255):02x}{int(opacity * 255):02x}")
                self.root.after(50, lambda: self.fade_in(widget, callback, step + 1))
            elif callback:
                callback()
        except Exception as e:
            print(f"Erro no fade in: {e}")
            
    def toggle_skip_mode(self, event=None):
        """Toggle skip mode"""
        try:
            self.skip_mode = not self.skip_mode
            
            if self.skip_mode:
                self.skip_button.configure(bg="#6a6a6a", text="Parar")
                self.continue_indicator.configure(text=">>")
                self.mostrar_proximo_texto()
            else:
                self.skip_button.configure(bg="#4a4a4a", text="Pular")
                self.continue_indicator.configure(text="▼")
        except Exception as e:
            self.mostrar_erro("Erro ao alternar modo de pular", str(e))
            
    def mostrar_historico(self):
        """Show text history window"""
        try:
            history_window = tk.Toplevel(self.root)
            history_window.title("Histórico")
            history_window.geometry("600x400")
            
            frame = tk.Frame(history_window)
            frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            scrollbar = tk.Scrollbar(frame)
            scrollbar.pack(side="right", fill="y")
            
            text_area = tk.Text(frame, wrap="word", yscrollcommand=scrollbar.set,
                              bg="#1a1a1a", fg="white", font=("Arial", 12))
            text_area.pack(side="left", fill="both", expand=True)
            
            scrollbar.config(command=text_area.yview)
            
            for texto in self.text_history:
                text_area.insert(tk.END, texto + "\n\n")
            
            text_area.config(state="disabled")
            
            tk.Button(history_window, text="Fechar",
                     command=history_window.destroy,
                     bg="#4a4a4a", fg="white",
                     font=("Arial", 12)).pack(pady=10)
            
            history_window.focus_set()
            
        except Exception as e:
            self.mostrar_erro("Erro ao mostrar histórico", str(e))
            
    def mostrar_erro(self, titulo, mensagem):
        """Show error window"""
        try:
            error_window = tk.Toplevel(self.root)
            error_window.title(titulo)
            error_window.geometry("400x200")
            
            tk.Label(error_window, text=mensagem, wraplength=350).pack(pady=20)
            tk.Button(error_window, text="OK", command=error_window.destroy).pack()
        except Exception as e:
            print(f"Erro ao mostrar erro: {e}")
            
    def on_click(self, event=None):
        """Handle click/keyboard events"""
        try:
            self.audio.play_sound("click.wav")
            
            if self.text_animation_running:
                self.text_widget.delete("1.0", tk.END)
                self.text_widget.insert(tk.END, self.current_text)
                self.text_animation_running = False
            else:
                self.mostrar_proximo_texto()
        except Exception as e:
            self.mostrar_erro("Erro ao processar clique", str(e))
