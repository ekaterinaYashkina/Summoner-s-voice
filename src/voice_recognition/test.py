import time
import speech_recognition as sr
import sys

from PyQt5.QtCore import QTimer, QThread
from PyQt5 import QtWidgets

from info import *


class MyThread(QThread):

    def __init__(self, q):
        QThread.__init__(self)
        self.q = q

    def run(self):
        r = sr.Recognizer()

        with sr.Microphone() as source:
            i = 0
            r.adjust_for_ambient_noise(source)
            while True:
                print("Say something", i)
                i += 1

                audio = r.listen(source)

                try:
                    text = r.recognize_google(audio)
                    print(text)
                    self.q.append(text)

                except:
                    print("Something goes wrong")
                # self.q.append(str(i))
                # time.sleep(2)
                # i+=1


class InfoWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(QtWidgets.QMainWindow, self).__init__(parent)
        self.ui1 = Ui_FirstWindow()
        self.ui1.setupUi(self)
        self.q = []
        self.my_thread = MyThread(self.q)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)
        self.my_thread.start()

    def showTime(self):
        str_to_print = [str(time.ctime()), '\n']

        for e in self.q:
            str_to_print.append(e)
            str_to_print.append('\n')

        self.ui1.textEdit.setText(''.join(str_to_print))


def main():
    app = QtWidgets.QApplication(sys.argv)
    myapp = InfoWindow()
    myapp.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
