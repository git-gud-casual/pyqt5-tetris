import sqlite3

from os.path import join

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog

from db_tools import DBDeleter

from .ui import settings_ui

from config import IMAGES_DIR


class SettingsDialog(QDialog, settings_ui.Ui_Settings):
    _music_play: bool = True

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setupUi(self)
        self.setWindowIcon(QIcon(join(IMAGES_DIR, "tetris_icon.png")))

        self.del_button.clicked.connect(self._db_clear)
        self.checkBox.stateChanged.connect(self._music_toggle)

    @staticmethod
    def _db_clear():
        DBDeleter().delete_all()

    def _music_toggle(self, state):
        self._music_play = state != Qt.Checked

    @property
    def music_is_on(self) -> bool:
        return self._music_play
