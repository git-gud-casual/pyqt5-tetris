from os.path import join

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap, QIcon

from .ui import main_ui
from .game import Game
from .settings import SettingsDialog
from .score import ScoreDialog

from config import IMAGES_DIR


class MainWindow(QMainWindow, main_ui.Ui_MainWindow):
    _setting: SettingsDialog
    _game: Game

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowIcon(QIcon(join(IMAGES_DIR, "tetris_icon.png")))
        self.logo_pic.setPixmap(QPixmap(join(IMAGES_DIR, "tetris_logo.jpg")))
        self.setWindowTitle('Tetris')

        self._settings = SettingsDialog()

        self.start_button.clicked.connect(self._start_game)
        self.settings_button.clicked.connect(self._settings_window)
        self.score_button.clicked.connect(self._score_window)
        self.exit_button.clicked.connect(self.close)

    def _start_game(self):
        self._game = Game(self, self._settings.music_is_on)
        self._game.show()
        self.hide()

    def _settings_window(self):
        self._settings.exec()

    @staticmethod
    def _score_window():
        score = ScoreDialog()
        score.exec()
