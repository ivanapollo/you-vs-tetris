import pygame as pg
from consts import *
from matrix import *


class MatrixSurface(pg.Surface):
    """Класс для отрисовки игрового поля"""

    def __init__(self):
        super().__init__(MATRIX_SURF_SIZE)
        self.matrix = Matrix(*MATRIX_SIZE)

    def update(self):
        """Рисует ячейки"""

        self.fill(GRAY)

        for i in range(self.matrix.height):
            for j in range(self.matrix.width):

                color = pg.Color('lightblue') \
                    if self.matrix.grid[i][j] \
                    else GRAY

                _rect = (j * BLOCK_SIZE,
                         i * BLOCK_SIZE,
                         BLOCK_SIZE,
                         BLOCK_SIZE)

                pg.draw.rect(self, color, _rect, border_radius=BORDER_RADIUS)
