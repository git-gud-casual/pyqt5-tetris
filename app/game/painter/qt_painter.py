from PyQt5.QtGui import QPainter, QColor

from ..game import Game
from ..cell import Cell


class PyQtGamePainter:
    GRID_COLOR = QColor(255, 255, 255)
    BLACK_COLOR = QColor(0, 0, 0)
    ACTIVE_COLOR = QColor(243, 202, 32)
    FROZEN_COLOR = QColor(128, 128, 128)
    NEXT_FIG_COLOR = QColor(255, 215, 0)

    def __call__(self, game: Game, painter: QPainter):
        self._draw_grid(painter)
        self._draw_board(game, painter)
        self._draw_next_figure(game, painter)

    def _draw_grid(self, painter: QPainter):
        painter.setBrush(self.GRID_COLOR)
        for x in range(0, Game.WIDTH * 20 + 1, 20):
            painter.drawLine(x, 0, x, Game.HEIGHT * 20)
        for y in range(0, Game.HEIGHT * 20 + 1, 20):
            painter.drawLine(0, y, Game.WIDTH * 20, y)

    @classmethod
    def _draw_board(cls, game: Game, painter: QPainter):
        for i in range(2, len(game._board)):
            for j in range(len(game._board[i])):
                if game._board[i][j] != Cell.EMPTY:
                    color = cls.ACTIVE_COLOR if game._board[i][j] == Cell.ACTIVE else cls.FROZEN_COLOR
                    cls._draw_square(painter, cls.BLACK_COLOR,
                                     20 * j, 20 * i - 40, 20)
                    cls._draw_square(painter, color,
                                     2 + 20 * j, 2 + 20 * i - 40, 16)

    @classmethod
    def _draw_next_figure(cls, game: Game, painter: QPainter):
        for string in range(len(game.next_shape.shape)):
            for block in range(len(game.next_shape.shape[string])):
                if game.next_shape.shape[string][block] == Cell.ACTIVE:
                    cls._draw_square(painter, cls.NEXT_FIG_COLOR, 212 + 14 * block, 50 + 14 * string, 14)

    @staticmethod
    def _draw_square(painter, color, x, y, size):
        painter.setBrush(color)
        painter.drawRect(x, y, size, size)
