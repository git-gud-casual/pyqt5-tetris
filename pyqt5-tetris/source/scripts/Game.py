# PyQt5
from PyQt5.QtWidgets import QLabel, QMainWindow
from PyQt5.QtGui import QPainter, QColor, QIcon
from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import Qt, QBasicTimer
# Фигуры
from source.scripts import Tetraminoe, GameOver
# random
from random import choice


# Класс игрового окна
class Game(QMainWindow):
    width = 10
    height = 22
    shapes = [Tetraminoe.ShapeG, Tetraminoe.ShapeLine,
              Tetraminoe.ShapeReverseG, Tetraminoe.ShapeSquare,
              Tetraminoe.ShapeT, Tetraminoe.ShapeZ,
              Tetraminoe.ShapeReverseZ]

    # window нужна для того, чтобы потом открыть меню
    def __init__(self, window, music_play):
        super().__init__()
        self.window = window
        # Значения окна
        self.setWindowIcon(QIcon('source/img/tetris_icon.png'))
        self.setFixedSize(self.width * 20 + 10 * 2 + 50, (self.height - 2) * 20)
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
        # Инициализация очков
        self.score = 0
        self.score_text.setText(f'Lines: {self.score}      ')
        # Уровни
        self.level = 1
        self.speed = (10 - self.level) * 40
        self.level_text.setText(f'Level: {self.level}')
        # Для проверки в дальнейшем
        self.full_string = [2 for _ in range(self.width)]
        self.paused = False
        if music_play:
            self.music = QSound('source/music/music.wav')
            self.music.play()
            self.music.setLoops(self.music.Infinite)
        self.music_play = music_play
        self.start()

    # Старт
    def start(self):
        self.next_shape = choice(self.shapes)()
        # Игровое поле в виде списка
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.timer = QBasicTimer()
        self.add_new_shape()
        self.timer.start(self.speed, self)

    def timerEvent(self, event):
        if 2 in self.board[1]:
            self.game_over()
        elif self.new_shape:
            self.move_down()
        else:
            self.clear_lines()
            self.add_new_shape()

    # Куски кода отвечающие за перемещение фигур.
    # Падение
    def move_down(self):
        break_flag = False
        for y in range(self.bottomY, self.topY - 1, -1):
            for x in range(self.leftX, self.rightX + 1):
                if y >= 21 or self.board[y + 1][x] == 2 and \
                        self.board[y][x] == 1 or \
                        self.board[self.topY + 1][x] == 2 and \
                        self.board[self.topY][x] == 1 or \
                        self.topY + 2 <= 21 and \
                        self.board[self.topY + 2][x] == 2 and \
                        self.board[self.topY + 1][x] == 1:
                    break_flag = True
                    # Если убрать, то мгновенное падение будет работать, но не так как надо
                    self.timer.start(self.speed, self)
                    self.new_shape = False
                    break
            if break_flag:
                for i in range(self.bottomY, self.topY - 1, -1):
                    for j in range(self.leftX, self.rightX + 1):
                        if self.board[i][j] == 1:
                            self.board[i][j] = 2
                break
            for x in range(self.leftX, self.rightX + 1):
                if self.board[y][x] == 1:
                    self.board[y + 1][x] = self.board[y][x]
                    self.board[y][x] = 0
        self.bottomY += 1
        self.topY += 1
        self.update()

    # Движение влево
    def move_left(self):
        if self.leftX > 0 and not self.paused:
            _break = False
            for y in range(self.topY, self.bottomY + 1):
                for x in range(self.leftX, self.rightX + 1):
                    if not self.new_shape or x > 0 and self.board[y][x - 1] == 2 and \
                            self.board[y][x] == 1:
                        _break = True
                        break
                if _break:
                    break

            if not _break:
                for y in range(self.topY, self.bottomY + 1):
                    for x in range(self.leftX, self.rightX + 1):
                        if x > 0 and self.board[y][x - 1] == 0 and self.board[y][x] == 1:
                            self.board[y][x - 1] = self.board[y][x]
                            self.board[y][x] = 0
                self.leftX -= 1
                self.rightX -= 1
                self.update()

    # Движение вправо
    def move_right(self):
        if self.rightX < self.width - 1 and not self.paused:
            _break = False
            for y in range(self.topY, self.bottomY + 1):
                for x in range(self.rightX, self.leftX - 1, -1):
                    if not self.new_shape or self.board[y][x + 1] == 2 and \
                            self.board[y][x] == 1:
                        _break = True
                        break
                if _break:
                    break

            if not _break:
                for y in range(self.topY, self.bottomY + 1):
                    for x in range(self.rightX, self.leftX - 1, -1):
                        if self.board[y][x + 1] == 0 and self.board[y][x] == 1:
                            self.board[y][x + 1] = self.board[y][x]
                            self.board[y][x] = 0
                self.leftX += 1
                self.rightX += 1
                self.update()

    # Поворот
    def rotate(self):
        if self.new_shape and not self.paused:
            rotated_shape = []
            can_rotate = True
            for x in range(self.rightX, self.leftX - 1, -1):
                rotated_shape.append([])
                for y in range(self.topY, self.bottomY + 1):
                    if self.board[y][x] == 2:
                        rotated_shape[-1].append(0)
                    else:
                        rotated_shape[-1].append(self.board[y][x])
            for y in range(len(rotated_shape)):
                for x in range(len(rotated_shape[y])):
                    if (self.topY + y > 21 or self.leftX + x > 9) or \
                            self.board[self.topY + y][self.leftX + x] == 2 and \
                            rotated_shape[y][x] != 0:
                        can_rotate = False
            if can_rotate:
                for y in range(self.topY, self.bottomY + 1):
                    for x in range(self.leftX, self.rightX + 1):
                        if self.board[y][x] == 1:
                            self.board[y][x] = 0
                for y in range(len(rotated_shape)):
                    for x in range(len(rotated_shape[y])):
                        if rotated_shape[y][x] == 1:
                            self.board[self.topY + y][self.leftX + x] = rotated_shape[y][x]
                self.bottomY = self.topY + len(rotated_shape) - 1
                self.rightX = self.leftX + len(rotated_shape[-1]) - 1
                self.update()

    # Мгновенное падение
    def fast_move(self):
        if not self.paused:
            self.timer.start(0, self)
    # Конец куска кода с методами перемещения фигур

    # Добавление новой фигуры на экран
    def add_new_shape(self):
        # Определяем фигуру
        self.active_shape = self.next_shape
        self.next_shape = choice(self.shapes)()
        # Добавляем ее на поле
        for i in range(self.active_shape.get_height()):
            for j in range(self.active_shape.get_width()):
                self.board[i][4 + j] = self.active_shape.shape[i][j]
        # Координаты фигуры
        self.topY, self.bottomY = 0, self.active_shape.get_height() - 1
        self.rightX, self.leftX = self.active_shape.get_width() + 3, 4
        self.new_shape = True

    # Очищение заполненных линий, начисление очков, уровней
    def clear_lines(self):
        while self.full_string in self.board:
            string = self.board.index(self.full_string)
            self.board[1:string + 1] = self.board[0:string]
            self.board[0] = [0 for _ in range(self.width)]
            self.score += 1
            if self.level < 9 and self.score % 10 == 0:
                self.level += 1
                self.level_text.setText(f'Level: {self.level}')
                self.speed = (10 - self.level) * 40
                self.timer.start(self.speed, self)
            self.score_text.setText(f'Lines: {self.score}')

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
        for i in range(2, len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] != 0:
                    color1 = QColor(255, 255, 255)
                    color2 = QColor(255, 255, 255)
                    color1.setNamedColor('#000000')
                    if self.board[i][j] == 1:
                        color2.setNamedColor('#f3ca20')
                    elif self.board[i][j] == 2:
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
        for x in range(0, self.width * 20 + 1, 20):
            painter.drawLine(x, 0, x, self.height * 20)
        for y in range(0, self.height * 20 + 1, 20):
            painter.drawLine(0, y, self.width * 20, y)

    # Метод отрисовки следующей фигуры
    def draw_next_figure(self, painter):
        for string in range(len(self.next_shape.shape)):
            for block in range(len(self.next_shape.shape[string])):
                if self.next_shape.shape[string][block] == 1:
                    self.draw_square(painter, QColor(255, 215, 0), 212 + 14 * block, 50 + 14 * string, 14)

    # Проигрыш
    def game_over(self):
        self.timer.stop()
        if self.music_play:
            self.music.stop()
        game_over_dialogue = GameOver.GameOver(self.score, self.level)
        game_over_dialogue.exec()
        self.close()

    # Что делать при закрытии программы
    def closeEvent(self, event):
        self.window.show()
        if self.music_play:
            self.music.stop()
        self.close()

    # Обработчик нажатий клавиш
    def keyPressEvent(self, event):
        key1 = event.nativeVirtualKey()
        key = event.key()

        if key == Qt.Key_Down or key1 == Qt.Key_S:
            self.fast_move()
        elif key == Qt.Key_Left or key1 == Qt.Key_A:
            self.move_left()
        elif key == Qt.Key_Right or key1 == Qt.Key_D:
            self.move_right()
        elif key == Qt.Key_Up or key1 == Qt.Key_W:
            self.rotate()
        elif key == Qt.Key_Space:
            self.pause()
