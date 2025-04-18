import random
from typing import Callable

from hitori_solver.hitori.field import Field
from hitori_solver.GUI.shared_models import Cell
from hitori_solver.hitori.solver import Solver
from hitori_solver.hitori.tiling import Tiling


class FieldGenerator:
    """Генератор полей для Hitori"""

    def _swap_cells(self, matrix: list[list[int]], first: Cell, second: Cell) -> Callable[[], None]:
        """
        Меняет местами 2 ячейки поданной матрицы.
        Возвращает функцию, которая откатывает обмен
        """

        temp = matrix[first.x][first.y]
        matrix[first.x][first.y] = matrix[second.x][second.y]
        matrix[second.x][second.y] = temp

        def undo() -> None:
            matrix[second.x][second.y] = matrix[first.x][first.y]
            matrix[first.x][first.y] = temp

        return undo

    def _swap_rows(self, matrix: list[list[int]], first: int, second: int) -> Callable[[], None]:
        """
        Меняет местами 2 строки поданной матрицы.
        Возвращает функцию, которая откатывает обмен
        """

        temp = matrix[first]
        matrix[first] = matrix[second]
        matrix[second] = temp

        def undo() -> None:
            matrix[second] = matrix[first]
            matrix[first] = temp

        return undo

    def _change_value(self, matrix: list[list[int]], cell: Cell, value: int) -> Callable[[], None]:
        """
        Меняет значение ячейки поданной матрицы.
        Возвращает функцию, которая возвращает в ячейку старое значение
        """

        temp = matrix[cell.x][cell.y]
        matrix[cell.x][cell.y] = value

        def undo() -> None:
            matrix[cell.x][cell.y] = temp

        return undo

    def generate_hitori_field(self, size: int) -> list[list[int]]:
        """
        Генерирует решаемое поле для головоломки Hitori заданного размера size.
        Возвращает его в виде экземпляра Field
        2 < size < 9
        """

        if size < 3:
            raise ValueError("Размер поля должен быть не менее 3x3")
        elif size > 8:
            raise ValueError("Размер поля должен быть не более 8x8")

        matrix = [[(i + j) % size + 1 for i in range(size)] for j in range(size)]

        # Перемешиваем строки
        for _ in range(12):
            row_1 = random.randint(0, size - 1)
            row_2 = random.randint(0, size - 1)

            undo = self._swap_rows(matrix, row_1, row_2)

            result = Solver(Field(matrix)).solve()

            if not result:
                undo()

        attempts = 100

        tiling = Tiling(size)

        while True:
            if not attempts:
                return matrix

            # Меняем местами две ячейки
            if random.random() < 0.7:
                point = Cell(random.randint(0, size - 1), random.randint(0, size - 1))
                point_2 = Cell(random.randint(0, size - 1), random.randint(0, size - 1))

                if tiling(point_2) or tiling(point):
                    attempts -= 1
                    continue

                undo = self._swap_cells(matrix, point, point_2)

                result = Solver(Field(matrix)).solve()

                if result:
                    tiling = result[0]
                    pass
                else:
                    attempts -= 1
                    undo()

            # Меняем значение одной ячейки
            else:
                point = Cell(random.randint(0, size - 1), random.randint(0, size - 1))

                if tiling(point):
                    attempts -= 1
                    continue

                undo = self._change_value(matrix, point, random.randint(1, size))

                result = Solver(Field(matrix)).solve()

                if result:
                    tiling = result[0]
                    pass
                else:
                    attempts -= 1

                    undo()
