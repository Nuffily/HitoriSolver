import copy
import queue

from src.Field import Field
from src.Tiling import Tiling


class Solver:
    def __init__(self, matrix: list[list[int]]) -> None:
        self.field = Field(matrix)
        self.size = self.field.size
        self.answer: list[list[list[int]]] = []

    def solve(self) -> list[list[list[int]]]:
        sets: list[list[tuple[int, int]]] = []

        field = copy.deepcopy(self.field)
        field2 = copy.deepcopy(self.field)
        for i in range(self.size):
            set_count = len(sets)

            for j in range(self.size):
                if field(i, j) == 0:
                    continue

                current = [(i, j)]

                for k in range(j + 1, self.size):
                    if field(i, j) == field(i, k):
                        field.erase(i, k)
                        current.append((i, k))

                if len(current) > 1:
                    sets.append(current)

            for j in range(self.size):
                if field2(j, i) == 0:
                    continue

                current = [(j, i)]

                for k in range(j + 1, self.size):
                    if field2(j, i) == field2(k, i):
                        field2.erase(k, i)
                        current.append((k, i))

                if len(current) > 1:
                    sets.append(current)

            if i > 0:
                if set_count != len(sets):
                    # print(i)
                    sets.append([(-1, i)])

        # field = copy.deepcopy(self.field)
        # for j in range(self.size):
        #     for i in range(self.size):
        #         if field(i, j) == 0:
        #             continue
        #
        #         current = [(i, j)]
        #
        #         for k in range(i + 1, self.size):
        #             if field(i, j) == field(k, j):
        #                 field.erase(k, j)
        #                 current.append((k, j))
        #
        #         if len(current) > 1:
        #             dilemma.append(current)

        # print(sets)

        # table = self.create_zero_field()

        self.resolve_sets(sets, Tiling(self.size), 0)

        return self.answer

    def create_zero_field(self) -> list[list[int]]:
        return [[0] * self.size for _ in range(self.size)]

    def resolve_sets(self, sets: list[list[tuple[int, int]]], tiling: Tiling, i: int) -> None:
        if i == len(sets):
            if not (tiling.is_a_enclosed_in_column(self.size - 1) | tiling.is_a_enclosed_in_column(self.size - 1)):
                if tiling.check_connection():
                    self.answer.append(tiling.get_int_matrix())
                    print("yappie!")

            # for d in tiling.get_int_matrix():
            #     print(d)
            #
            # print("------------")

            return

        set = sets[i]
        i = i + 1

        # print(i)

        if len(set) == 1:
            # print(set)
            if not (tiling.is_a_enclosed_in_column(set[0][1] - 1) | tiling.is_a_enclosed_in_column(set[0][1] - 1)):
                self.resolve_sets(sets, tiling, i)
            # else:
            # for d in tiling.get_int_matrix():
            #     print(d)
            # print("-----")
            return

        for j in set:
            if not tiling(j):
                break

        else:
            self.resolve_sets(sets, tiling, i)

        for j in set:
            if tiling(j):
                continue

            changed = []

            # new_table = copy.deepcopy(tiling)
            for k in set:
                if not k == j:
                    if tiling.can_be_painted_over(k):
                        if tiling.paint_over(k):
                            changed.append(k)

                    else:
                        break
            else:
                self.resolve_sets(sets, tiling, i)

            for k in changed:
                tiling.erase(k)

    # def solve_row(self, sets: list[list[tuple[int, int]]], table: list[list[int]], i: int) -> None:
    #     if i == len(sets):
    #         if self.check_connection(table):
    #             self.answer.append(table)
    #
    #         # for d in table:
    #         #     print(d)
    #         #
    #         # print(self.check_connection(table))
    #         # print("------------")
    #
    #         return
    #
    #     set = sets[i]
    #     i = i + 1
    #
    #     # if len(set) == 1:
    #     #
    #
    #     for j in set:
    #         if not table[j[0]][j[1]]:
    #             break
    #     else:
    #         self.solve_row(sets, copy.deepcopy(table), i)
    #
    #     for j in set:
    #         if table[j[0]][j[1]]:
    #             continue
    #         new_table = copy.deepcopy(table)
    #         for k in set:
    #             if not k == j:
    #                 if self.valid(new_table, k):
    #                     new_table[k[0]][k[1]] = 1
    #                 else:
    #                     break
    #         else:
    #             self.solve_row(sets, new_table, i)

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

    def is_closed(self, table: list[list[int]], point: tuple[int, int]) -> bool:
        if point[0] != 0:
            if not table[point[0] - 1][point[1]]:
                return False
        if point[0] != self.size - 1:
            if not table[point[0] + 1][point[1]]:
                return False
        if point[1] != 0:
            if not table[point[0]][point[1] - 1]:
                return False
        if point[1] != self.size - 1:
            if not table[point[0]][point[1] + 1]:
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
    # [
    #             [2, 3, 3, 4, 1],
    #             [5, 2, 4, 4, 3],
    #             [1, 2, 2, 5, 1],
    #             [3, 4, 2, 2, 5],
    #             [4, 3, 5, 3, 3]
    #         ]
    # [
    #     [10, 2, 2, 4, 3, 6, 5, 8, 6, 6],
    #     [8, 10, 9, 5, 6, 3, 1, 6, 4, 2],
    #     [5, 2, 1, 2, 8, 6, 10, 2, 7, 6],
    #     [7, 1, 7, 8, 3, 2, 3, 9, 7, 10],
    #     [1, 2, 4, 2, 7, 2, 9, 2, 8, 5],
    #     [6, 8, 7, 10, 6, 5, 2, 4, 7, 1],
    #     [9, 4, 3, 4, 10, 6, 4, 5, 2, 4],
    #     [4, 3, 4, 9, 4, 8, 4, 6, 10, 4],
    #     [3, 2, 8, 4, 5, 6, 7, 2, 1, 6],
    #     [6, 5, 10, 2, 2, 7, 6, 1, 2, 8],
    # ]
    # [
    #     [9, 6, 3, 3, 2, 7, 8, 3, 10, 7],
    # [5, 6, 8, 2, 6, 9, 1, 4, 6, 10],
    # [4, 7, 6, 4, 3, 1, 4, 10, 9, 4],
    # [4, 2, 10, 8, 5, 10, 3, 5, 4, 1],
    # [7, 7, 9, 3, 10, 2, 1, 8, 3, 3],
    # [3, 9, 10, 7, 8, 4, 5, 1, 8, 2],
    # [1, 10, 4, 10, 8, 3, 9, 3, 7, 6],
    # [3, 4, 3, 1, 3, 8, 3, 6, 5, 3],
    # [10, 8, 2, 3, 4, 3, 7, 3, 8, 9],
    # [3, 10, 5, 9, 1, 6, 7, 7, 2, 3]
    #      ]
    #     [0, 0, 1, 0, 0, 0, 0, 1, 0, 1]
    # [0, 1, 0, 0, 1, 0, 0, 0, 0, 0]
    # [0, 0, 0, 1, 0, 0, 1, 0, 0, 1]
    # [1, 0, 1, 0, 0, 0, 0, 1, 0, 0]
    # [0, 1, 0, 1, 0, 0, 1, 0, 0, 1]
    # [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
    # [0, 1, 0, 0, 0, 0, 0, 1, 0, 0]
    # [1, 0, 0, 0, 1, 0, 1, 0, 0, 1]
    # [0, 0, 0, 1, 0, 1, 0, 0, 1, 0]
    # [1, 0, 0, 0, 0, 0, 1, 0, 0, 0]
    [
        [7, 5, 9, 14, 11, 3, 6, 2, 5, 8, 12, 5, 10, 6, 5],
        [11, 2, 13, 12, 1, 11, 5, 12, 7, 9, 10, 14, 12, 15, 9],
        [10, 11, 1, 3, 11, 15, 11, 8, 5, 13, 11, 1, 7, 11, 6],
        [1, 1, 2, 9, 10, 9, 4, 11, 7, 12, 15, 5, 9, 3, 7],
        [2, 14, 15, 4, 15, 10, 9, 7, 3, 15, 13, 11, 12, 5, 15],
        [14, 9, 15, 5, 2, 5, 9, 6, 1, 4, 1, 9, 3, 5, 11],
        [2, 12, 2, 15, 2, 9, 3, 2, 8, 2, 11, 6, 2, 4, 2],
        [6, 10, 1, 11, 4, 13, 2, 14, 13, 9, 3, 10, 5, 10, 8],
        [13, 3, 8, 13, 5, 14, 7, 15, 6, 13, 4, 7, 11, 10, 13],
        [15, 13, 15, 1, 3, 2, 8, 15, 11, 6, 15, 9, 15, 12, 4],
        [5, 7, 11, 1, 13, 1, 7, 4, 1, 15, 14, 7, 9, 1, 1],
        [10, 8, 10, 13, 9, 1, 12, 7, 15, 7, 9, 3, 14, 2, 14],
        [8, 7, 14, 9, 15, 4, 10, 3, 4, 5, 9, 4, 1, 9, 12],
        [12, 4, 6, 2, 6, 7, 6, 9, 1, 6, 5, 12, 15, 13, 6],
        [3, 14, 12, 5, 7, 5, 6, 1, 9, 11, 1, 10, 13, 14, 2],
    ]
    # [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1]
    # [1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0]
    # [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0]
    # [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0]
    # [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
    # [0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0]
    # [1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1]
    # [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0]
    # [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0]
    # [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0]
    # [0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1]
    # [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0]
    # [0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0]
    # [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1]
    # [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0]
)
#
#
b = a.solve()

for c in b:
    for d in c:
        print(d)
    print("------------")
