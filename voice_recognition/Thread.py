import threading
import speech_recognition as sr
import time
from PyQt5.QtCore import QThread

from voice_recognition.Index import Index
from stats.statistics import *
from stats.healthcare import *


class Thread(QThread):
    def __init__(self, timings_info: list):
        super().__init__()
        self.index = Index()
        self.timings_info = timings_info
        self.recognizer = sr.Recognizer()

    def run(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)

            while True:
                audio = self.recognizer.listen(source=source)
                t = time.time()
                response = ApiResponse(self.index, self.timings_info, self.recognizer, audio, t)
                response.start()


class ApiResponse(threading.Thread):
    def __init__(self, index, timings_info, recognizer, audio, t):
        super().__init__()
        self.index = index
        self.timings_info = timings_info
        self.recognizer = recognizer
        self.audio = audio
        self.t = t

    def run(self):
        try:
            text = self.recognizer.recognize_google(self.audio)
            ans, acc = self.index.find_most_similar(text)

            if ans['command_name'] == 'statistic':
                name = 'twelvedavinci'
                token = 'RGAPI-548630ff-7321-40fc-a0f9-5f532b52bdbb'
                get_statistics(name, token)
                return
            ans['time'] = self.t
            if acc >= 0.4:
                self.timings_info.append(ans)
        except Exception:
            print("Google API error!")


class ThreadEat(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        remind_to_eat()


class ThreadRest(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        remind_to_rest()
