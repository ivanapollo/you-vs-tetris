import pygame as pg
from consts import *
import graphics


class Game:

    def __init__(self):
        # инициализируем pygame
        pg.init()
        self.screen = pg.display.set_mode(WINDOW_SIZE)
        self.clock = pg.time.Clock()
        self.field = graphics.MatrixSurface()
        self.lines_cleared: int = 0

    def do_cycle(self) -> bool:

        for i in pg.event.get():
            if i.type == pg.QUIT:
                pg.quit()
                exit()
            if i.type == pg.KEYDOWN:
                if i.key == pg.K_UP:
                    self.field.m.rotate()
                self.field.m.move_figure(i.key)

        # если не можем сдвинуть фигуру вниз, записываем фигуру
        if not self.field.m.move_figure(pg.K_DOWN, _side=1):
            self.field.m.blit_figure()
            # если не можем сгенерировать, значит игра закончилась
            if not self.field.m.generate_new_figure():
                return False

        # если есть полные ряды, записываем в статистику
        if full_rows := self.field.m.get_full_rows():
            self.lines_cleared += len(full_rows)
            self.field.m.shrink_rows(full_rows)

        self.field.update()

        return True

    def draw(self):
        self.screen.fill(pg.Color('black'))
        self.screen.blit(self.field, (0, 0))
        pg.display.flip()
        self.clock.tick(FPS)