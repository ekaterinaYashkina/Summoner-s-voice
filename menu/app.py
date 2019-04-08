import sys
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *

import loading_screen
from System_State import State

class MainWindow(QMainWindow):
    def __init__(self, state):

        super().__init__()
        self.title = "Summoner's voice"
        self.top = 100
        self.left = 100
        self.width = 303
        self.height = 500
        self.sys_state = state
        self.InitUi()
    def InitUi(self):
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        self.setStyleSheet("border-image: url(background.png);")
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.pushButton = QPushButton(self)
        self.pushButton.setGeometry(QRect(70, 90, 161, 161))

        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.start_button_onclick)
        self.label = QLabel(self)
        self.label.setGeometry(QRect(100, 260, 111, 51))
        self.label.setStyleSheet("border-radius: 10px;\n"
                                 "border-image: url(label.png);\n"
                                 "color: #9d7c43")
        self.label.setAlignment(Qt.AlignCenter)

        self.label.setObjectName("label")

        if self.sys_state.working == False:
            self.pushButton.setStyleSheet("border-radius: 80%;\n"
                                          "background-color: #9c7c44;\n"
                                          "border-image: url(disabled.png);\n"
                                          )
            self.label.setText("OFF")
        else:
            self.pushButton.setStyleSheet("border-radius: 80%;\n"
                                          "background-color: #9c7c44;\n"
                                          "border-image: url(enabled.png);\n"
                                          )
            self.label.setText("ON")

        self.pushButton_2 = QPushButton(self)
        self.pushButton_2.setGeometry(QRect(170, 390, 111, 51))
        self.pushButton_2.setStyleSheet("border-image: url(settings.png)")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.settingsWindow_onClick)
        # self.btn.clicked.connect(self.onSettingsClick)
        self.pushButton_3 = QPushButton(self)
        self.pushButton_3.setGeometry(QRect(30, 390, 111, 51))
        self.pushButton_3.setStyleSheet("border-image: url(advice.png)")
        self.pushButton_3.setObjectName("pushButton_3")
        self.show()

    @pyqtSlot()
    def settingsWindow_onClick(self):
        # self.statusBar().showMessage("Switched to window 1")
        self.cams = SettingsWindow(self.sys_state)
        self.cams.show()
        self.close()

    def start_button_onclick(self):
        if self.sys_state.working == False:
            self.pushButton.setStyleSheet("border-radius: 80%;\n"
                                      "background-color: #9c7c44;\n"
                                      "border-image: url(enabled.png);\n")
            self.label.setText("ON")
            self.sys_state.working = True
        else:
            self.pushButton.setStyleSheet("border-radius: 80%;\n"
                                      "background-color: #9c7c44;\n"
                                      "border-image: url(disabled.png);\n")
            self.label.setText("OFF")
            self.sys_state.working = False

        self.sys_state.info()




class SettingsWindow(QDialog):
    def __init__(self, state, parent = None):
        super().__init__(parent)
        self.sys_state = state
        self.setWindowTitle("Settings: Summoner's voice")
        self.setStyleSheet("border-image: url(background.png); color: #9d7c43")
        self.setFixedSize(303, 500)
        self.setLayoutDirection(Qt.RightToLeft)
        self.pushButton_2 = QPushButton(self)
        self.pushButton_2.setGeometry(QRect(170, 390, 111, 51))
        self.pushButton_2.setStyleSheet("border-image: url(back.png)")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.goMainWindow)
        self.pushButton_3 = QPushButton(self)
        self.pushButton_3.setGeometry(QRect(30, 390, 111, 51))
        self.pushButton_3.setStyleSheet("border-image: url(advice.png)")
        self.pushButton_3.setObjectName("pushButton_3")


        # self.statistics = QButtonGroup(self)
        # self.health = QButtonGroup(self)
        self.radioButton =QCheckBox(self)
        self.radioButton.setGeometry(QRect(50, 90, 211, 41))
        self.radioButton.setObjectName("radioButton")
        self.radioButton.setStyleSheet("border-image: none")
        self.radioButton.stateChanged.connect(self.stats_changed)
        if self.sys_state.enable_advice == True:
            self.radioButton.toggle()
        # self.statistics.addButton(self.radioButton)
        self.radioButton_2 = QCheckBox(self)
        self.radioButton_2.setGeometry(QRect(50, 150, 211, 20))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_2.setStyleSheet("border-image: none")
        self.radioButton_2.stateChanged.connect(self.health_changed)
        if self.sys_state.enable_healthcare == True:
            self.radioButton_2.toggle()
        # self.health.addButton(self.radioButton_2)
        self.horizontalSlider = QSlider(self)
        self.horizontalSlider.setGeometry(QRect(70, 260, 161, 22))
        self.horizontalSlider.setLayoutDirection(Qt.LeftToRight)
        self.horizontalSlider.setOrientation(Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.setStyleSheet("border-image: none")
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setValue(self.sys_state.volume)
        self.horizontalSlider.valueChanged.connect(self.volume_changed)
        self.label = QLabel(self)
        self.label.setGeometry(QRect(120, 240, 57, 16))
        self.label.setObjectName("label")
        self.label.setStyleSheet("border-image: none")
        self.radioButton.setText( "    Enable voice statistics               ")
        self.radioButton_2.setText("God healthcare                           ")
        self.label.setText("Volume")

    def goMainWindow(self):
        self.cams = MainWindow(self.sys_state)
        self.cams.show()
        self.close()

    def stats_changed(self, state):
        if state == Qt.Checked:
            self.sys_state.enable_advice = True
        else:
            self.sys_state.enable_advice = False
        self.sys_state.info()


    def health_changed(self, state):
        if state == Qt.Checked:
            self.sys_state.enable_healthcare = True
        else:
            self.sys_state.enable_healthcare = False
        self.sys_state.info()

    def volume_changed(self):
        vol = self.horizontalSlider.value()
        self.sys_state.volume = vol
        self.sys_state.info()


class StartApp(QMainWindow, loading_screen.Ui_LoadingWindow):
    def __init__(self, state):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)
        self.sys_state = state

        self.show()
        QTimer.singleShot(5000, self.change_main)

    def change_main(self):
        self.cams = MainWindow(self.sys_state)
        self.cams.show()
        self.close()

        # Это нужно для инициализации нашего дизайна


if __name__ == '__main__':
    app=QApplication(sys.argv)
    sys_state = State()
    ex = StartApp(sys_state)
    sys.exit(app.exec_())
