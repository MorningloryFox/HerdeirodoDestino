import pygame.mixer
import os

class AudioManager:
    def __init__(self):
        """Inicializa o sistema de áudio"""
        pygame.mixer.init()
        self.sounds_dir = "assets/sounds"
        self.music_dir = "assets/music"
        self.ensure_directories()
        
        # Volume padrão
        self.music_volume = 0.5
        self.sound_volume = 0.7
        
        # Cache de sons
        self.sound_effects = {}
        
    def ensure_directories(self):
        """Garante que os diretórios de áudio existam"""
        os.makedirs(self.sounds_dir, exist_ok=True)
        os.makedirs(self.music_dir, exist_ok=True)
        
    def load_sound(self, name):
        """Carrega um efeito sonoro do cache ou do disco"""
        if name not in self.sound_effects:
            path = os.path.join(self.sounds_dir, name)
            try:
                sound = pygame.mixer.Sound(path)
                sound.set_volume(self.sound_volume)
                self.sound_effects[name] = sound
            except Exception as e:
                print(f"Erro ao carregar som {name}: {e}")
                return None
        return self.sound_effects[name]
        
    def play_sound(self, name):
        """Toca um efeito sonoro"""
        sound = self.load_sound(name)
        if sound:
            sound.play()
            
    def play_music(self, name, loop=True):
        """Toca uma música de fundo"""
        try:
            path = os.path.join(self.music_dir, name)
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1 if loop else 0)
        except Exception as e:
            print(f"Erro ao tocar música {name}: {e}")
            
    def stop_music(self):
        """Para a música atual"""
        pygame.mixer.music.stop()
        
    def fade_out_music(self, time_ms=1000):
        """Fade out na música atual"""
        pygame.mixer.music.fadeout(time_ms)
        
    def fade_in_music(self, name, time_ms=1000, loop=True):
        """Inicia uma música com fade in"""
        try:
            path = os.path.join(self.music_dir, name)
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(0.0)
            pygame.mixer.music.play(-1 if loop else 0)
            
            # Aumenta gradualmente o volume
            steps = 20
            step_time = time_ms / steps
            step_volume = self.music_volume / steps
            
            for i in range(steps):
                pygame.mixer.music.set_volume(step_volume * (i + 1))
                pygame.time.wait(int(step_time))
        except Exception as e:
            print(f"Erro ao fazer fade in na música {name}: {e}")
            
    def set_music_volume(self, volume):
        """Define o volume da música (0.0 a 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
        
    def set_sound_volume(self, volume):
        """Define o volume dos efeitos sonoros (0.0 a 1.0)"""
        self.sound_volume = max(0.0, min(1.0, volume))
        for sound in self.sound_effects.values():
            sound.set_volume(self.sound_volume)
