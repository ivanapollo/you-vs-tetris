import pygame as pg
from consts import *
import graphics

# инициализируем pygame
pg.init()

screen = pg.display.set_mode(WINDOW_SIZE)
clock = pg.time.Clock()

playfield = graphics.MatrixSurface()

while True:
    screen.fill(pg.Color('black'))

    playfield.update()

    for i in pg.event.get():
        if i.type == pg.QUIT:
            pg.quit()
            exit()
        if i.type == pg.KEYDOWN:
            if i.key == pg.K_UP:
                playfield.m.rotate()
            playfield.m.move_fig(i.key)

    if not playfield.m.move_fig(pg.K_DOWN, side=1):
        playfield.m.blit_fig()
        if not playfield.m.gen_new_fig():
            break

    playfield.m.shrink_rows(playfield.m.full_rows())

    screen.blit(playfield, (0, 0))

    pg.display.flip()

    # залочили FPS
    clock.tick(FPS // 4)
