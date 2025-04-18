import queue
from copy import deepcopy

from hitori_solver.GUI.shared_models import Cell


class Tiling:
    def __init__(self, size: int) -> None:
        """Создает квадратную булеву матрицу размера size"""
        self._size = size
        self._matrix: list[list[bool]] = [[False] * size for _ in range(size)]

    def __call__(self, point: Cell) -> bool:
        """Возвращает значение матрицы в данной клетке"""
        return self._matrix[point.x][point.y]

    def __eq__(self, other: object) -> bool:
        """Проверяет, равны ли матрицы двух укладок"""
        if not isinstance(other, Tiling):
            return NotImplemented
        return self._matrix == other._matrix

    def __le__(self, other: "Tiling") -> bool:
        """
        Сравнивает две матрицы и возвращает False, если есть хоть одна ячейка, в которой первая
        матрица имеет 1, а вторая - 0. Иначе - True
        """

        if self._size != other._size:
            raise ValueError("Матрицы разного размера")

        for x in range(self._size):
            for y in range(self._size):
                if self._matrix[x][y] and not other._matrix[x][y]:
                    return False

        return True

    def __copy__(self) -> "Tiling":
        """Возвращает копию данной укладки"""
        result = Tiling(self._size)
        result._matrix = deepcopy(self._matrix)
        return result

    def __hash__(self) -> int:
        """Возвращает число единиц в матрице"""
        result = 0
        for x in range(self._size):
            for y in range(self._size):
                result += self._matrix[x][y]
        return result

    def get_size(self) -> int:
        """Возвращает размер укладки"""
        return self._size

    def get_matrix(self) -> list[list[bool]]:
        """Возвращает матрицу укладки"""
        return deepcopy(self._matrix)

    def get_int_matrix(self) -> list[list[int]]:
        """Возвращает матрицу укладки заменив тип клеток на int"""
        return [[1 if x else 0 for x in row] for row in self.get_matrix()]

    def paint_over(self, point: Cell) -> bool:
        """
        Меняет значение клетки по координатам point на 1
        Если ячейка была равна 0, то возвращает True, иначе - False
        """
        if not self(point):
            self._matrix[point.x][point.y] = True
            return True
        else:
            return False

    def erase(self, point: Cell) -> None:
        """Меняет значение клетки по координатам point на 0"""
        self._matrix[point.x][point.y] = False

    def can_be_painted_over(self, point: Cell) -> bool:
        """
        Проверяет, есть ли вокруг клетки по координатам point уже закрашенные клетки
        Возвращает True, если нет и False - иначе
        """
        if point[0] != 0:
            if self._matrix[point.x - 1][point.y]:
                return False
        if point[0] != self._size - 1:
            if self._matrix[point.x + 1][point.y]:
                return False
        if point[1] != 0:
            if self._matrix[point.x][point.y - 1]:
                return False
        if point[1] != self._size - 1:
            if self._matrix[point.x][point.y + 1]:
                return False
        return True

    def is_enclosed(self, point: Cell) -> bool:
        """
        Проверяет, есть ли вокруг клетки по координатам point не закрашенные клетки
        Возвращает True, если нет и False - иначе
        """
        if point.x != 0:
            if not self._matrix[point.x - 1][point.y]:
                return False
        if point.x != self._size - 1:
            if not self._matrix[point.x + 1][point.y]:
                return False
        if point.y != 0:
            if not self._matrix[point.x][point.y - 1]:
                return False
        if point.y != self._size - 1:
            if not self._matrix[point.x][point.y + 1]:
                return False
        return True

    def is_a_enclosed_in_row(self, row: int) -> bool:
        """
        Проверяет, есть ли в данном ряду клетки, вокруг которых нет незакрашенных клеток
        Возвращает True, если есть и False - иначе
        """
        for i in range(self._size):
            if self.is_enclosed(Cell(row, i)):
                return True

        return False

    def is_a_enclosed_in_column(self, column: int) -> bool:
        """
        Проверяет, есть ли в данном столбце клетки, вокруг которых нет незакрашенных клеток
        Возвращает True, если есть и False - иначе
        """
        for i in range(self._size):
            if self.is_enclosed(Cell(i, column)):
                return True

        return False

    def check_connection(self) -> bool:
        """
        Проверяет, связана ли матрица относительно незакрашенных клеток,
        то есть - из каждой ли пустой клетки можно добраться в любую другую по пустым клеткам
        Возвращает True, если связана и False - иначе
        """
        que: queue.Queue[Cell] = queue.Queue()

        matrix = self.get_matrix()

        if matrix[0][0] == 1:
            que.put(Cell(0, 1))
        else:
            que.put(Cell(0, 0))

        while not que.empty():
            cur = que.get()

            matrix[cur.x][cur.y] = True

            if cur[0] != 0:
                if not matrix[cur.x - 1][cur.y]:
                    que.put(Cell(cur.x - 1, cur.y))
            if cur[0] != self._size - 1:
                if not matrix[cur.x + 1][cur.y]:
                    que.put(Cell(cur.x + 1, cur.y))
            if cur[1] != 0:
                if not matrix[cur.x][cur.y - 1]:
                    que.put(Cell(cur.x, cur.y - 1))
            if cur[1] != self._size - 1:
                if not matrix[cur.x][cur.y + 1]:
                    que.put(Cell(cur.x, cur.y + 1))

        for row in matrix:
            for cell in row:
                if not cell:
                    return False

        return True
