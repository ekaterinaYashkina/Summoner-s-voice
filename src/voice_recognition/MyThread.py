import speech_recognition as sr
import time
from PyQt5.QtCore import QThread

from src.voice_recognition.MyIndex import MyIndex


class MyThread(QThread):

    def __init__(self, l: list):
        QThread.__init__(self)
        self.index = MyIndex()
        self.l = l

    def run(self):
        r = sr.Recognizer()

        with sr.Microphone() as source:

            r.adjust_for_ambient_noise(source)

            while True:

                audio = r.listen(source)

                try:
                    t = time.time()
                    text = r.recognize_google(audio)
                    answer, accuracy = self.index.find_most_similar(text)
                    answer['time'] = t
                    if accuracy >= 0.4:
                        self.l.append(answer)

                except:
                    print("Google api error!")
