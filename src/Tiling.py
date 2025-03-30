import queue
from copy import deepcopy


class Tiling:
    def __init__(self, size: int) -> None:
        self.size = size
        self.matrix: list[list[bool]] = [[False] * size for _ in range(size)]

    def __call__(self, point: tuple[int, int]) -> bool:
        return self.matrix[point[0]][point[1]]

    def __copy__(self) -> "Tiling":
        result = Tiling(self.size)
        result.matrix = deepcopy(self.matrix)
        return result

    def get_matrix(self) -> list[list[bool]]:
        return deepcopy(self.matrix)

    def get_int_matrix(self) -> list[list[int]]:
        return [[1 if x else 0 for x in row] for row in self.get_matrix()]

    def paint_over(self, point: tuple[int, int]) -> bool:
        if not self(point):
            self.matrix[point[0]][point[1]] = True
            return True
        else:
            return False

    def erase(self, point: tuple[int, int]) -> None:
        self.matrix[point[0]][point[1]] = False

    def can_be_painted_over(self, point: tuple[int, int]) -> bool:
        if point[0] != 0:
            if self.matrix[point[0] - 1][point[1]]:
                return False
        if point[0] != self.size - 1:
            if self.matrix[point[0] + 1][point[1]]:
                return False
        if point[1] != 0:
            if self.matrix[point[0]][point[1] - 1]:
                return False
        if point[1] != self.size - 1:
            if self.matrix[point[0]][point[1] + 1]:
                return False
        return True

    def is_enclosed(self, point: tuple[int, int]) -> bool:
        if point[0] != 0:
            if not self.matrix[point[0] - 1][point[1]]:
                return False
        if point[0] != self.size - 1:
            if not self.matrix[point[0] + 1][point[1]]:
                return False
        if point[1] != 0:
            if not self.matrix[point[0]][point[1] - 1]:
                return False
        if point[1] != self.size - 1:
            if not self.matrix[point[0]][point[1] + 1]:
                return False
        return True

    def is_a_enclosed_in_row(self, row: int) -> bool:
        for i in range(self.size):
            if self.is_enclosed((row, i)):
                return True

        return False

    def is_a_enclosed_in_column(self, column: int) -> bool:
        for i in range(self.size):
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
            if cur[0] != self.size - 1:
                if not matrix[cur[0] + 1][cur[1]]:
                    que.put((cur[0] + 1, cur[1]))
            if cur[1] != 0:
                if not matrix[cur[0]][cur[1] - 1]:
                    que.put((cur[0], cur[1] - 1))
            if cur[1] != self.size - 1:
                if not matrix[cur[0]][cur[1] + 1]:
                    que.put((cur[0], cur[1] + 1))

        for p in matrix:
            for f in p:
                if not f:
                    return False

        return True
