import copy

from hitori_solver.GUI.shared_models import Cell
from hitori_solver.hitori.field import Field
from hitori_solver.hitori.tiling import Tiling


class Solver:
    """
    Класс решающий головоломку Hitori - полученное поле Field
    """

    def __init__(self, matrix: "Field") -> None:
        self._field = matrix
        self._size = self._field.get_size()
        self._answer: list[Tiling] = []

    def solve(self) -> list[Tiling]:
        """
        Решает головоломку относительно ранее полученного поля Field
        Возвращает список решений в виде списка экземпляров Tiling
        """
        sets = self._find_sets_to_resolve()
        self._resolve_sets(sets, Tiling(self._size), 0)
        return list(set(self._answer))

    def _find_sets_to_resolve(self) -> list[list[Cell]]:
        """
        Находит наборы клеток с одинаковыми значениями на всех строках и столбцах поля
        Возвращает список списков, в каждом из которых координаты клеток полей с одинаковым значением и
        лежащих в одной строке/столбце

        Строки и столбцы проходит поочередно уголком из левого верхнего угла: 1 строка -> 1 столбец -> 2 строка...

        Пройдя столбец с i индексом (i > 0) добавляет в список элемент [Cell(-1, i)], говорящий о том,
        что индекс сменился, что пригодится для оптимизации
        """
        sets: list[list[Cell]] = []

        field_to_find_by_rows = copy.deepcopy(self._field)
        field_to_find_by_columns = copy.deepcopy(self._field)

        for index in range(self._size):
            set_count = len(sets)

            sets += self._find_sets_of_same_numbers_in_row(field_to_find_by_rows, index)
            sets += self._find_sets_of_same_numbers_in_column(field_to_find_by_columns, index)

            if (index > 0) & (set_count != len(sets)):
                sets.append([Cell(-1, index)])

        return sets

    def _find_sets_of_same_numbers_in_row(self, field: Field, row: int) -> list[list[Cell]]:
        """
        Находит наборы клеток с одинаковыми значениями в строке по поданному номеру
        Возвращает список списков, в каждом из которых координаты клеток полей с одинаковым значением и
        лежащих строке
        """

        sets: list[list[Cell]] = []

        for y in range(self._size):
            if field(row, y) == 0:
                continue

            pack = [Cell(row, y)]

            for y2 in range(y + 1, self._size):
                if field(row, y) == field(row, y2):
                    field.erase(row, y2)
                    pack.append(Cell(row, y2))

            if len(pack) > 1:
                sets.append(pack)

        return sets

    def _find_sets_of_same_numbers_in_column(self, field: Field, column: int) -> list[list[Cell]]:
        """
        Находит наборы клеток с одинаковыми значениями в столбце по поданному номеру
        Возвращает список списков, в каждом из которых координаты клеток полей с одинаковым значением и
        лежащих столбце
        """

        sets: list[list[Cell]] = []

        for x in range(self._size):
            if field(x, column) == 0:
                continue

            pack = [Cell(x, column)]

            for x2 in range(x + 1, self._size):
                if field(x, column) == field(x2, column):
                    field.erase(x2, column)
                    pack.append(Cell(x2, column))

            if len(pack) > 1:
                sets.append(pack)

        return sets

    def _resolve_sets(self, sets: list[list[Cell]], tiling: Tiling, set_num: int) -> None:
        """
        Поочередно идет по списку sets, рекурсивно вызывая сама себя после обхода каждого подсписка, если для
        текущего подсписка получилось заполнить допустимую укладку и использует return,
        если допустимой закраски текущего подсписка для текущей укладки нет

        Если список полностью пройден, проверяется связность полученной укладки, и если она связна -
        то она добавляется в список ответов - self._answer
        """

        """Обход окончен и все нужные клетки закрашены, проверяем связность"""
        if set_num == len(sets):
            if (not (tiling.is_a_enclosed_in_column(self._size - 1) | tiling.is_a_enclosed_in_row(self._size - 1))) & (
                tiling.check_connection()
            ):
                self._answer.append(tiling.__copy__())
            return

        pack = sets[set_num]
        set_num = set_num + 1

        """
        В выбранном списке один элемент - значит это элемент типа [(-1, i)], а значит, только что были пройдены
        строка и столбец под индексом i.
        Если сейчас в укладке есть замкнутая клетка, то она может быть только в строке i-1  или в столбце i-1,
        Поскольку желательно узнавать о несвязности решения как можно раньше, сейчас проверяем, появились ли
        замкнутые клетки, если да - бросаем решение
        """
        if len(pack) == 1:
            if not (tiling.is_a_enclosed_in_column(pack[0][1] - 1) | tiling.is_a_enclosed_in_row(pack[0][1] - 1)):
                self._resolve_sets(sets, tiling, set_num)
            return

        """Если все клетки набора уже закрашены, значит он уже решен и смысла его рассматривать нет, идем дальше"""
        for free_cell in pack:
            if not tiling(free_cell):
                break
        else:
            self._resolve_sets(sets, tiling, set_num)

        """
        Надо попробовать закрасить все клетки кроме одной в наборе, выбираем единственную клетку,
        которую не закрасим
        """
        for free_cell in pack:
            if tiling(free_cell):
                continue

            """
            Пробуя закрасить клетки, мы меняем общую матрицу. Для того, чтобы не пришлось тратится на глубокое
            копирование каждую итерацию, сохраняем клетки которые мы закрасили, чтобы потом вернуть все на место
            """
            painted_cells = []

            """Пробуем закрасить все оставшиеся"""
            for painted_cell in pack:
                if not painted_cell == free_cell:
                    if tiling.can_be_painted_over(painted_cell):
                        if tiling.paint_over(painted_cell):
                            painted_cells.append(painted_cell)
                    else:
                        break

            else:
                self._resolve_sets(sets, tiling, set_num)

            for painted_cell in painted_cells:
                tiling.erase(painted_cell)
