import os
import pygame
import numpy as np
from array import array

def create_sound_file(filename, frequency, duration, volume=0.5):
    """Create a simple sound file with the given parameters"""
    pygame.mixer.init(44100, -16, 1, 1024)
    
    # Generate samples
    sample_rate = 44100
    n_samples = int(round(duration * sample_rate))
    
    # Setup our numpy array to handle 16 bit ints, which is what we set our mixer to use
    buf = np.zeros((n_samples, 2), dtype=np.int16)
    max_sample = 2**(16 - 1) - 1
    
    for s in range(n_samples):
        t = float(s) / sample_rate  # Time at this sample
        # Sine wave calculations at time t
        sine = np.sin(2.0 * np.pi * frequency * t)
        # Apply volume and convert to 16 bit int
        buf[s][0] = int(sine * max_sample * volume)  # Left channel
        buf[s][1] = int(sine * max_sample * volume)  # Right channel
    
    sound = pygame.sndarray.make_sound(buf)
    
    # Save the sound file
    pygame.sndarray.save(sound, filename)

def main():
    # Ensure the sounds directory exists
    os.makedirs("assets/sounds", exist_ok=True)
    
    # Generate different sound effects
    sounds = {
        "click.wav": (440, 0.1, 0.3),      # Short click sound
        "type.wav": (880, 0.05, 0.1),      # Very short typing sound
        "transition.wav": (330, 0.5, 0.4),  # Longer transition sound
        "save.wav": (660, 0.3, 0.4),       # Save game sound
        "load.wav": (550, 0.3, 0.4),       # Load game sound
    }
    
    for filename, (freq, duration, volume) in sounds.items():
        filepath = os.path.join("assets/sounds", filename)
        create_sound_file(filepath, freq, duration, volume)
        print(f"Created {filename}")
    
    # Create a simple background music file
    create_sound_file(
        os.path.join("assets/music", "background.mp3"),
        frequency=440,
        duration=5.0,
        volume=0.3
    )
    print("Created background music")

if __name__ == "__main__":
    main()
