import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

from views import AppView

if __name__ == '__main__':
    # TODO #1 polish the UI
    # TODO #2 add close button
    # TODO #3 add splash screen
    app = QApplication(sys.argv)
    app_view = AppView()
    app_view.setObjectName('AppView')
    flags = QtCore.Qt.WindowFlags(
        QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint  # | QtCore.Qt.SplashScreen
    )
    app_view.setWindowFlags(flags)
    app_view.setStyleSheet('#AppView { border-image: url(res/border.png); }')
    app_view.show()
    sys.exit(app.exec_())
