from os.path import join

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt

from db_tools import DBInserter

from .ui import game_over_ui

from config import IMAGES_DIR


# Класс окна проигрыша
class GameOver(QDialog, game_over_ui.Ui_Dialog):
    _score: int
    _level: int

    def __init__(self, score, level):
        super().__init__()
        self._score, self._level = score, level
        self.setupUi(self)
        self.setWindowIcon(QIcon(join(IMAGES_DIR, "tetris_icon.png")))
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        self.setWindowTitle('Game Over')
        self.lvl_label.setText(f'Level: {self._level}')
        self.lines_label.setText(f'Lines: {self._score}')

        self.quit_button.clicked.connect(self.close)

    def closeEvent(self, event):
        name = self.name_line.text() or "Player"
        self.name_line.setText(name)
        DBInserter().add_score(name, self._score)
        self.close()
