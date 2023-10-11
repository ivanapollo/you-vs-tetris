import pygame as pg
from consts import *
import matrix


class MatrixSurface(pg.Surface):
    """Класс для отрисовки игрового поля"""

    def __init__(self):
        super().__init__((MATRIX_WIDTH * BLOCK_SIZE,
                          MATRIX_HEIGHT * BLOCK_SIZE))
        self.m = matrix.Matrix(MATRIX_WIDTH, MATRIX_HEIGHT)

    def update(self):
        """Рисует ячейки"""

        # отрисовываем стакан
        for i in range(self.m.height):
            for j in range(self.m.width):

                # если ячейка в стакане не пустая, отрисовываем цветом
                # иначе фоновым
                color = self.m.get_block_color(i, j) \
                    if self.m.grid[i][j] \
                    else BG

                # прямоугольник для отрисовки
                _rect = (j * BLOCK_SIZE,
                         i * BLOCK_SIZE,
                         BLOCK_SIZE,
                         BLOCK_SIZE)

                pg.draw.rect(self, color, _rect, border_radius=BORDER_RADIUS)

        # отрисовываем фигуру
        for i in range(self.m.fig.height):
            for j in range(self.m.fig.width):
                if not (0 <= self.m.fig_top + i < MATRIX_HEIGHT and
                        0 <= self.m.fig_left + j < MATRIX_WIDTH):
                    continue

                # если ячейка пустая, не отрисовываем
                if not self.m.fig.grid[i][j]:
                    continue

                # отрисовываем фигуру её цветом
                color = self.m.fig.get_fig_color()

                _rect = ((self.m.fig_left + j) * BLOCK_SIZE,
                         (self.m.fig_top + i) * BLOCK_SIZE,
                         BLOCK_SIZE,
                         BLOCK_SIZE)

                pg.draw.rect(self, color, _rect, border_radius=BORDER_RADIUS)


