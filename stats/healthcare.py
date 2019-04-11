import os

from gtts import gTTS
import pygame
from tempfile import TemporaryFile


def remind_to_eat():
    phrase = "My child, Food is not just eating energy. It's an experience. Please, have a snack."
    tts = gTTS(phrase, 'en')
    # tts.save("eat.mp3")

    pygame.mixer.init()
    sf = TemporaryFile()
    tts.write_to_fp(sf)
    sf.seek(0)
    pygame.mixer.music.load(sf)
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play()

    # pygame.mixer.music.load("eat.mp3")
    # pygame.mixer.music.set_volume(1.0)
    # pygame.mixer.music.play()

    while pygame.mixer.music.get_busy() == True:
        pass
    # player.play()
    #
    # if os.path.exists("eat.mp3"):
    #     os.remove("eat.mp3")
    # else:
    #     print("The file does not exist")
    return phrase


def remind_to_rest():
    phrase = "My child, Refresh and renew yourself, your body, your mind, your spirit. Then get back to game."
    tts = gTTS(phrase, 'en')
    # tts.save("sleep.mp3")

    pygame.mixer.init()
    sf = TemporaryFile()
    tts.write_to_fp(sf)
    sf.seek(0)
    pygame.mixer.music.load(sf)
    pygame.mixer.music.play()
    # pygame.mixer.music.load("sleep.mp3")
    # pygame.mixer.music.set_volume(1.0)
    # pygame.mixer.music.play()

    while pygame.mixer.music.get_busy() == True:
        pass
    # player.play()
    #
    # if os.path.exists("sleep.mp3"):
    #     os.remove("sleep.mp3")
    # else:
    #     print("The file does not exist")
    return phrase


