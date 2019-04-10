import time
from PyQt5.QtCore import Qt, QTimer

from PyQt5.QtWidgets import QWidget, QPushButton, QSlider, QHBoxLayout, QVBoxLayout, QLabel, QTextEdit


def get_hbox_top(to_menu, to_gameinfo):
    hbox_top = QHBoxLayout()
    hbox_top.setSpacing(0)
    hbox_top.addWidget(to_menu)
    hbox_top.addWidget(to_gameinfo)

    return hbox_top


class StartWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.user_name = QTextEdit()
        self.to_main = QPushButton('Submit')
        # self.info = QLabel()

        self.init_ui()

    def init_ui(self):
        # self.info.setAlignment(Qt.AlignTop)
        # self.info.setStyleSheet('color: white')
        # self.info.setText('Here is the info about timings')

        vbox = QVBoxLayout()
        vbox.addWidget(self.user_name)
        vbox.addWidget(self.to_main)

        self.setLayout(vbox)


class PushButton(QPushButton):
    def __init__(self, text=None, x=48, y=48, img_path='button_disabled.png', color='white'):
        super().__init__(text)

        self.setFixedSize(x, y)
        self.setStyleSheet(f'border-image: url(res/{img_path});' + \
                           f'color: {color};')


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.to_menu = QPushButton('Menu')
        self.to_gameinfo = QPushButton('Game Info')
        self.activate = PushButton(x=250, y=250, img_path='deactivated.png')
        self.status = PushButton('DEACTIVATED', int(167 * 1.5), int(33 * 1.5), 'button_disabled.png', 'red')
        self.to_about = PushButton(img_path='about.png')
        self.to_settings = PushButton(img_path='settings.png')

        self.init_ui()

    def init_ui(self):
        hbox = QHBoxLayout()
        hbox.addWidget(self.to_about)
        hbox.addStretch()
        hbox.addWidget(self.to_settings)

        vbox = QVBoxLayout()
        vbox.addLayout(get_hbox_top(self.to_menu, self.to_gameinfo))
        vbox.addWidget(self.activate)
        vbox.addWidget(self.status)
        vbox.addStretch()
        vbox.addLayout(hbox)

        self.setLayout(vbox)


class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.to_menu = QPushButton('Menu')
        self.to_gameinfo = QPushButton('Game Info')
        self.voice_stats = PushButton('Voice statistics', int(167 * 1.5), int(33 * 1.5))
        self.health_care = PushButton('Health care', int(167 * 1.5), int(33 * 1.5))
        self.to_about = PushButton(img_path='about.png')
        self.to_main = PushButton(img_path='back.png')
        self.volume_label = QLabel('Volume: ')
        self.volume_value = QLabel()
        self.volume = QSlider(Qt.Horizontal)

        self.init_ui()

    def init_ui(self):
        self.volume_label.setStyleSheet('color: white')
        self.volume_value.setStyleSheet('color: white')
        self.volume.setFocusPolicy(Qt.StrongFocus)
        self.volume.setTickPosition(QSlider.TicksBothSides)
        self.volume.setTickInterval(10)
        self.volume.setSingleStep(1)

        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.to_main)

        hbox_volume = QHBoxLayout()
        hbox_volume.setAlignment(Qt.AlignLeft)
        hbox_volume.addWidget(self.volume_label)
        hbox_volume.addWidget(self.volume_value)

        vbox = QVBoxLayout()
        vbox.addLayout(get_hbox_top(self.to_menu, self.to_gameinfo))
        vbox.addWidget(self.voice_stats)
        vbox.addWidget(self.health_care)
        vbox.addStretch(1)
        vbox.addLayout(hbox_volume)
        vbox.addWidget(self.volume)
        vbox.addStretch()
        vbox.addLayout(hbox)

        self.setLayout(vbox)


class AboutWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.to_menu = QPushButton('Menu')
        self.to_gameinfo = QPushButton('Game Info')
        self.about = QLabel()
        self.to_main = PushButton(img_path='back.png')

        self.init_ui()

    def init_ui(self):
        self.about.setAlignment(Qt.AlignCenter)
        self.about.setStyleSheet('color: white;')
        self.about.setText('This project was done by:\n' + \
                           'Ekaterina Yashkina\n' + \
                           'Farid Kopzhassarov\n' + \
                           'Amir Nazyrov\n' + \
                           'Mikhail Fadeev')

        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.to_main)

        vbox = QVBoxLayout()
        vbox.addLayout(get_hbox_top(self.to_menu, self.to_gameinfo))
        vbox.addWidget(self.about)
        vbox.addStretch()
        vbox.addLayout(hbox)

        self.setLayout(vbox)


class GameInfoWidget(QWidget):
    def __init__(self, l: list):
        super().__init__()
        self.to_menu = QPushButton('Menu')
        self.to_gameinfo = QPushButton('Game Info')
        self.info = QLabel()
        self.list_with_info = l
        self.init_ui()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showInfo)
        self.timer.start(1000)

    def init_ui(self):
        self.info.setAlignment(Qt.AlignTop)
        self.info.setStyleSheet('color: white')
        # self.info.setText('Here is the info about timings')

        vbox = QVBoxLayout()
        vbox.addLayout(get_hbox_top(self.to_menu, self.to_gameinfo))
        vbox.addWidget(self.info)

        self.setLayout(vbox)

    def showInfo(self):
        str_to_print = [str(time.ctime()), '\n']
        removing_elements = []
        for e in self.list_with_info:
            if 0 >= int(e['duration']) - int(time.time() - e['time']):
                removing_elements.append(e)
            else:
                str_to_print.append(
                    str(e['name_and_skill']) + " " + str(int(e['duration']) - int(time.time() - e['time'])))
                str_to_print.append('\n')
        for e in removing_elements:
            self.list_with_info.remove(e)
        self.info.setText(''.join(str_to_print))
