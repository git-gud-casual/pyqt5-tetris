# Импорт всего необходимого
from sys import exit, argv

from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QDialog)
from PyQt5.QtGui import QPixmap, QIcon

from source.scripts import Game, SettingsDialog, ScoreDialog
from source.ui import main_ui


# Класс начального окна
class MainWindow(QMainWindow, main_ui.Ui_MainWindow):
    # Инициализация
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('source/img/tetris_icon.png'))
        logo = QPixmap('source/img/tetris_logo.jpg')
        self.logo_pic.setPixmap(logo)
        self.message = 'Hello'
        self.setWindowTitle('Tetris')
        self.load_ui()

    def load_ui(self):
        self.settings = SettingsDialog.SettingsDialog()
        # Привяка кнопок к обработчику
        self.start_button.clicked.connect(self.start_game)
        self.settings_button.clicked.connect(self.settings_window)
        self.score_button.clicked.connect(self.score_window)
        self.exit_button.clicked.connect(self.close)

    def start_game(self):
        self.game = Game.Game(self, self.settings.music_play)
        self.game.show()
        self.hide()

    def settings_window(self):
        self.settings.exec()

    @staticmethod
    def score_window():
        score = ScoreDialog.ScoreDialog()
        score.exec()


if __name__ == '__main__':
    app = QApplication(argv)
    window = MainWindow()
    window.show()
    exit(app.exec_())
