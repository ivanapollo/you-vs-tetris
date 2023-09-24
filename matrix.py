from consts import *


def print_matrix() -> None:
    for i in range(m.height):
        print(*m.grid[i], sep='')


class Matrix:
    """Класс игрового поля"""

    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
        self.grid = [
            [0 for j in range(width)] for i in range(height)
        ]

    def full_rows(self) -> tuple:
        """Возвращает кортеж из номеров заполненных рядов"""

        full_rows = []
        for row in range(self.height):
            # добавили номер ряда если он полный
            full_rows.append(row) if all(self.grid[row]) else 0
        return tuple(full_rows)

    def shrink_rows(self, rows_to_shrink: tuple) -> None:
        """Убирает указанные ряды и дополняет поле пустыми рядами"""

        for row in rows_to_shrink:
            self.grid.pop(-(self.height - row))
            self.grid.insert(0, [0] * self.width)


m = Matrix(*MATRIX_SIZE)
print_matrix()
print(m.full_rows())
m.shrink_rows(m.full_rows())
print_matrix()