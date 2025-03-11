from ...base_chapter import BaseChapter

class VisualNovel(BaseChapter):
    def __init__(self, root, settings, audio_manager):
        chapter_info = {
            "name": "Ato 1",
            "narration_file": "chapters/one/ato1/narration/narracao_ato1.txt",
            "number": 1
        }
        super().__init__(root, settings, audio_manager, chapter_info)
        
        # Start background music
        self.audio.play_music("background.mp3", loop=True)
        
        # Setup auto-save if enabled
        if self.settings.get_setting("auto_save", "enabled"):
            self.setup_auto_save()
            
    def setup_auto_save(self):
        """Configura o timer de auto-save"""
        interval = self.settings.get_setting("auto_save", "interval") * 1000
        self.root.after(interval, self.auto_save)
        
    def auto_save(self):
        """Realiza o auto-save e agenda o próximo"""
        try:
            self.salvar_jogo()
            if self.settings.get_setting("auto_save", "enabled"):
                self.setup_auto_save()
        except Exception as e:
            self.mostrar_erro("Erro no auto-save", str(e))
            
    def salvar_jogo(self):
        """Salva o estado atual do jogo"""
        try:
            self.audio.play_sound("save.wav")
            
            current_scene = self.narrativa[self.index_narrativa].strip()
            if current_scene.startswith("[IMG]"):
                current_scene = self.narrativa[self.index_narrativa - 1].strip()
                
            save_file = self.game_state.save_game(
                chapter=self.chapter_info["name"],
                scene_index=self.index_narrativa,
                description=current_scene[:50] + "..." if len(current_scene) > 50 else current_scene
            )
            
            self.mostrar_mensagem("Jogo salvo com sucesso!")
        except Exception as e:
            self.mostrar_erro("Erro ao salvar jogo", str(e))
            
    def mostrar_mensagem(self, mensagem):
        """Mostra uma mensagem temporária na tela"""
        try:
            msg_label = tk.Label(self.frame_jogo, text=mensagem,
                               bg="#4a4a4a", fg="white",
                               font=("Arial", 12), padx=10, pady=5)
            msg_label.place(x=120, y=20)
            self.root.after(2000, msg_label.destroy)
        except Exception as e:
            print(f"Erro ao mostrar mensagem: {e}")
