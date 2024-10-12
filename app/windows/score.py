import sqlite3

from os.path import join

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from db_tools import DBViewer

from .ui import scores_ui

from config import IMAGES_DIR


class ScoreDialog(QDialog, scores_ui.Ui_ScoreDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setupUi(self)
        self.setWindowIcon(QIcon(join(IMAGES_DIR, "tetris_icon.png")))
        self._load_scores()

    def _load_scores(self):
        strs = [self.one, self.two, self.thre, self.four, self.five]
        for i, val in enumerate(DBViewer().get_ordered_scores()):
            name, score = val
            strs[i].setText(f"{i + 1}. {name} {score}")
