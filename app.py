import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication

from views import AppView, SplashView


def on_close():
    app_view.show()
    splash_view.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    splash_view = SplashView()
    splash_view.show()

    app_view = AppView()

    QTimer.singleShot(3000, on_close)

    sys.exit(app.exec_())
