import itertools

import pygame as pg

from consts import *
import matrix


class MatrixSurface(pg.Surface):
    """Класс для отрисовки игрового поля"""

    def __init__(self):
        super().__init__((MATRIX_WIDTH * BLOCK_SIZE,
                          MATRIX_HEIGHT * BLOCK_SIZE))

        # экземпляр игрового поля
        self.m = matrix.Matrix(MATRIX_WIDTH, MATRIX_HEIGHT)

    def update(self):
        """Рисует ячейки"""

        # отрисовываем стакан
        for i, j in itertools.product(range(self.m.height),
                                      range(self.m.width)):
            # если ячейка в стакане не пустая, отрисовываем цветом
            # иначе фоновым
            color = BG
            if self.m.grid[i][j]:
                color = self.m.get_block_color(i, j)

            # прямоугольник для отрисовки
            _rect = (j * BLOCK_SIZE, i * BLOCK_SIZE,
                     BLOCK_SIZE, BLOCK_SIZE)

            pg.draw.rect(self, color, _rect, border_radius=BORDER_RADIUS)

        # отрисовываем фигуру
        color = self.m.p_figure.get_fig_color()
        for i, j in itertools.product(range(self.m.p_figure.height),
                                      range(self.m.p_figure.width)):
            if not (0 <= self.m.figure_top + i < MATRIX_HEIGHT
                    and 0 <= self.m.figure_left + j < MATRIX_WIDTH):
                continue

            # если ячейка пустая, не отрисовываем
            if not self.m.p_figure.grid[i][j]:
                continue

            _rect = ((self.m.figure_left + j) * BLOCK_SIZE, (self.m.figure_top + i) * BLOCK_SIZE,
                     BLOCK_SIZE, BLOCK_SIZE)

            pg.draw.rect(self, color, _rect, border_radius=BORDER_RADIUS)


