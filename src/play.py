import pygame

# Initialize the mixer
pygame.mixer.init()

def playsound(wavfile):
    # Load and play the WAV file
    pygame.mixer.music.load(wavfile)
    pygame.mixer.music.play()

    # Wait until the music finishes playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)