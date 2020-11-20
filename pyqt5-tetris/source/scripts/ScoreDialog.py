from PyQt5.QtWidgets import QDialog
from source.ui import scores_ui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import sqlite3


# Класс для отображения очков
class ScoreDialog(QDialog, scores_ui.Ui_ScoreDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setupUi(self)
        self.setWindowIcon(QIcon('source/img/tetris_icon.png'))
        self.loadUi()

    def loadUi(self):
        con = sqlite3.connect('source/data_base/score.sqlite')
        cur = con.cursor()
        values = []
        for _ in range(5):
            values.append(cur.execute('''SELECT * FROM score_table
WHERE score = (SELECT MAX(score) FROM score_table)''').fetchall())
            cur.execute('''DELETE from score_table 
WHERE score = (SELECT MAX(score) FROM score_table)''')
        con.close()
        for i in range(len(values)):
            for j in values[i]:
                name, score = j
                if self.one.text() == '':
                    self.one.setText(f'1. {name} {score}')
                elif self.two.text() == '':
                    self.two.setText(f'2. {name} {score}')
                elif self.thre.text() == '':
                    self.thre.setText(f'3. {name} {score}')
                elif self.four.text() == '':
                    self.four.setText(f'4. {name} {score}')
                elif self.five.text() == '':
                    self.five.setText(f'5. {name} {score}')
