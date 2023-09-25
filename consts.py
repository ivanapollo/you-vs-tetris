from enum import IntEnum
from pygame import Color

WINDOW_SIZE = (800, 600)
MATRIX_WIDTH = 10
MATRIX_HEIGHT = 20
BLOCK_SIZE = 20
BORDER_RADIUS = BLOCK_SIZE // 4
MATRIX_SURF_SIZE = (MATRIX_WIDTH * BLOCK_SIZE,
                    MATRIX_HEIGHT * BLOCK_SIZE)
FPS = 30


class Dir(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


ALL_DIRS = (Dir.UP,
            Dir.RIGHT,
            Dir.DOWN,
            Dir.LEFT)


class Fig(IntEnum):
    O = 1
    T = 2
    LC = 3
    RC = 4
    Z = 5
    S = 6
    I = 7


ALL_FIGS = (Fig.O,
            Fig.T,
            Fig.LC,
            Fig.RC,
            Fig.Z,
            Fig.S,
            Fig.I)

BG = (40, 40, 40)

COLORS = (
    Color('yellow'),
    Color('purple'),
    Color('lightblue'),
    Color('orange'),
    Color('red'),
    Color('green'),
    Color('cyan'),
)