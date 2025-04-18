import re

from hitori_solver.hitori.field import Field
from hitori_solver.hitori.solver import Solver


class Handler:
    """
    Управляет взаимодействием с классом Solver,
    может принимать матрицу из потока ввода и выводить в поток вывода результат
    """

    def __init__(self) -> None:
        self._field: Field
        self._limit = 0

    def change_limit(self, new_limit: int) -> None:
        """
        Изменяет предел суммы чисел в строках и столбцах до модуля new_limit
        При значении 0 снимает ограничение
        """
        self._limit = abs(new_limit)

    def input_field(self, size: int) -> None:
        """
        С помощью input() принимает size строк

        В каждой строке должны быть size чисел, иначе выбрасывается ValueError
        В строке ищутся только числа с помощью регулярного выражения '/d+'
        Сумма чисел в каждой строке и столбце должна не превышать _limit, иначе выбрасывается ValueError
        Полученные числа собирает в матрицу и создает из нее экземпляр Field и кладет его в _field
        """
        row_pattern = re.compile(r"\d+")
        matrix: list[list[int]] = []

        for _i in range(size):
            string = input()

            row = [int(x) for x in row_pattern.findall(string)]

            if self._limit:
                if sum(row) > self._limit:
                    raise ValueError("Превышен лимит суммы в строке")

            if len(row) != size:
                raise ValueError(f"В каждой строке должно быть {size} натуральных чисел")
            else:
                matrix.append(row)

        if self._limit:
            for y in range(size):
                if sum([matrix[x][y] for x in range(size)]) > self._limit:
                    raise ValueError("Превышен лимит суммы в столбце")

        self._field = Field(matrix)

    def solve_and_print(self) -> None:
        """
        Подает _field в экземпляр Solver и выводит один ответ
        Если остались еще ответы, с помощью input() предлагает ввести число ответов, которые еще следует вывести
        """

        print("Считаю...")

        solver = Solver(self._field)
        result = solver.solve()
        n = len(result)

        if n == 0:
            print("Решений нет")

        elif n == 1:
            print("Найдено единственное минимальное решение:")
            self._field.print_painted_over(result[0])

        else:
            print(f"Найдено {n} минимальных решений, вот первое:")
            self._field.print_painted_over(result[0])
            print("Сколько еще вывести?")

            string = input()

            if string.isdigit() and (int(string) > 0):
                for index in range(1, int(string) + 1):
                    try:
                        print("-------------------------")
                        self._field.print_painted_over(result[index])
                    except IndexError:
                        print("Выведены все минимальные решения")
                        break
