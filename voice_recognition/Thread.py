import threading
import speech_recognition as sr
import time
from PyQt5.QtCore import QThread

from voice_recognition.Index import Index
from stats.statistics import *
from stats.healthcare import *


class Thread(QThread):
    def __init__(self, timings_info: list, app_state):
        super().__init__()
        self.index = Index()
        self.timings_info = timings_info
        self.recognizer = sr.Recognizer()
        self.app_state = app_state

    def run(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            i = 0
            while True:
                print(i)
                audio = self.recognizer.listen(source=source, phrase_time_limit=10)
                print("PROCESSING")
                for thread in threading.enumerate():
                    print('    ' + thread.name)
                t = time.time()
                response = ApiResponse(self.index, self.timings_info, self.recognizer, audio, t, self.app_state)
                response.setDaemon(True)

                response.start()
                i += 1
                print(i)


mutex = threading.Lock()
mutex2 = threading.Lock()


class ApiResponse(threading.Thread):
    def __init__(self, index, timings_info, recognizer, audio, t, app_state):
        super().__init__()
        self.index = index
        self.timings_info = timings_info
        self.recognizer = recognizer
        self.audio = audio
        self.t = t
        self.app_state = app_state

    def run(self):
        mutex2.acquire()
        try:
            text = self.recognizer.recognize_google(self.audio)
            ans, acc = self.index.find_most_similar(text)

            if ans['command_name'] == 'statistic':
                name = self.app_state['user_name']
                token = 'RGAPI-548630ff-7321-40fc-a0f9-5f532b52bdbb'
                print("Statistic")
                get_statistics(name, token)

                return
            ans['time'] = self.t
            if acc >= 0.4:
                self.timings_info.append(ans)
        except Exception:
            print("Google API error!")
        mutex2.release()


class ThreadEat(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        mutex.acquire()
        remind_to_eat()
        mutex.release()


class ThreadRest(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        mutex.acquire()
        remind_to_rest()
        mutex.release()
