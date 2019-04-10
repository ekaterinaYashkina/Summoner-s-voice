import time
import sys

from PyQt5.QtCore import QTimer
from PyQt5 import QtWidgets

from info import *

class InfoWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(QtWidgets.QMainWindow, self).__init__(parent)
        self.ui1 = Ui_FirstWindow()
        self.ui1.setupUi(self)
        self.l = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)



    def showTime(self):
        str_to_print = [str(time.ctime()), '\n']
        removing_elements = []
        for e in self.l:
            if 0 >= int(e['duration']) - int(time.time()-e['time']):
                removing_elements.append(e)
            else:
                str_to_print.append(str(e['name_and_skill'])+" "+str(int(e['duration']) - int(time.time()-e['time'])))
                str_to_print.append('\n')
        for e in removing_elements:
            self.l.remove(e)
        self.ui1.textEdit.setText(''.join(str_to_print))


def main():
    app = QtWidgets.QApplication(sys.argv)
    myapp = InfoWindow()
    myapp.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
