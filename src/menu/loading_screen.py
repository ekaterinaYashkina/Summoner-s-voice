# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LoadingWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("LoadingWindow")
        MainWindow.resize(700, 200)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.centralWidget.setStyleSheet("border-image: url(splash.png);")
        self.centralWidget.setFixedSize(700, 200)
        # self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        # self.pushButton.setGeometry(QtCore.QRect(70, 90, 161, 161))
        # self.pushButton.setStyleSheet("border-radius: 80%;\n"
        # "background-color: #9c7c44;\n"
        # "border-image: url(button.png);\n"
        #                               )
        # self.pushButton.setText("")
        # self.pushButton.setObjectName("pushButton")
        # self.label = QtWidgets.QLabel(self.centralWidget)
        # self.label.setGeometry(QtCore.QRect(100, 260, 111, 51))
        # self.label.setStyleSheet("border-radius: 10px;\n"
        #     "border-image: url(label.png);\n"
        #     "color: #9d7c43")
        # self.label.setAlignment(QtCore.Qt.AlignCenter)
        #
        # self.label.setObjectName("label")
        #
        # self.pushButton_2 = QtWidgets.QPushButton(self.centralWidget)
        # self.pushButton_2.setGeometry(QtCore.QRect(170, 390, 111, 51))
        # self.pushButton_2.setStyleSheet("border-image: url(settings.png)")
        # self.pushButton_2.setObjectName("pushButton_2")
        # self.pushButton_3 = QtWidgets.QPushButton(self.centralWidget)
        # self.pushButton_3.setGeometry(QtCore.QRect(30, 390, 111, 51))
        # self.pushButton_3.setStyleSheet("border-image: url(advice.png)")
        # self.pushButton_3.setObjectName("pushButton_3")

        MainWindow.setCentralWidget(self.centralWidget)
        # self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        # self.mainToolBar.setObjectName("mainToolBar")
        # MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        # self.statusBar = QtWidgets.QStatusBar(MainWindow)
        # self.statusBar.setObjectName("statusBar")
        # MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Summoner's voice"))
        # self.label.setText(_translate("MainWindow", "SV is ON"))