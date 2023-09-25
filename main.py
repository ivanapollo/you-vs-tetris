import pygame as pg
from consts import *
import graphics
import matrix

# инициализируем pygame
pg.init()

screen = pg.display.set_mode(WINDOW_SIZE)
clock = pg.time.Clock()

test = graphics.MatrixSurface()
test.m.fig = matrix.Figure(Fig.Z, Dir.UP)

while True:

    # TODO ввод от игрока
    for i in pg.event.get():
        if i.type == pg.QUIT:
            pg.quit()
            exit()
        if i.type == pg.KEYDOWN:
            if i.key == pg.K_UP:
                print(Dir.UP)
            if i.key == pg.K_RIGHT:
                print(Dir.RIGHT)
            if i.key == pg.K_DOWN:
                print(Dir.DOWN)
            if i.key == pg.K_LEFT:
                print(Dir.LEFT)
    # TODO обработка
    # TODO отрисовка

    screen.fill(GRAY)

    test.update()
    print(test.m.move_fig(Dir.DOWN))
    screen.blit(test, (0, 0))

    pg.display.flip()

    # залочили FPS
    clock.tick(3)
