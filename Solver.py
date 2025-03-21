import copy
from idlelib.configdialog import is_int


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

        print(dilemma)
        self.solve_row(dilemma,
                       [
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]
                   ], 0)



    def solve_row(self, dilemma, table, i):

        if i == len(dilemma):
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

a = Solver([ [1,3, 1, 3],
             [2,3, 4, 5],
             [2,1, 2, 2],
             [2,3, 4, 5]
             ])

print(a.matrix)
a.solve()