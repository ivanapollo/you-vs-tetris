from enum import IntEnum

WINDOW_SIZE = (800, 600)
MATRIX_SIZE = (10, 20)
BLOCK_SIZE = 25
BORDER_RADIUS = BLOCK_SIZE // 4
MATRIX_SURF_SIZE = (MATRIX_SIZE[0] * BLOCK_SIZE,
                    MATRIX_SIZE[1] * BLOCK_SIZE)
FPS = 30


class Dir(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Fig(IntEnum):
    O = 0
    T = 1
    LC = 2
    RC = 3
    Z = 4
    S = 5
    I = 6


GRAY = (40, 40, 40)
# TODO перечисление цветов?