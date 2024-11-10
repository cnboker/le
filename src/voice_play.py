import pygame
from config.settings import current_playing_file_path
import threading

pygame.init()
# Initialize the mixer
pygame.mixer.init()


def playsound(wavfile):

    # Load and play the WAV file
    print("play file:", wavfile)
    pygame.mixer.music.load(wavfile)
    current_playing_file_path = wavfile
    pygame.mixer.music.play()

    # Wait until the music finishes playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    current_playing_file_path = ""
    print("play file finished:", wavfile)


