import copy

from src.Field import Field
from src.Tiling import Tiling


class Solver:
    def __init__(self, matrix: "Field") -> None:
        self.field = matrix
        self.size = self.field.size
        self.answer: list[Tiling] = []

    def solve(self) -> list[Tiling]:
        sets = self.find_sets_to_resolve()

        self.resolve_sets(sets, Tiling(self.size), 0)

        return self.answer

    def find_sets_to_resolve(self) -> list[list[tuple[int, int]]]:
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

            if (i > 0) & (set_count != len(sets)):
                sets.append([(-1, i)])

        return sets

    def resolve_sets(self, sets: list[list[tuple[int, int]]], tiling: Tiling, i: int) -> None:
        if i == len(sets):
            if (not (tiling.is_a_enclosed_in_column(self.size - 1) | tiling.is_a_enclosed_in_row(self.size - 1))) & (
                tiling.check_connection()
            ):
                self.answer.append(tiling.__copy__())

            return

        pack = sets[i]
        i = i + 1

        if len(pack) == 1:
            if not (tiling.is_a_enclosed_in_column(pack[0][1] - 1) | tiling.is_a_enclosed_in_row(pack[0][1] - 1)):
                self.resolve_sets(sets, tiling, i)

            return

        for j in pack:
            if not tiling(j):
                break

        else:
            self.resolve_sets(sets, tiling, i)

        for j in pack:
            if tiling(j):
                continue

            changed = []

            for k in pack:
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
