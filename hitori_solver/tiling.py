import queue
from copy import deepcopy

from hitori_solver.shared_models import Cell


class Tiling:
    def __init__(self, size: int) -> None:
        self._size = size
        self._matrix: list[list[bool]] = [[False] * size for _ in range(size)]

    def __call__(self, point: Cell) -> bool:
        return self._matrix[point.x][point.y]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Tiling):
            return NotImplemented
        return self._matrix == other._matrix

    def __copy__(self) -> "Tiling":
        result = Tiling(self._size)
        result._matrix = deepcopy(self._matrix)
        return result

    def __hash__(self) -> int:
        result = 0
        for x in range(self._size):
            for y in range(self._size):
                result += self._matrix[x][y]
        return result

    def get_size(self) -> int:
        return self._size

    def get_matrix(self) -> list[list[bool]]:
        return deepcopy(self._matrix)

    def get_int_matrix(self) -> list[list[int]]:
        return [[1 if x else 0 for x in row] for row in self.get_matrix()]

    def paint_over(self, point: Cell) -> bool:
        if not self(point):
            self._matrix[point.x][point.y] = True
            return True
        else:
            return False

    def erase(self, point: Cell) -> None:
        self._matrix[point.x][point.y] = False

    def can_be_painted_over(self, point: Cell) -> bool:
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

    def is_enclosed(self, point: tuple[int, int]) -> bool:
        if point[0] != 0:
            if not self._matrix[point[0] - 1][point[1]]:
                return False
        if point[0] != self._size - 1:
            if not self._matrix[point[0] + 1][point[1]]:
                return False
        if point[1] != 0:
            if not self._matrix[point[0]][point[1] - 1]:
                return False
        if point[1] != self._size - 1:
            if not self._matrix[point[0]][point[1] + 1]:
                return False
        return True

    def is_a_enclosed_in_row(self, row: int) -> bool:
        for i in range(self._size):
            if self.is_enclosed((row, i)):
                return True

        return False

    def is_a_enclosed_in_column(self, column: int) -> bool:
        for i in range(self._size):
            if self.is_enclosed((i, column)):
                return True

        return False

    def check_connection(self) -> bool:
        que: queue.Queue[tuple[int, int]] = queue.Queue()

        matrix = self.get_matrix()

        if matrix[0][0] == 1:
            que.put((0, 1))
        else:
            que.put((0, 0))

        while not que.empty():
            cur = que.get()

            matrix[cur[0]][cur[1]] = True

            if cur[0] != 0:
                if not matrix[cur[0] - 1][cur[1]]:
                    que.put((cur[0] - 1, cur[1]))
            if cur[0] != self._size - 1:
                if not matrix[cur[0] + 1][cur[1]]:
                    que.put((cur[0] + 1, cur[1]))
            if cur[1] != 0:
                if not matrix[cur[0]][cur[1] - 1]:
                    que.put((cur[0], cur[1] - 1))
            if cur[1] != self._size - 1:
                if not matrix[cur[0]][cur[1] + 1]:
                    que.put((cur[0], cur[1] + 1))

        for row in matrix:
            for cell in row:
                if not cell:
                    return False

        return True
