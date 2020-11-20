# Классы фигур
class Tetraminoe:
    shape = []

    def get_width(self):
        return len(self.shape[0])

    def get_height(self):
        return len(self.shape)


class ShapeSquare(Tetraminoe):
    shape = [[1, 1],
             [1, 1]]


class ShapeLine(Tetraminoe):
    shape = [[1, 1, 1, 1]]


class ShapeG(Tetraminoe):
    shape = [[0, 0, 1],
             [1, 1, 1]]


class ShapeReverseG(Tetraminoe):
    shape = [[1, 0, 0],
             [1, 1, 1]]


class ShapeT(Tetraminoe):
    shape = [[0, 1, 0],
             [1, 1, 1]]


class ShapeZ(Tetraminoe):
    shape = [[1, 1, 0],
             [0, 1, 1]]


class ShapeReverseZ(Tetraminoe):
    shape = [[0, 1, 1],
             [1, 1, 0]]
