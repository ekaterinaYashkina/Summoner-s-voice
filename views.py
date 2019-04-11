import pickle

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget

from voice_recognition.Thread import Thread, ThreadEat, ThreadRest
from widgets import AboutWidget, MainWidget, SettingsWidget, GameInfoWidget, StartWidget


def check_saved_state():
    try:
        with open('saved_state', 'rb') as handle:
            return pickle.load(handle)
    except IOError:
        return {
            'user_name': None,
            'active': False,
            'voice_stats': False,
            'health_care': False,
            'volume': 50,
        }


def save_state(app_state):
    with open('saved_state', 'wb') as handle:
        pickle.dump(app_state, handle)


def move_center(self):
    center = QDesktopWidget().availableGeometry().center()
    rect = self.frameGeometry()
    rect.moveCenter(center)
    self.move(rect.topLeft())


class SplashView(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        flags = QtCore.Qt.WindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | QtCore.Qt.SplashScreen
        )
        self.setWindowFlags(flags)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(400, 287)

        move_center(self)

    def paintEvent(self, event=None):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, QPixmap('res/splash.png'))

    def closeEvent(self, event):
        event.accept()


class AppView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.press_pos = None

        self.app_state = check_saved_state()

        self.timings_info = []
        self.my_thread = Thread(self.timings_info, self.app_state)

        self.mode = 0
        self.init_ui()

        self.timer_rest = QTimer(self)
        self.timer_rest.timeout.connect(self.say_rest)

        self.timer_eat = QTimer(self)
        self.timer_eat.timeout.connect(self.say_eat)

    def init_ui(self):
        flags = QtCore.Qt.WindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint  # | QtCore.Qt.SplashScreen
        )
        self.setWindowFlags(flags)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setFixedSize(317, 479)
        self.setContentsMargins(28, 25, 25, 5)

        move_center(self)

        self.mode = 0 if self.app_state['user_name'] else -2
        self.setCentralWidget(self.get_main() if self.app_state['user_name'] else self.get_start())

    def switch_layout(self, event, obj=None):
        if self.mode == -2:
            try:
                if not obj.user_name.text():
                    obj.warning.setText('Invalid username!')
                    return
                self.app_state['user_name'] = obj.user_name.text()
            except AttributeError:
                obj.warning.setText('Invalid username!')
                return

        if event == -1:
            self.setCentralWidget(self.get_about())
        elif event == 0:
            self.setCentralWidget(self.get_main())
        elif event == 1:
            self.setCentralWidget(self.get_settings())
        elif event == 2:
            self.setCentralWidget(self.get_gameinfo())
        self.mode = event

    def switch_state(self, key, value=None, obj=None):
        self.app_state[key] = (not self.app_state[key] if value is None else value)

        if key == 'active':
            self.switch_active(obj, self.app_state[key])
        elif key == 'voice_stats':
            self.switch_button(obj.voice_stats, self.app_state[key])
        elif key == 'health_care':
            self.switch_button(obj.health_care, self.app_state[key])
            self.run_or_disable_timers(self.app_state[key])
        elif key == 'volume':
            obj.volume.setValue(value)
            obj.volume_value.setText(str(value))
        print(self.app_state)

    def switch_active(self, obj, state):
        obj.activate.setStyleSheet('border-image: url(res/' + \
                                   ('activated' if state else 'deactivated') + \
                                   '.png)')

        obj.status.setText("ACTIVATED" if state else "DEACTIVATED")
        obj.status.setStyleSheet('border-image: url(res/button_' + \
                                 ('enabled' if state else 'disabled') + '.png);' + \
                                 'color: ' + ('green;' if state else 'red;'))

        if state and not self.my_thread.isRunning():
            self.my_thread.start()
            print('my_thread start')

        if not state and self.my_thread.isRunning():
            self.my_thread.terminate()
            print('my_thread terminate')

    def switch_button(self, obj, state):
        obj.setStyleSheet('border-image: url(res/button_' + \
                          ('enabled' if state else 'disabled') + '.png);' + \
                          'color: ' + ('green;' if state else 'red;'))

    # Widget getters
    def get_start(self):
        start = StartWidget()

        start.to_main.clicked.connect(lambda: self.switch_layout(0, start))
        start.to_quit.clicked.connect(lambda: quit(0))

        return start

    def get_about(self):
        about = AboutWidget()
        about.to_menu.setDefault(True)

        about.to_menu.clicked.connect(lambda: self.switch_layout(0))
        about.to_gameinfo.clicked.connect(lambda: self.switch_layout(2))
        about.to_main.clicked.connect(lambda: self.switch_layout(0))
        about.to_quit.clicked.connect(lambda: quit(0))

        return about

    def get_main(self):
        main = MainWidget()
        main.to_menu.setDefault(True)
        self.switch_active(main, self.app_state['active'])

        main.activate.clicked.connect(lambda: self.switch_state('active', obj=main))
        main.status.clicked.connect(lambda: self.switch_state('active', obj=main))

        main.to_gameinfo.clicked.connect(lambda: self.switch_layout(2))
        main.to_about.clicked.connect(lambda: self.switch_layout(-1))
        main.to_settings.clicked.connect(lambda: self.switch_layout(1))
        main.to_quit.clicked.connect(lambda: quit(0))

        return main

    def get_settings(self):
        settings = SettingsWidget()
        settings.to_menu.setDefault(True)
        self.switch_button(settings.voice_stats, self.app_state['voice_stats'])
        self.switch_button(settings.health_care, self.app_state['health_care'])
        settings.volume.setValue(self.app_state['volume'])
        settings.volume_value.setText(str(self.app_state['volume']))

        settings.voice_stats.clicked.connect(lambda: self.switch_state('voice_stats', obj=settings))
        settings.health_care.clicked.connect(lambda: self.switch_state('health_care', obj=settings))
        settings.volume.valueChanged.connect(lambda: self.switch_state('volume', settings.volume.value(), settings))

        settings.to_menu.clicked.connect(lambda: self.switch_layout(0))
        settings.to_gameinfo.clicked.connect(lambda: self.switch_layout(2))
        settings.to_main.clicked.connect(lambda: self.switch_layout(0))
        settings.to_quit.clicked.connect(lambda: quit(0))

        return settings

    def get_gameinfo(self):
        gameinfo = GameInfoWidget(self.timings_info)
        gameinfo.to_gameinfo.setDefault(True)

        gameinfo.to_menu.clicked.connect(lambda: self.switch_layout(0))
        gameinfo.to_quit.clicked.connect(lambda: quit(0))

        return gameinfo

    def paintEvent(self, event=None):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, QPixmap('res/border.png'))

    # Make the window draggable
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.press_pos = event.pos()  # remember starting position

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.press_pos = None

    def mouseMoveEvent(self, event):
        if self.press_pos:  # follow the mouse
            self.move(self.pos() + (event.pos() - self.press_pos))

    def closeEvent(self, event):
        save_state(self.app_state)

        self.my_thread.terminate()
        self.my_thread.exit(0)
        self.my_thread.quit()
        self.my_thread.deleteLater()
        print("QUIT")

        quit(0)

    # TODO why do we need to start a NEW my_thread every time?
    def say_eat(self):
        thread = ThreadEat()
        thread.start()

    def say_rest(self):
        thread = ThreadRest()
        thread.start()

    def run_or_disable_timers(self, run):
        if run:
            self.timer_eat.start(60000 * 1)
            self.timer_rest.start(60000 * 2)
        else:
            self.timer_eat.stop()
            self.timer_rest.stop()
