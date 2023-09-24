import pygame as pg
from consts import *

# инициализируем pygame
pg.init()

screen = pg.display.set_mode(WINDOW_SIZE)
clock = pg.time.Clock()

while True:

    # TODO ввод от игрока
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

    # TODO обработка
    # TODO отрисовка

    # pg.display.flip()

    # залочили FPS
    clock.tick(FPS)
