from consts import *
import random
import pygame.constants as pgc

class Figure:
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
        self.fig: int = fig
        # где-то поворотов надо всего два, вот и разделяю по кейсам
        self.dirs: int = len(self._figs[fig - 1])
        self.dir: int = dir % self.dirs

        self.grid: tuple = ()
        self.height: int = 0
        self.width: int = 0

        self.__update()

    def clockwise(self):
        self.dir = (self.dir + 1) % self.dirs
        self.__update()

    def counterclockwise(self):
        self.dir = (self.dir - 1) % self.dirs
        self.__update()

    def __update(self):
        self.grid = self._figs[self.fig - 1][self.dir]
        self.height = len(self.grid)
        self.width = len(self.grid[0])

    # дебаг 90 lvl
    def print(self):
        for i in range(self.height):
            print(self.grid[i])

    # def __print_figs(self):
    #     for i in range(len(self._figs)):
    #         for j in range(len(self._figs[i])):
    #             for k in range(len(self._figs[i][j])):
    #                 print(self._figs[i][j][k])


class Matrix:
    """Класс игрового поля"""

    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
        self.grid: list = [
            [0 for j in range(width)] for i in range(height)
        ]

        self.fig = None
        self.fig_left: int = 0
        self.fig_top: int = 0

        self.gen_new_fig()

    def gen_new_fig(self) -> bool:
        """True, если сгенерировали фигуру, иначе False"""

        self.fig = Figure(
            random.choice(ALL_FIGS),
            random.choice(ALL_DIRS),
        )
        self.fig_top = 0
        self.fig_left = 0
        for i in range(self.width):
            if not self.check_collision():
                return True
            self.fig_left += 1
        return False

    def check_collision(self) -> bool:
        """
        True, если падающая фигура накладывается на ячейки сетки,
        иначе False
        """

        for i in range(self.fig.height):
            for j in range(self.fig.width):
                if not (0 <= self.fig_top + i < MATRIX_HEIGHT and
                        0 <= self.fig_left + j < MATRIX_WIDTH):
                    continue
                if (self.grid[self.fig_top + i][self.fig_left + j] and
                    self.fig.grid[i][j] or
                    self.fig_top + i == MATRIX_HEIGHT):
                    return True
        return False

    def move_fig(self, dir: int, side=0) -> bool:

        dx = 0
        dy = 0
        if side and dir == pgc.K_DOWN:
            dy = 1
        if dir == pgc.K_RIGHT:
            dx = 1
        elif dir == pgc.K_LEFT:
            dx = -1

        if self.fig.fig == Fig.I:
            if not (-1 <= self.fig_left + dx <= MATRIX_WIDTH - self.fig.width and
                    0 <= self.fig_top + dy <= MATRIX_HEIGHT - self.fig.height):
                return False
        else:
            if not (0 <= self.fig_left + dx <= MATRIX_WIDTH - self.fig.width and
                    0 <= self.fig_top + dy <= MATRIX_HEIGHT - self.fig.height):
                return False

        self.fig_top += dy
        self.fig_left += dx
        if not self.check_collision():
            return True

        # if self.fig_top != MATRIX_HEIGHT - self.fig.height:
        self.fig_top -= dy
        self.fig_left -= dx
        return False

    def rotate(self):
        self.fig.clockwise()
        if self.check_collision():
            self.fig.counterclockwise()

    def blit_fig(self):
        for i in range(self.fig.height):
            for j in range(self.fig.width):
                if not (0 <= self.fig_top + i < MATRIX_HEIGHT and
                        0 <= self.fig_left + j < MATRIX_WIDTH):
                    continue
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