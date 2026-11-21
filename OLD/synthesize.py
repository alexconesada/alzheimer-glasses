import time
from gtts import gTTS
import pygame

name = "alex"
voice_file_name = f"voices/{name}.mp3"

# Create an audio file from a given string
speech = gTTS(text=name, lang="es", slow=False) # wav
speech.save(voice_file_name)

# Reproduce the generated file above
pygame.mixer.init()
pygame.mixer.music.load(voice_file_name)
pygame.mixer.music.play()

# Wait until the mp3 playing completes
while pygame.mixer.music.get_busy():
    # Give time to the CPU
    time.sleep(0.1)

print("Done!")

