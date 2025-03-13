import pygame.mixer
import os

class AudioManager:
    def __init__(self):
        """Inicializa o sistema de áudio"""
        try:
            pygame.mixer.init()
        except pygame.error as e:
            print(f"Audio initialization failed: {e}")
            self.audio_enabled = False
        else:
            self.audio_enabled = True
            self.sounds_dir = "assets/sounds"
            self.load_sounds()

    def load_sounds(self):
        """Load sound files and handle errors"""
        """Load sound files"""
        self.sounds = {}
        for sound_file in os.listdir(self.sounds_dir):
            if sound_file.endswith('.wav'):
                sound_path = os.path.join(self.sounds_dir, sound_file)
                try:
                    self.sounds[sound_file] = pygame.mixer.Sound(sound_path)
                except pygame.error as e:
                    print(f"Could not load sound {sound_file}: {e}")
                    self.audio_enabled = False

    def play_sound(self, sound_name):
        """Play a sound if audio is enabled"""
        if self.audio_enabled and sound_name in self.sounds:
            self.sounds[sound_name].play()
