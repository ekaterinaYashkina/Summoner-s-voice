# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'info.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FirstWindow(object):
    def setupUi(self, FirstWindow):
        FirstWindow.setObjectName("FirstWindow")
        FirstWindow.resize(350, 250)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FirstWindow.sizePolicy().hasHeightForWidth())
        FirstWindow.setSizePolicy(sizePolicy)
        FirstWindow.setMinimumSize(QtCore.QSize(350, 250))
        FirstWindow.setMaximumSize(QtCore.QSize(350, 250))
        FirstWindow.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        FirstWindow.setMouseTracking(False)
        self.centralwidget = QtWidgets.QWidget(FirstWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setEnabled(True)
        self.textEdit.setGeometry(QtCore.QRect(0, 0, 350, 250))
        self.textEdit.setMinimumSize(QtCore.QSize(350, 250))
        self.textEdit.setMaximumSize(QtCore.QSize(350, 250))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(False)
        self.textEdit.setFont(font)
        self.textEdit.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        FirstWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(FirstWindow)
        QtCore.QMetaObject.connectSlotsByName(FirstWindow)

    def retranslateUi(self, FirstWindow):
        _translate = QtCore.QCoreApplication.translate
        FirstWindow.setWindowTitle(_translate("FirstWindow", "Info"))

