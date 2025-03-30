import re

from src.Field import Field
from src.Solver import Solver


def get_field(command: str) -> list[list[int]]:
    cells = command.split(" ")

    n = len(cells)

    matrix: list[list[int]] = []
    row: list[int] = []

    for j in range(n):
        try:
            row[j] = int(cells[j])
        except ValueError:
            print("В матрице должны быть только натуральные числа")
            return []

    matrix.append(row)

    for _i in range(1, n):
        cells = input().split(" ")

        row = []

        if len(cells) != n:
            return []

        for j in range(n):
            try:
                row[j] = int(command[j])
            except ValueError:
                print("В матрице должны быть только натуральные числа")
                return []

        else:
            matrix.append(row)

    return matrix


def main() -> int:
    limit = 0
    straight = 1

    row_pattern = re.compile(r"((\d)+\s)+(\d)+")

    print(
        """
    Это программа, решающая головоломку Hitori!
    Введите построчно игровое поле Hitori или команду -help для справки
    """
    )

    while True:
        command = input()

        if row_pattern.fullmatch(command):
            matrix = get_field(command)

            if not len(matrix):
                continue

            ffield = Field(matrix)
            solver = Solver(matrix)

            result = solver.solve()

            for r in result:
                ffield.print_painted_over(r)

            # solves: list[list[list[str]]] = []
            #
            # for r in result:
            #     solves.append(ffield.paint_over_matrix(r))
            #
            # for s in solves:
            #     for r in s:
            #         print(r)
            #     print("--------")

        args = command.split()

        if not len(args):
            continue

        if args[0] in ("-help", "--h"):
            print(
                """
    Это программа, решающая головоломку Hitori!
    Для решения введите построчно игровое поле Hitori
    Поле должно быть квадратным и состоять только из натуральных чисел

    Чтобы ограничить сумму чисел в столбцах и строках до N введите:
        -limit N

    Сразу выводить первые N решений (По умолчанию 1):
        -printstr N

    Вывести еще N решений:
        -printnxt N
                """
            )

        elif args[0] in ("-exit", "-quit"):
            print("Пока-пока!")
            return 0

        if len(args) == 1:
            continue

        elif args[0] == "-limit":
            limit = int(args[1])

        elif args[0] == "-printstr":
            straight = int(args[1])

        elif args[0] == "-printnxt":
            # print_next(command[1])
            pass

        elif args[0] == "-useless":
            print(limit, straight)
            pass


if __name__ == "__main__":
    main()
