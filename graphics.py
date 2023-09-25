import pygame as pg
from consts import *
import matrix


class MatrixSurface(pg.Surface):
    """Класс для отрисовки игрового поля"""

    def __init__(self):
        super().__init__(MATRIX_SURF_SIZE)
        self.m = matrix.Matrix(MATRIX_WIDTH,
                               MATRIX_HEIGHT)

    def update(self):
        """Рисует ячейки"""

        self.fill(BG)

        for i in range(self.m.height):
            for j in range(self.m.width):

                color = COLORS[self.m.grid[i][j] - 1] \
                    if self.m.grid[i][j] \
                    else BG

                _rect = (j * BLOCK_SIZE,
                         i * BLOCK_SIZE,
                         BLOCK_SIZE,
                         BLOCK_SIZE)

                pg.draw.rect(self, color, _rect, border_radius=BORDER_RADIUS)

        for i in range(self.m.fig.height):
            for j in range(self.m.fig.width):
                if not (0 <= self.m.fig_top + i < MATRIX_HEIGHT and
                        0 <= self.m.fig_left + j < MATRIX_WIDTH):
                    continue

                if self.m.fig.grid[i][j]:
                    color = COLORS[self.m.fig.fig - 1]
                    _rect = ((self.m.fig_left + j) * BLOCK_SIZE,
                             (self.m.fig_top + i) * BLOCK_SIZE,
                             BLOCK_SIZE,
                             BLOCK_SIZE)

                    pg.draw.rect(self, color, _rect, border_radius=BORDER_RADIUS)


