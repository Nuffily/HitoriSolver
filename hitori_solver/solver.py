import copy

from hitori_solver.field import Field
from hitori_solver.shared_models import Cell
from hitori_solver.tiling import Tiling


class Solver:
    def __init__(self, matrix: "Field") -> None:
        self._field = matrix
        self._size = self._field.get_size()
        self._answer: list[Tiling] = []

    def solve(self) -> list[Tiling]:
        sets = self._find_sets_to_resolve()

        self._resolve_sets(sets, Tiling(self._size), 0)

        return list(set(self._answer))

    def _find_sets_to_resolve(self) -> list[list[Cell]]:
        sets: list[list[Cell]] = []

        field = copy.deepcopy(self._field)
        field2 = copy.deepcopy(self._field)

        for i in range(self._size):
            set_count = len(sets)

            for j in range(self._size):
                if field(i, j) == 0:
                    continue

                current = [Cell(i, j)]

                for k in range(j + 1, self._size):
                    if field(i, j) == field(i, k):
                        field.erase(i, k)
                        current.append(Cell(i, k))

                if len(current) > 1:
                    sets.append(current)

            for j in range(self._size):
                if field2(j, i) == 0:
                    continue

                current = [Cell(j, i)]

                for k in range(j + 1, self._size):
                    if field2(j, i) == field2(k, i):
                        field2.erase(k, i)
                        current.append(Cell(k, i))

                if len(current) > 1:
                    sets.append(current)

            if (i > 0) & (set_count != len(sets)):
                sets.append([Cell(-1, i)])

        return sets

    def _resolve_sets(self, sets: list[list[Cell]], tiling: Tiling, i: int) -> None:
        if i == len(sets):
            if (not (tiling.is_a_enclosed_in_column(self._size - 1) | tiling.is_a_enclosed_in_row(self._size - 1))) & (
                tiling.check_connection()
            ):
                self._answer.append(tiling.__copy__())

            return

        pack = sets[i]
        i = i + 1

        if len(pack) == 1:
            if not (tiling.is_a_enclosed_in_column(pack[0][1] - 1) | tiling.is_a_enclosed_in_row(pack[0][1] - 1)):
                self._resolve_sets(sets, tiling, i)

            return

        for j in pack:
            if not tiling(j):
                break

        else:
            self._resolve_sets(sets, tiling, i)

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
                self._resolve_sets(sets, tiling, i)

            for k in changed:
                tiling.erase(k)
