from consts import *

# def print_matrix() -> None:
#     for i in range(m.height):
#         print(*m.grid[i], sep='')


class Figure:

    # кортеж со всеми возможными фигурами и поворотами
    _figs = (
        # О
        (
            (
                (1, 1),
                (1, 1),
            ),
            (
                (1, 1),
                (1, 1),
            )
        ),
        # Т
        (
            (
                (0, 1, 0),
                (1, 1, 1),
            ),
            (
                (1, 0),
                (1, 1),
                (1, 0),
            ),
            (
                (1, 1, 1),
                (0, 1, 0),
            ),
            (
                (0, 1),
                (1, 1),
                (0, 1),
            ),
        ),
        # Г
        (
            (
                (1, 1),
                (1, 0),
                (1, 0),
            ),
            (
                (1, 1, 1),
                (0, 0, 1),
            ),
            (
                (0, 1),
                (0, 1),
                (1, 1),
            ),
            (
                (1, 0, 0),
                (1, 1, 1),
            ),
        ),
        # обратная Г
        (
            (
                (1, 1),
                (0, 1),
                (0, 1),
            ),
            (
                (0, 0, 1),
                (1, 1, 1),
            ),
            (
                (1, 0),
                (1, 0),
                (1, 1),
            ),
            (
                (1, 1, 1),
                (1, 0, 0),
            ),
        ),
        # Z
        (
            (
                (0, 1),
                (1, 1),
                (1, 0),
            ),
            (
                (1, 1, 0),
                (0, 1, 1),
            ),
        ),
        # S
        (
            (
                (1, 0),
                (1, 1),
                (0, 1),
            ),
            (
                (0, 1, 1),
                (1, 1, 0),
            ),
        ),
        # I
        (
            (
                (0, 1),
                (0, 1),
                (0, 1),
                (0, 1),
            ),
            (
                (1, 1, 1, 1),
                (0, 0, 0, 0),
            ),
        )
    )

    def __init__(self, type: int, dir: int):
        self.type = type
        # где-то поворотов надо всего два, вот и разделяю по кейсам
        self.dirs = len(self._figs[type])
        self.dir = dir % self.dirs
        self.grid = ()
        self.__update()

    def rotate_clockwise(self):
        self.dir = (self.dir + 1) % self.dirs
        self.__update()

    def __update(self):
        self.grid = self._figs[self.type][self.dir]
        self.height = len(self.grid)
        self.width = len(self.grid[0])

    # дебаг 90 lvl
    # def print_fig(self):
    #     for i in range(self.height):
    #         print(self.grid[i])
    #
    # def __print_figs(self):
    #     for i in range(len(self._figs)):
    #         for j in range(len(self._figs[i])):
    #             for k in range(len(self._figs[i][j])):
    #                 print(self._figs[i][j][k])


class Matrix:
    """Класс игрового поля"""

    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
        self.grid: list = [
            [1 for j in range(width)] for i in range(height)
        ]

    def full_rows(self) -> tuple:
        """Возвращает кортеж из номеров заполненных рядов"""

        full_rows: list = []
        for row in range(self.height):
            # добавили номер ряда если он полный
            full_rows.append(row) if all(self.grid[row]) else 0
        return tuple(full_rows)

    def shrink_rows(self, rows_to_shrink: tuple) -> None:
        """Убирает указанные ряды и дополняет поле пустыми рядами"""

        for row in rows_to_shrink:
            self.grid.pop(-(self.height - row))
            self.grid.insert(0, [0] * self.width)


# f = Figure(Fig.Z, Dir.RIGHT)
# f.print_fig()
# f.rotate_clockwise()
# f.print_fig()

# m = Matrix(*MATRIX_SIZE)
# print_matrix()
# print(m.full_rows())
# m.shrink_rows(m.full_rows())
# print_matrix()