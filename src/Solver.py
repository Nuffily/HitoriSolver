import copy
import queue


class Solver:
    def __init__(self, matrix: list[list[int]]) -> None:
        for i in range(len(matrix)):
            if len(matrix[i]) != len(matrix):
                raise ValueError("Поле Hitori должно быть квадратным")
            for j in range(len(matrix)):
                try:
                    matrix[i][j] = int(matrix[i][j])
                except ValueError:
                    raise ValueError("В поле Hitori должны быть лишь целые числа")

                if matrix[i][j] < 1:
                    raise ValueError("В поле Hitori должны быть лишь положительные целые числа")

        self.matrix = matrix
        self.size = len(matrix)

    def solve(self) -> None:
        dilemma = []

        matrix = copy.deepcopy(self.matrix)
        for i in range(self.size):
            for j in range(self.size):
                if matrix[i][j] == 0:
                    continue

                current = [(i, j)]

                for k in range(j + 1, self.size):
                    if matrix[i][j] == matrix[i][k]:
                        matrix[i][k] = 0
                        current.append((i, k))

                if len(current) > 1:
                    dilemma.append(current)

        matrix = copy.deepcopy(self.matrix)
        for j in range(self.size):
            for i in range(self.size):
                if matrix[i][j] == 0:
                    continue

                current = [(i, j)]

                for k in range(i + 1, self.size):
                    if matrix[i][j] == matrix[k][j]:
                        matrix[k][j] = 0
                        current.append((k, j))

                if len(current) > 1:
                    dilemma.append(current)

        print(dilemma)

        table = self.create_zero_matrix()

        print(table)
        self.solve_row(dilemma, table, 0)

        print("A")

    def create_zero_matrix(self) -> list[list[int]]:
        return [[0] * self.size for _ in range(self.size)]

    def solve_row(self, dilemma: list[list[tuple[int, int]]], table: list[list[int]], i: int) -> None:
        if i == len(dilemma):
            print(self.check_connection(table))
            for t in table:
                print(t)

            print("____")
            return
        set = dilemma[i]
        i = i + 1
        for j in set:
            if table[j[0]][j[1]]:
                continue
            new_table = copy.deepcopy(table)
            for k in set:
                if not k == j:
                    if self.valid(new_table, k):
                        new_table[k[0]][k[1]] = 1
                    else:
                        break
            else:
                self.solve_row(dilemma, new_table, i)

    def valid(self, table: list[list[int]], point: tuple[int, int]) -> bool:
        if point[0] != 0:
            if table[point[0] - 1][point[1]]:
                return False
        if point[0] != self.size - 1:
            if table[point[0] + 1][point[1]]:
                return False
        if point[1] != 0:
            if table[point[0]][point[1] - 1]:
                return False
        if point[1] != self.size - 1:
            if table[point[0]][point[1] + 1]:
                return False
        return True

    def check_connection(self, table: list[list[int]]) -> bool:
        que: queue.Queue[tuple[int, int]] = queue.Queue()

        checked = copy.deepcopy(table)

        if table[0][0] == 1:
            que.put((0, 1))
        else:
            que.put((0, 0))

        while not que.empty():
            cur = que.get()

            checked[cur[0]][cur[1]] = 1

            if cur[0] != 0:
                if not checked[cur[0] - 1][cur[1]]:
                    que.put((cur[0] - 1, cur[1]))
            if cur[0] != self.size - 1:
                if not checked[cur[0] + 1][cur[1]]:
                    que.put((cur[0] + 1, cur[1]))
            if cur[1] != 0:
                if not checked[cur[0]][cur[1] - 1]:
                    que.put((cur[0], cur[1] - 1))
            if cur[1] != self.size - 1:
                if not checked[cur[0]][cur[1] + 1]:
                    que.put((cur[0], cur[1] + 1))

        for p in checked:
            for f in p:
                if not f:
                    return False

        return True


a = Solver(
    # [
    #     [8, 4, 1, 9, 5, 10, 10, 7, 8, 6],
    #     [4, 1, 9, 3, 5, 8, 1, 5, 10, 5],
    #     [4, 5, 4, 10, 6, 7, 7, 9, 7, 3],
    #     [10, 4, 2, 4, 9, 6, 3, 4, 7, 4],
    #     [6, 7, 10, 4, 10, 6, 8, 5, 9, 1],
    #     [7, 4, 5, 4, 8, 4, 2, 3, 4, 10],
    #     [1, 2, 10, 7, 10, 9, 1, 6, 5, 6],
    #     [8, 8, 7, 9, 4, 4, 6, 10, 3, 9],
    #     [5, 3, 8, 6, 2, 10, 9, 8, 4, 7],
    #     [3, 10, 6, 3, 1, 3, 5, 4, 3, 5]
    # ]
    [
        [10, 2, 2, 4, 3, 6, 5, 8, 6, 6],
        [8, 10, 9, 5, 6, 3, 1, 6, 4, 2],
        [5, 2, 1, 2, 8, 6, 10, 2, 7, 6],
        [7, 1, 7, 8, 3, 2, 3, 9, 7, 10],
        [1, 2, 4, 2, 7, 2, 9, 2, 8, 5],
        [6, 8, 7, 10, 6, 5, 2, 4, 7, 1],
        [9, 4, 3, 4, 10, 6, 4, 5, 2, 4],
        [4, 3, 4, 9, 4, 8, 4, 6, 10, 4],
        [3, 2, 8, 4, 5, 6, 7, 2, 1, 6],
        [6, 5, 10, 2, 2, 7, 6, 1, 2, 8],
    ]
    # [
    #     [7, 5, 9, 14, 11, 3, 6, 2, 5, 8, 12, 5, 10, 6, 5],
    #     [11, 2, 13, 12, 1, 11, 5, 12, 7, 9, 10, 14, 12, 15, 9],
    #     [10, 11, 1, 3, 11, 15, 11, 8, 5, 13, 11, 1, 7, 11, 6],
    #     [1, 1, 2, 9, 10, 9, 4, 11, 7, 12, 15, 5, 9, 3, 7],
    #     [2, 14, 15, 4, 15, 10, 9, 7, 3, 15, 13, 11, 12, 5, 15],
    #     [14, 9, 15, 5, 2, 5, 9, 6, 1, 4, 1, 9, 3, 5, 11],
    #     [2, 12, 2, 15, 2, 9, 3, 2, 8, 2, 11, 6, 2, 4, 2],
    #     [6, 10, 1, 11, 4, 13, 2, 14, 13, 9, 3, 10, 5, 10, 8],
    #     [13, 3, 8, 13, 5, 14, 7, 15, 6, 13, 4, 7, 11, 10, 13],
    #     [15, 13, 15, 1, 3, 2, 8, 15, 11, 6, 15, 9, 15, 12, 4],
    #     [5, 7, 11, 1, 13, 1, 7, 4, 1, 15, 14, 7, 9, 1, 1],
    #     [10, 8, 10, 13, 9, 1, 12, 7, 15, 7, 9, 3, 14, 2, 14],
    #     [8, 7, 14, 9, 15, 4, 10, 3, 4, 5, 9, 4, 1, 9, 12],
    #     [12, 4, 6, 2, 6, 7, 6, 9, 1, 6, 5, 12, 15, 13, 6],
    #     [3, 14, 12, 5, 7, 5, 6, 1, 9, 11, 1, 10, 13, 14, 2]
    # ]
)

print(a.matrix)
a.solve()

print("z")
