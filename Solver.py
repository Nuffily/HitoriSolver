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

        if i == self.size:
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
                    new_table[k[0]][k[1]] = 1

            self.solve_row(dilemma, new_table, i)





a = Solver([ [1,3, 1, 3],
             [2,3, 4, 5],
             [2,"2",2 ,2],
             [2,"2",2 ,2]])

print(a.matrix)
a.solve()