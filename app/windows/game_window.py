from os.path import join
from typing import Optional

from PyQt5.QtWidgets import QLabel, QMainWindow
from PyQt5.QtGui import QPainter, QColor, QIcon
from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import Qt, QBasicTimer

from .game_over import GameOver
from game import Game, Cell
from game.painter import qt_paint

from config import IMAGES_DIR, MUSIC_DIR


class GameWindow(QMainWindow):
    _parent_window: QMainWindow

    _timer: QBasicTimer
    _speed: int
    _music: Optional[QSound]
    _paused: bool = False
    _painter: QPainter

    _game: Game

    def __init__(self, window: QMainWindow, music_play: bool):
        super().__init__()
        self._parent_window = window

        self.setWindowIcon(QIcon(join(IMAGES_DIR, "tetris_icon.png")))
        self.setFixedSize(Game.WIDTH * 20 + 10 * 2 + 50, (Game.HEIGHT - 2) * 20)
        self.setWindowTitle('Tetris')
        self.score_text = QLabel(self)
        self.score_text.move(205, 350)
        self.level_text = QLabel(self)
        self.level_text.move(205, 325)
        self.pause_status = QLabel(self)
        self.pause_status.move(205, 15)
        self.pause_status.setText('Pause')
        self.pause_status.hide()
        text = QLabel(self)
        text.move(208, 80)
        text.setText('Next Figure')

        self._game = Game()
        self.score_text.setText(f'Lines: {self._game.score}')
        self.level_text.setText(f'Level: {self._game.level}')

        self._speed = (10 - self._game.level) * 40
        self._timer = QBasicTimer()
        self._timer.start(self._speed, self)

        if music_play:
            self._music = QSound(join(MUSIC_DIR, "music.wav"))
            self._music.play()
            self._music.setLoops(self._music.Infinite)

    def _fast_move(self):
        if not self._paused:
            self._timer.start(0, self)

    def _pause(self):
        self._paused = not self._paused
        if self._paused:
            self.pause_status.show()
            self._timer.stop()
        else:
            self.pause_status.hide()
            self._timer.start(self.speed, self)

    def keyPressEvent(self, event):
        key_to_func = {Qt.Key_Down: self._fast_move,
                       Qt.Key_S: self._fast_move,
                       Qt.Key_Left: self._game.move_left,
                       Qt.Key_A: self._game.move_left,
                       Qt.Key_Right: self._game.move_right,
                       Qt.Key_D: self._game.move_right,
                       Qt.Key_Up: self._game.rotate,
                       Qt.Key_W: self._game.rotate,
                       Qt.Key_Space: self._pause}
        key1, key2 = event.nativeVirtualKey(), event.key()
        if func := (key_to_func.get(key1) or key_to_func.get(key2)):
            func()
            self.update()

    def paintEvent(self, event):
        self._painter = QPainter()
        self._painter.begin(self)
        qt_paint(self._game, self._painter)
        self._painter.end()

    def _game_over(self):
        self._timer.stop()
        if self._music is not None:
            self._music.stop()
        GameOver(self._game.score, self._game.level).exec()
        self.close()

    def closeEvent(self, event):
        self._parent_window.show()
        if self._music is not None:
            self._music.stop()
        self.close()

    def timerEvent(self, event):
        self._game.next()
        if self._game.game_over:
            self._game_over()
            return

        self.level_text.setText(f'Level: {self._game.level}')
        self.score_text.setText(f'Lines: {self._game.score}')
        self._speed = (10 - self._game.level) * 40
        self._timer.start(self._speed, self)

        self.update()
