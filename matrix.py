import itertools
import random

import pygame.constants as pgc

from consts import *


class Figure:
    """Класс фигуры"""

    # кортеж со всеми возможными фигурами и поворотами
    _figures = (
        # О
        (
            (
                (1, 1),
                (1, 1),
            ),
            (
                (1, 1),
                (1, 1),
            )
        ),
        # Т
        (
            (
                (0, 1, 0),
                (1, 1, 1),
            ),
            (
                (1, 0),
                (1, 1),
                (1, 0),
            ),
            (
                (1, 1, 1),
                (0, 1, 0),
            ),
            (
                (0, 1),
                (1, 1),
                (0, 1),
            ),
        ),
        # Г
        (
            (
                (1, 1),
                (1, 0),
                (1, 0),
            ),
            (
                (1, 1, 1),
                (0, 0, 1),
            ),
            (
                (0, 1),
                (0, 1),
                (1, 1),
            ),
            (
                (1, 0, 0),
                (1, 1, 1),
            ),
        ),
        # обратная Г
        (
            (
                (1, 1),
                (0, 1),
                (0, 1),
            ),
            (
                (0, 0, 1),
                (1, 1, 1),
            ),
            (
                (1, 0),
                (1, 0),
                (1, 1),
            ),
            (
                (1, 1, 1),
                (1, 0, 0),
            ),
        ),
        # Z
        (
            (
                (0, 1),
                (1, 1),
                (1, 0),
            ),
            (
                (1, 1, 0),
                (0, 1, 1),
            ),
        ),
        # S
        (
            (
                (1, 0),
                (1, 1),
                (0, 1),
            ),
            (
                (0, 1, 1),
                (1, 1, 0),
            ),
        ),
        # I
        (
            (
                (0, 1),
                (0, 1),
                (0, 1),
                (0, 1),
            ),
            (
                (1, 1, 1, 1),
            ),
        )
    )

    def __init__(self, _type: int, _orientation: int):
        # тип фигуры
        self.type: int = _type

        # где-то поворотов надо всего два, вот и разделяю по кейсам
        self.orients: int = len(self._figures[_type - 1])

        # направление фигуры
        self.orient: int = _orientation % self.orients

        # матрица фигуры
        self.grid: tuple = ()

        # высота, ширина
        self.height: int = 0
        self.width: int = 0

        self.__update()

    def rotate(self, _orient: str):

        if _orient == 'clock':
            _d_theta = 1
        if _orient == 'counter':
            _d_theta = -1

        self.orient = (self.orient + _d_theta) % self.orients
        self.__update()

    def get_fig_color(self):
        return COLORS[self.type - 1]

    # обновляем матрицу фигуры, её длину и высоту
    def __update(self):
        self.grid = self._figures[self.type - 1][self.orient]
        self.height = len(self.grid)
        self.width = len(self.grid[0])


class Matrix:
    """Класс игрового поля"""

    def __init__(self, _width: int, _height: int):

        # ширина, высота стакана
        self.width: int = _width
        self.height: int = _height

        # матрица стакана
        self.grid: list = [
            [0 for j in range(_width)] for i in range(_height)
        ]

        # падающая фигура
        self.p_figure = None

        # координаты левого верхнего угла фигуры
        self.figure_left: int = 0
        self.figure_top: int = 0

        self.generate_new_figure()

    def generate_new_figure(self) -> bool:
        """True, если сгенерировали фигуру, иначе False"""

        # рандомно выбрали фигуру
        self.p_figure = Figure(
            random.choice(ALL_FIGS),
            random.choice(ALL_DIRS),
        )
        self.figure_top = 0
        self.figure_left = 0

        # смотрим, где есть пустое место, чтобы поставить фигуру
        for i in range(self.width):
            # если ни с чем не пересекаемся, ставим фигуру
            if not self.check_collision():
                return True
            # если пересеклись, пробуем поставить её в соседнюю справа ячейку
            self.figure_left += 1

        # если нигде не получилось, значит капут
        return False

    def check_collision(self) -> bool:
        """True, если падающая фигура накладывается на ячейки сетки,
        иначе False"""

        # записал вложенный цикл через декартово произведение
        for i, j in itertools.product(range(self.p_figure.height),
                                      range(self.p_figure.width)):
            # если ячейка не в пределах стакана, не проверяем
            if not (0 <= self.figure_top + i < MATRIX_HEIGHT
                    and 0 <= self.figure_left + j < MATRIX_WIDTH):
                continue

            # проверяем:
            # 1) ячейка фигуры наложилась на ячейку в стакане
            # 2) ячейка фигуры наткнулась на низ стакана
            if (self.grid[self.figure_top + i][self.figure_left + j]
                    and self.p_figure.grid[i][j]
                    or self.figure_top + i == MATRIX_HEIGHT):
                return True

        return False

    def move_figure(self, _direction: int, _side=0) -> bool:
        """True, если фигура переместилась, иначе False"""

        dx = 0
        dy = 0
        if _side and _direction == pgc.K_DOWN:
            dy = 1
        if _direction == pgc.K_RIGHT:
            dx = 1
        elif _direction == pgc.K_LEFT:
            dx = -1

        # -1 потому что в вертикальной палке первый столбец пустой,
        # поэтому сместиться влево ещё можно
        # у нас слева есть пустой ряд, но по факту-то сместить её всё ещё можно
        _l_bound = 0
        if (self.p_figure.type == Fig.I
                and self.p_figure.orient == Dir.UP):
            _l_bound = -1

        # проверяем, чтобы фигура была в пределах стакана, иначе не двигаем
        if not (_l_bound <= self.figure_left + dx <= MATRIX_WIDTH - self.p_figure.width
                and 0 <= self.figure_top + dy <= MATRIX_HEIGHT - self.p_figure.height):
            return False

        # пробуем сместиться
        self.figure_top += dy
        self.figure_left += dx

        # если ни на что не наткнулись, значит сместились
        if not self.check_collision():
            return True

        # если наткнулись, значит сместимся обратно
        self.figure_top -= dy
        self.figure_left -= dx

        return False

    def rotate(self) -> bool:

        self.p_figure.rotate('clock')
        if self.check_collision():
            self.p_figure.rotate('counter')
            return False
        return True

    def blit_figure(self) -> None:
        """Записывает пользовательскую фигуру в матрицу стакана"""

        for i, j in itertools.product(range(self.p_figure.height),
                                      range(self.p_figure.width)):
            # если ячейка вне стакана, не рисуем
            if not (0 <= self.figure_top + i < MATRIX_HEIGHT and
                    0 <= self.figure_left + j < MATRIX_WIDTH):
                continue
            # если ячейка фигуры не пустая, то записываем в матрицу
            if self.p_figure.grid[i][j]:
                self.grid[self.figure_top + i][self.figure_left + j] = self.p_figure.type

    def get_full_rows(self) -> tuple:
        """Возвращает кортеж из номеров заполненных рядов"""

        full_rows: list = []
        for row in range(self.height):
            # добавили номер ряда если он полный
            full_rows.append(row) if all(self.grid[row]) else 0
        return tuple(full_rows)

    def shrink_rows(self, rows_to_shrink: tuple) -> None:
        """Убирает указанные ряды и дополняет поле пустыми рядами"""

        for row in rows_to_shrink:
            self.grid.pop(-(self.height - row))
            self.grid.insert(0, [0] * self.width)

    def get_block_color(self, i: int, j: int) -> int:
        return COLORS[self.grid[i][j] - 1]
