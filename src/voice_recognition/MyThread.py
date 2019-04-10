import threading
import speech_recognition as sr
import time
from PyQt5.QtCore import QThread

from src.voice_recognition.MyIndex import MyIndex


class MyThread(QThread):

    def __init__(self, l: list):
        QThread.__init__(self)
        self.index = MyIndex()
        self.l = l
        self.r = sr.Recognizer()

    def run(self):
        with sr.Microphone() as source:
            self.r.adjust_for_ambient_noise(source)

            while True:
                audio = self.r.listen(source=source)
                t = time.time()
                response = ApiResponse(self.index, self.l, self.r, audio, t)
                response.start()


class ApiResponse(threading.Thread):
    def __init__(self, index, l, r, audio, t):
        threading.Thread.__init__(self)
        self.index = index
        self.l = l
        self.r = r
        self.audio = audio
        self.t = t

    def run(self):
        try:
            text = self.r.recognize_google(self.audio)
            answer, accuracy = self.index.find_most_similar(text)
            answer['time'] = self.t
            if accuracy >= 0.4:
                self.l.append(answer)

        except:
            print("Google api error!")
