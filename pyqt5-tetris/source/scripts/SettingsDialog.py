from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog
from source.ui import settings_ui
import sqlite3


# Класс окна для настроек
class SettingsDialog(QDialog, settings_ui.Ui_Settings):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setupUi(self)
        self.setWindowIcon(QIcon('source/img/tetris_icon.png'))
        self.loadUi()

    def loadUi(self):
        self.music_play = True
        self.del_button.clicked.connect(self.db_clear)
        self.checkBox.stateChanged.connect(self.music_toggle)

    @staticmethod
    def db_clear():
        con = sqlite3.connect('source/data_base/score.sqlite')
        cur = con.cursor()
        cur.execute('''DELETE FROM score_table''')
        con.commit()
        con.close()

    def music_toggle(self, state):
        if state == Qt.Checked:
            self.music_play = False
        else:
            self.music_play = True
