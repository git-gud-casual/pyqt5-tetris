from typing import List, Optional
from random import choice
from dataclasses import dataclass

from .shapes import shapes_factory, Tetraminoe
from .cell import Cell


@dataclass
class ShapeWithCoord(Tetraminoe):
    x: int
    y: int

    @property
    def bottom_y(self) -> int:
        return self.y + self.height - 1

    @property
    def right_x(self) -> int:
        return self.x + self.width - 1

    def get_rotated(self) -> "ShapeWithCoord":
        rotated = super().get_rotated()
        return ShapeWithCoord(rotated.shape, self.x, self.y)


class Board(list):
    def __init__(self, width: int, height: int):
        super().__init__([[Cell.EMPTY for _ in range(width)] for _ in range(height)])

    def transfer_another_list(self, list_: List[List[Cell]], x: int, y: int):
        for i in range(len(list_)):
            for j in range(len(list_[i])):
                if self[y + i][x + j] != Cell.FROZEN:
                    self[y + i][x + j] = list_[i][j]

    def del_active_figure(self, active_fig: ShapeWithCoord):
        clear_mask = [[Cell.EMPTY] * active_fig.width for _ in range(active_fig.height)]
        self.transfer_another_list(clear_mask, active_fig.x, active_fig.y)


class Game:
    WIDTH = 10
    HEIGHT = 22
    _SHAPES = shapes_factory()

    _lines_count = 0
    _level: int
    _board: Board
    _next_shape: Optional[Tetraminoe] = None
    _active_shape: Optional[ShapeWithCoord] = None
    _game_over: bool = False

    def __init__(self):
        self._level = 1
        self._board = Board(self.WIDTH, self.HEIGHT)

    @property
    def next_shape(self) -> Tetraminoe:
        if self._next_shape is None:
            self._next_shape = choice(self._SHAPES)
        return self._next_shape

    def _drop_new_shape(self):
        x_offset = (self.WIDTH - self.next_shape.width) // 2
        self._active_shape = ShapeWithCoord(self.next_shape.shape, x_offset, 0)
        self._board.transfer_another_list(self._active_shape.shape, x_offset, 0)
        self._next_shape = None

    def next(self):
        if self._game_over:
            return

        if self._active_shape is None:
            if not (game_over := (Cell.FROZEN in self._board[0])):
                self._drop_new_shape()
            self._game_over = game_over
        elif self._can_move_down():
            self._move_down()
        else:
            self._freeze_active_figure()
            self._clear_lines()
            self._level = min(self._lines_count // 10 + 1, 9)

    def _freeze_active_figure(self):
        for y in range(self._active_shape.height):
            for x in range(self._active_shape.width):
                if self._active_shape.shape[y][x] != Cell.EMPTY:
                    self._board[y + self._active_shape.y][x + self._active_shape.x] = Cell.FROZEN
        self._active_shape = None

    def _clear_lines(self):
        full_line = [Cell.FROZEN for _ in range(self.WIDTH)]
        while full_line in self._board:
            line_index = self._board.index(full_line)
            self._board[1:line_index + 1] = self._board[0:line_index]
            self._board[0] = [Cell.EMPTY for _ in range(self.WIDTH)]
            self._lines_count += 1

    def _can_move_down(self) -> bool:
        next_y = self._active_shape.bottom_y + 1
        if next_y >= self.HEIGHT:
            return False

        for x in range(self._active_shape.width):
            if self._board[next_y][x + self._active_shape.x] == Cell.FROZEN and \
                    self._active_shape.shape[-1][x] != Cell.EMPTY:
                return False
        return True

    def _move_down(self):
        self._board.del_active_figure(self._active_shape)

        self._active_shape.y += 1
        self._board.transfer_another_list(self._active_shape.shape, self._active_shape.x,
                                          self._active_shape.y)

    def _move_on_x_by_step(self, step: int):
        if step not in (-1, 1):
            raise ValueError("step should be 1 or -1")

        next_x = self._active_shape.right_x + 1 if step == 1 else self._active_shape.x - 1
        if not (0 <= next_x < self.WIDTH):
            return

        for y in range(self._active_shape.y, self._active_shape.bottom_y + 1):
            if self._board[y][next_x] == Cell.FROZEN and self._active_shape.shape[y][-step] != Cell.EMPTY:
                return

        self._board.del_active_figure(self._active_shape)

        self._active_shape.x += step
        self._board.transfer_another_list(self._active_shape.shape, self._active_shape.x,
                                          self._active_shape.y)

    def move_right(self):
        self._move_on_x_by_step(1)

    def move_left(self):
        self._move_on_x_by_step(-1)

    def rotate(self):
        rotated = self._active_shape.get_rotated()
        if rotated.bottom_y >= self.HEIGHT or \
                rotated.right_x >= self.WIDTH:
            return

        for y in range(rotated.height):
            for x in range(rotated.width):
                if self._board[y + rotated.y][x + rotated.x] == Cell.FROZEN and \
                        rotated.shape[y][x] != Cell.EMPTY:
                    return

        self._board.del_active_figure(self._active_shape)
        self._active_shape = rotated
        self._board.transfer_another_list(rotated.shape, rotated.x, rotated.y)

    @property
    def game_over(self) -> bool:
        return self._game_over

    @property
    def score(self) -> int:
        return self._lines_count

    @property
    def level(self) -> int:
        return self._level
