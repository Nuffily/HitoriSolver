import copy
import queue
from collections import deque
from idlelib.configdialog import is_int
from tabnanny import check


class Solver:

    def __init__(self, matrix):
        for i in range(len(matrix)):
            if len(matrix[i]) != len(matrix):
                raise ValueError("Поле Hitori должно быть квадратным")
            for j in range(len(matrix)):
                try:
                    matrix[i][j] = int(matrix[i][j])
                except:
                    raise ValueError("В поле Hitori должны быть лишь целые числа")

                if matrix[i][j] < 1:
                    raise ValueError("В поле Hitori должны быть лишь положительные целые числа")

        self.matrix = matrix
        self.size = len(matrix)

    def solve(self):
        dilemma = []

        matrix = self.matrix
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

        matrix = self.matrix
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
        self.solve_row(dilemma,
                       table, 0)

        print("A")


    def create_zero_matrix(self):
        return [[0] * self.size for _ in range(self.size)]



    def solve_row(self, dilemma, table, i):


        if i == len(dilemma):
            print(self.check_connection(table))
            for t in table:
                print(t)

            print("____")
            return

        set = dilemma[i]
        i = i + 1
        for j in set:
            new_table = copy.deepcopy(table)
            for k in set:
                if not k == j:

                    if self.valid(new_table, k):
                        new_table[k[0]][k[1]] = 1
                    else:
                        break
            else:
                self.solve_row(dilemma, new_table, i)


    def valid(self, table, point):

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


    def check_connection(self, table):

        que = queue.Queue()

        checked = copy.deepcopy(table)

        if table[0][0] == 1:
            que.put((0,1))
        else:
            que.put((0, 0))

        while not que.empty():

            cur = que.get()

            checked[cur[0]][cur[1]] = 1

            if cur[0] != 0:
                if not checked[cur[0] - 1][cur[1]]:
                    que.put((cur[0] - 1,cur[1]))
            if cur[0] != self.size - 1:
                if not checked[cur[0] + 1][cur[1]]:
                    que.put((cur[0] + 1,cur[1]))
            if cur[1] != 0:
                if not checked[cur[0]][cur[1] - 1]:
                    que.put((cur[0], cur[1] - 1))
            if cur[1] != self.size - 1:
                if not checked[cur[0]][cur[1] + 1]:
                    que.put((cur[0],cur[1] + 1))

        for p in checked:
            for f in p:
                if not f:
                    return False

        return True


a = Solver(
    [
        [1, 1, 6, 1, 8, 2, 7, 9, 7, 1],
        [8, 3, 8, 2, 5, 8, 10, 8, 9, 4],
        [5, 6, 9, 7, 2, 8, 6, 3, 2, 1],
        [7, 2, 3, 9, 3, 10, 3, 6, 1, 3],
        [1, 8, 3, 8, 9, 8, 7, 2, 2, 10],
        [1, 4, 7, 10, 7, 3, 1, 1, 8, 9],
        [2, 9, 4, 9, 7, 9, 1, 5, 9, 3],
        [9, 7, 2, 3, 10, 2, 8, 4, 5, 4],
        [3, 9, 3, 1, 6, 5, 3, 10, 3, 7],
        [4, 2, 10, 6, 2, 7, 9, 8, 3, 2]
    ]
)

print(a.matrix)
a.solve()

print("z")
