from hitori_solver.GUI.shared_models import Cell
from hitori_solver.hitori.tiling import Tiling


class Field:
    """
    Является полем Hitori с которым работает класс Solver
    Поле должно быть квадратным и состоять только из натуральных чисел
    """

    _CELL_SIZE = 4

    def __init__(self, matrix: list[list[int]]) -> None:
        """
        Сохраняет в свое поле полученную матрицу.
        Выбрасывает ValueError, если он не квадратна или содержит не только натуральные числа
        """
        self._size = len(matrix)

        self._check_is_valid(matrix)

        self._field = matrix
        self._size = len(matrix)

    def __call__(self, x: int, y: int) -> int:
        """Возвращает поле матрицы по полученным координатам"""
        return self._field[x][y]

    def get_size(self) -> int:
        """Возвращает размер поля"""
        return self._size

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
        self._field[x][y] = 0

    def print_painted_over(self, tiling: Tiling) -> None:
        """
        Выводит поле закрасив на нем ячейки соответствующие тем координатам, в каких у полученной укладки стоят единицы
        Если укладка имеет размер различный с полем, выбрасывается ValueError
        """
        if tiling.get_size() != self._size:
            raise ValueError("Укладка не подходящего размера")

        for row in range(self._size):
            for column in range(self._size):
                if not tiling(Cell(row, column)):
                    print(
                        f"{self._field[row][column]}{" " * (self._CELL_SIZE - len(str(self._field[row][column])))}",
                        end="",
                    )

                else:
                    print(
                        "█" * len(str(self._field[row][column]))
                        + " " * (self._CELL_SIZE - len(str(self._field[row][column]))),
                        end="",
                    )

            print()
