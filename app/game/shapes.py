from dataclasses import dataclass
from copy import deepcopy
from typing import List

from .cell import Cell


@dataclass
class Tetraminoe:
    _shape: List[List[Cell]]

    @property
    def width(self):
        return len(self._shape[0])

    @property
    def height(self):
        return len(self._shape)

    @property
    def shape(self) -> List[List[Cell]]:
        return deepcopy(self._shape)

    def get_rotated(self) -> "Tetraminoe":
        new_shape = []
        for x in range(self.width):
            new_shape.append([])
            for y in range(self.height - 1, -1, -1):
                new_shape[-1].append(self._shape[y][x])
        return Tetraminoe(new_shape)


_shapes = (
    [[Cell.EMPTY, Cell.ACTIVE, Cell.ACTIVE],
     [Cell.ACTIVE, Cell.ACTIVE, Cell.EMPTY]],

    [[Cell.ACTIVE, Cell.ACTIVE, Cell.EMPTY],
     [Cell.EMPTY, Cell.ACTIVE, Cell.ACTIVE]],

    [[Cell.EMPTY, Cell.ACTIVE, Cell.EMPTY],
     [Cell.ACTIVE, Cell.ACTIVE, Cell.ACTIVE]],

    [[Cell.ACTIVE, Cell.EMPTY, Cell.EMPTY],
     [Cell.ACTIVE, Cell.ACTIVE, Cell.ACTIVE]],

    [[Cell.EMPTY, Cell.EMPTY, Cell.ACTIVE],
     [Cell.ACTIVE, Cell.ACTIVE, Cell.ACTIVE]],

    [[Cell.ACTIVE, Cell.ACTIVE, Cell.ACTIVE, Cell.ACTIVE]],

    [[Cell.ACTIVE, Cell.ACTIVE],
     [Cell.ACTIVE, Cell.ACTIVE]]
)


def shapes_factory() -> List[Tetraminoe]:
    shapes = []
    for shape in _shapes:
        shapes.append(Tetraminoe(shape))
    return shapes
