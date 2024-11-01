import pygame



def playsound(wavfile):
    # Initialize the mixer
    pygame.mixer.init()
    # Load and play the WAV file
    print("play file:", wavfile)
    pygame.mixer.music.load(wavfile)
    pygame.mixer.music.play()

    # Wait until the music finishes playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    print("play file finished:", wavfile)