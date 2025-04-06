from hitori_solver.shared_models import Cell
from hitori_solver.tiling import Tiling


class Field:
    def __init__(self, matrix: list[list[int]]) -> None:
        """
        Сохраняет в свое поле полученную матрицу.
        Выбрасывает ValueError, если он не квадратна или содержит не только натуральные числа
        """
        self._size = len(matrix)

        self._check_is_valid(matrix)

        self.field = matrix
        self.size = len(matrix)

    def __call__(self, x: int, y: int) -> int:
        """Возвращает поле матрицы по полученным координатам"""
        return self.field[x][y]

    def _check_is_valid(self, matrix: list[list[int]]) -> None:
        """
        Проверяет, является ли матрица квадратной и все ли числа в ней положительны.
        Иначе выбрасывает ValueError
        """
        for x in range(self._size):
            if len(matrix[x]) != len(matrix):
                raise ValueError("Поле Hitori должно быть квадратным")
            for y in range(self._size):
                if matrix[x][y] < 1:
                    raise ValueError("В поле Hitori должны быть лишь положительные целые числа")

    def erase(self, x: int, y: int) -> None:
        """Меняет значение ячейки матрицы по данным координатам на 0"""
        self.field[x][y] = 0

    def print_painted_over(self, tiling: Tiling) -> None:
        if tiling.get_size() != self.size:
            raise ValueError("Укладка не подходящего размера")

        for row in range(self.size):
            for column in range(self.size):
                if not tiling(Cell(row, column)):
                    print(str(self.field[row][column]) + " " * (4 - len(str(self.field[row][column]))), end="")
                else:
                    print("█" + " " * 3, end="")

            print()
