import pickle

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QMainWindow

from voice_recognition.Thread import *
from widgets import AboutWidget, MainWidget, SettingsWidget, GameInfoWidget, StartWidget

class AppView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.press_pos = None

        self.check_saved_state()
        if not self.app_state:
            self.app_state = {
                'user_name': None,
                'active': False,
                'voice_stats': False,
                'health_care': False,
                'volume': 50,
            }

        self.mode = 0

        self.timings_info = []
        self.my_thread = Thread(self.timings_info, self.app_state)

        self.init_ui()

        self.timer_rest = QTimer(self)
        self.timer_rest.timeout.connect(self.sayRest)

        self.timer_eat = QTimer(self)
        self.timer_eat.timeout.connect(self.sayEat)


    def check_saved_state(self):
        try:
            with open('saved_state', 'rb') as handle:
                self.app_state = pickle.load(handle)
        except IOError:
            self.app_state = None

    def save_state(self):
        with open('saved_state', 'wb') as handle:
            pickle.dump(self.app_state, handle)

    def init_ui(self):
        self.setGeometry(500, 300, 320, 320)
        self.setContentsMargins(35, 15, 25, 15)

        self.mode = 0 if self.app_state['user_name'] else -2
        self.setCentralWidget(self.get_main() if self.app_state['user_name'] else self.get_start())

    def switch_layout(self, event, user_name=None):
        if self.mode == -2:
            self.app_state['user_name'] = user_name

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
            print('thread start')

        if not state and self.my_thread.isRunning():
            self.my_thread.terminate()
            print('thread terminate')

    def switch_button(self, obj, state):
        obj.setStyleSheet('border-image: url(res/button_' + \
                          ('enabled' if state else 'disabled') + '.png);' + \
                          'color: ' + ('green;' if state else 'red;'))

    # Widget getters
    def get_start(self):
        start = StartWidget()

        start.to_main.clicked.connect(lambda: self.switch_layout(0, start.user_name.toPlainText()))

        return start

    def get_about(self):
        about = AboutWidget()
        about.to_menu.setDefault(True)

        about.to_menu.clicked.connect(lambda: self.switch_layout(0))
        about.to_gameinfo.clicked.connect(lambda: self.switch_layout(2))
        about.to_main.clicked.connect(lambda: self.switch_layout(0))

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
        settings.to_main.clicked.connect(lambda: self.switch_layout(0))
        settings.to_gameinfo.clicked.connect(lambda: self.switch_layout(2))

        return settings

    def get_gameinfo(self):
        gameinfo = GameInfoWidget(self.timings_info)
        gameinfo.to_gameinfo.setDefault(True)

        gameinfo.to_menu.clicked.connect(lambda: self.switch_layout(0))

        return gameinfo

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
        self.save_state()
        quit(0)

    def sayEat(self):
        thread = ThreadEat()
        thread.start()

    def sayRest(self):
        thread = ThreadRest()
        thread.start()

    def run_or_disable_timers(self, run):
        if run:
            self.timer_eat.start(60000*1)
            self.timer_rest.start(60000*2)
        else:
            self.timer_eat.stop()
            self.timer_rest.stop()
