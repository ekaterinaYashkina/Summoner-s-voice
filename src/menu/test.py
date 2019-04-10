import json
import time

import speech_recognition as sr
import textdistance
from PyQt5.QtCore import QThread


class MyIndex(object):
    def __init__(self):
        with open('phrases2.json') as f:
            self.index = dict(json.load(f))

    def find_most_similar(self, query):
        answer_best_score = dict()

        for phrase in self.index:
            answer_best_score[phrase] = textdistance.editex.normalized_similarity(phrase, query)
            for paraphrase in self.index[phrase]["paraphrases"]:
                v = textdistance.editex.normalized_similarity(paraphrase, query)
                if v > answer_best_score[phrase]:
                    answer_best_score[phrase] = v

        result = ''
        result_v = -1
        for k in answer_best_score:
            if answer_best_score[k] > result_v:
                result = k
                result_v = answer_best_score[k]
        print(result_v)
        return {"name_and_skill": result, "duration": self.index[result]['duration']}, result_v


class MyThread(QThread):
    def __init__(self, timings_list: list):
        QThread.__init__(self)
        self.index = MyIndex()
        self.timings_list = timings_list

        self.flag = True

    def run(self):
        r = sr.Recognizer()
        print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        with sr.Microphone() as source:
            i = 0
            r.adjust_for_ambient_noise(source)
            while self.flag:
                print("Say something", i)
                i += 1

                audio = r.listen(source)

                try:
                    t = time.time()
                    text = r.recognize_google(audio)
                    answer, accuracy = self.index.find_most_similar(text)
                    answer['time'] = t
                    if accuracy >= 0.4:
                        self.timings_list.append(answer)
                except Exception:
                    print("Google API error!")


# class InfoWindow(QtWidgets.QMainWindow):
#     def __init__(self, parent=None):
#         super(QtWidgets.QMainWindow, self).__init__(parent)
#         self.ui1 = Ui_FirstWindow()
#         self.ui1.setupUi(self)
#
#         self.l = []
#         self.my_thread = MyThread(self.l)
#
#
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.showTime)
#         self.timer.start(1000)
#
#         self.my_thread.start()
#     def showTime(self):
#         str_to_print = [str(time.ctime()), '\n']
#         removing_elements = []
#         for e in self.l:
#             if 0 >= int(e['duration']) - int(time.time()-e['time']):
#                 removing_elements.append(e)
#             else:
#                 str_to_print.append(str(e['name_and_skill'])+" "+str(int(e['duration']) - int(time.time()-e['time'])))
#                 str_to_print.append('\n')
#         for e in removing_elements:
#             self.l.remove(e)
#         self.ui1.textEdit.setText(''.join(str_to_print))
#
#
# def main():
#     app = QtWidgets.QApplication(sys.argv)
#     myapp = InfoWindow()
#     myapp.show()
#     sys.exit(app.exec_())
#
#
# if __name__ == '__main__':
#     main()
