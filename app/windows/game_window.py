from random import choice

from os.path import join

from PyQt5.QtWidgets import QLabel, QMainWindow
from PyQt5.QtGui import QPainter, QColor, QIcon
from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import Qt, QBasicTimer

from .game_over import GameOver
from game import Game, Cell

from config import IMAGES_DIR, MUSIC_DIR


class GameWindow(QMainWindow):
    _game: Game

    def __init__(self, window, music_play):
        super().__init__()
        self.window = window
        # Значения окна
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
        # Инициализация очков
        self.score_text.setText(f'Lines: {self._game.score}      ')
        # Уровни
        self.speed = (10 - self._game.level) * 40
        self.level_text.setText(f'Level: {self._game.level}')
        # Для проверки в дальнейшем
        self.paused = False
        if music_play:
            self.music = QSound(join(MUSIC_DIR, "music.wav"))
            self.music.play()
            self.music.setLoops(self.music.Infinite)
        self.music_play = music_play
        self.start()

    # Старт
    def start(self):
        self.timer = QBasicTimer()
        self.timer.start(self.speed, self)

    def timerEvent(self, event):
        self._game.next()
        if self._game.game_over:
            self.game_over()

        self.level_text.setText(f'Level: {self._game.level}')
        self.speed = (10 - self._game.level) * 40
        self.timer.start(self.speed, self)
        self.score_text.setText(f'Lines: {self._game.score}')
        self.update()

    # Мгновенное падение
    def fast_move(self):
        if not self.paused:
            self.timer.start(0, self)

    # Пауза
    def pause(self):
        self.paused = not self.paused
        if self.paused:
            self.pause_status.show()
            self.timer.stop()
        else:
            self.pause_status.hide()
            self.timer.start(self.speed, self)

    # Отрисовщик
    def paintEvent(self, event):
        self.painter = QPainter()
        self.painter.begin(self)
        self.draw_grid(self.painter, QColor(255, 255, 255))
        self.draw_next_figure(self.painter)
        self.draw_board(self.painter)
        self.painter.end()

    # Метод, отрисовывающий список board
    def draw_board(self, painter):
        for i in range(2, len(self._game._board)):
            for j in range(len(self._game._board[i])):
                if self._game._board[i][j] != Cell.EMPTY:
                    color1 = QColor(255, 255, 255)
                    color2 = QColor(255, 255, 255)
                    color1.setNamedColor('#000000')
                    if self._game._board[i][j] == Cell.ACTIVE:
                        color2.setNamedColor('#f3ca20')
                    elif self._game._board[i][j] == Cell.FROZEN:
                        color2.setNamedColor('#808080')
                    self.draw_square(painter, color1,
                                     20 * j, 20 * i - 40, 20)
                    self.draw_square(painter, color2,
                                     2 + 20 * j, 2 + 20 * i - 40, 16)

    # Метод рисования квадрата
    @staticmethod
    def draw_square(painter, color, x, y, size):
        painter.setBrush(color)
        painter.drawRect(x, y, size, size)

    # Метод рисования сетки
    def draw_grid(self, painter, color):
        painter.setBrush(color)
        for x in range(0, Game.WIDTH * 20 + 1, 20):
            painter.drawLine(x, 0, x, Game.HEIGHT * 20)
        for y in range(0, Game.HEIGHT * 20 + 1, 20):
            painter.drawLine(0, y, Game.WIDTH * 20, y)

    # Метод отрисовки следующей фигуры
    def draw_next_figure(self, painter):
        for string in range(len(self._game.next_shape.shape)):
            for block in range(len(self._game.next_shape.shape[string])):
                if self._game.next_shape.shape[string][block] == Cell.ACTIVE:
                    self.draw_square(painter, QColor(255, 215, 0), 212 + 14 * block, 50 + 14 * string, 14)

    # Проигрыш
    def game_over(self):
        self.timer.stop()
        if self.music_play:
            self.music.stop()
        GameOver(self._game.score, self._game.level).exec()
        self.close()

    def closeEvent(self, event):
        self.window.show()
        if self.music_play:
            self.music.stop()
        self.close()

    def keyPressEvent(self, event):
        key_to_func = {Qt.Key_Down: self.fast_move,
                       Qt.Key_S: self.fast_move,
                       Qt.Key_Left: self._game.move_left,
                       Qt.Key_A: self._game.move_left,
                       Qt.Key_Right: self._game.move_right,
                       Qt.Key_D: self._game.move_right,
                       Qt.Key_Up: self._game.rotate,
                       Qt.Key_W: self._game.rotate,
                       Qt.Key_Space: self.pause}
        key1, key2 = event.nativeVirtualKey(), event.key()
        if func := (key_to_func.get(key1) or key_to_func.get(key2)):
            func()
            self.update()
