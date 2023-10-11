from consts import *
import random
import pygame.constants as pgc
import itertools


class Figure:
    """Класс фигуры"""

    # кортеж со всеми возможными фигурами и поворотами
    _figs = (
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

    def __init__(self, fig: int, dir: int):
        # тип фигуры
        self.fig: int = fig

        # где-то поворотов надо всего два, вот и разделяю по кейсам
        self.dirs: int = len(self._figs[fig - 1])

        # направление фигуры
        self.dir: int = dir % self.dirs

        # матрица фигуры
        self.grid: tuple = ()

        # высота, ширина
        self.height: int = 0
        self.width: int = 0

        self.__update()

    def clockwise(self):
        self.dir = (self.dir + 1) % self.dirs
        self.__update()

    def counterclockwise(self):
        self.dir = (self.dir - 1) % self.dirs
        self.__update()

    def get_fig_color(self):
        return COLORS[self.fig - 1]

    # обновляем матрицу фигуры, её длину и высоту
    def __update(self):
        self.grid = self._figs[self.fig - 1][self.dir]
        self.height = len(self.grid)
        self.width = len(self.grid[0])


class Matrix:
    """Класс игрового поля"""

    def __init__(self, width: int, height: int):

        # ширина, высота стакана
        self.width: int = width
        self.height: int = height

        # матрица стакана
        self.grid: list = [
            [0 for j in range(width)] for i in range(height)
        ]

        # падающая фигура
        self.fig = None

        # координаты левого верхнего угла фигуры
        self.fig_left: int = 0
        self.fig_top: int = 0

        self.gen_new_fig()

    def gen_new_fig(self) -> bool:
        """True, если сгенерировали фигуру, иначе False"""

        # рандомно выбрали фигуру
        self.fig = Figure(
            random.choice(ALL_FIGS),
            random.choice(ALL_DIRS),
        )
        self.fig_top = 0
        self.fig_left = 0

        # смотрим, где есть пустое место, чтобы поставить фигуру
        for i in range(self.width):
            # если ни с чем не пересекаемся, ставим фигуру
            if not self.check_collision():
                return True
            # если пересеклись, пробуем поставить её в соседнюю справа ячейку
            self.fig_left += 1

        # если нигде не получилось, значит капут
        return False

    def check_collision(self) -> bool:
        """True, если падающая фигура накладывается на ячейки сетки,
        иначе False"""

        # записал вложенный цикл через декартово произведение
        for i, j in itertools.product(range(self.fig.height),
                                      range(self.fig.width)):
            # если ячейка не в пределах стакана, не проверяем
            if not (0 <= self.fig_top + i < MATRIX_HEIGHT
                    and 0 <= self.fig_left + j < MATRIX_WIDTH):
                continue

            # проверяем:
            # 1) ячейка фигуры наложилась на ячейку в стакане
            # 2) ячейка фигуры наткнулась на низ стакана
            if (self.grid[self.fig_top + i][self.fig_left + j]
                    and self.fig.grid[i][j]
                    or self.fig_top + i == MATRIX_HEIGHT):
                return True

        return False

    def move_fig(self, dir: int, side=0) -> bool:
        """True, если фигура переместилась, иначе False"""

        dx = 0
        dy = 0
        if side and dir == pgc.K_DOWN:
            dy = 1
        if dir == pgc.K_RIGHT:
            dx = 1
        elif dir == pgc.K_LEFT:
            dx = -1

        # -1 потому что в вертикальной палке первый столбец пустой, поэтому сместиться влево ещё можно
        # у нас слева есть пустой ряд, но по факту-то сместить её всё ещё можно
        l_bound = -1 if self.fig.fig == Fig.I else 0

        # проверяем, чтобы фигура была в пределах стакана, иначе не двигаем
        if not (l_bound <= self.fig_left + dx <= MATRIX_WIDTH - self.fig.width
                and 0 <= self.fig_top + dy <= MATRIX_HEIGHT - self.fig.height):
            return False

        # пробуем сместиться
        self.fig_top += dy
        self.fig_left += dx

        # если ни на что не наткнулись, значит сместились
        if not self.check_collision():
            return True

        # если наткнулись, значит сместимся обратно
        self.fig_top -= dy
        self.fig_left -= dx

        return False

    def rotate(self):
        self.fig.clockwise()
        if self.check_collision():
            self.fig.counterclockwise()

    def blit_fig(self):

        for i, j in itertools.product(range(self.fig.height),
                                      range(self.fig.width)):
            # если ячейка вне стакана, не рисуем
            if not (0 <= self.fig_top + i < MATRIX_HEIGHT and
                    0 <= self.fig_left + j < MATRIX_WIDTH):
                continue

            # если ячейка фигуры не пустая, то записываем в матрицу
            if self.fig.grid[i][j]:
                self.grid[self.fig_top + i][self.fig_left + j] = self.fig.fig

    def full_rows(self) -> tuple:
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

    def print_matrix(self):
        for i in range(self.height):
            print(self.grid[i])

    def get_block_color(self, i: int, j: int) -> int:
        return COLORS[self.grid[i][j] - 1]
