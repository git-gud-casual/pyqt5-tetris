import sqlite3
from PyQt5.QtGui import QIcon
from source.ui import game_over_ui
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt


# Класс окна проигрыша
class GameOver(QDialog, game_over_ui.Ui_Dialog):
    def __init__(self, score, level):
        super().__init__()
        self.score, self.level = score, level
        self.setupUi(self)
        self.setWindowIcon(QIcon('source/img/tetris_icon.png'))
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle('Game Over')
        self.con = sqlite3.connect('source/data_base/score.sqlite')
        self.cur = self.con.cursor()
        self.loadUi()

    def loadUi(self):
        self.lvl_label.setText(f'Level: {self.level}')
        self.lines_label.setText(f'Lines: {self.score}')
        self.quit_button.clicked.connect(self.close)

    def closeEvent(self, event):
        if self.name_line.text() == '':
            self.name_line.setText('Player')
        elif len(self.name_line.text()) > 18:
            self.name_line.setText(self.name_line.text()[:18])
        self.cur.execute(f"""INSERT INTO score_table(name, score) 
                                VALUES('{self.name_line.text()}', {self.score})""")
        self.con.commit()
        self.con.close()
        self.close()
