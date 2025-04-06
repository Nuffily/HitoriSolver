import click

from hitori_solver.handler import Handler

# def get_field(n: int, limit: int) -> Field:
#     row_pattern = re.compile(r"\d+")
#     matrix: list[list[int]] = []
#
#     for _i in range(n):
#         string = input()
#
#         row = [int(x) for x in row_pattern.findall(string)]
#
#         if limit:
#             if sum(row) > limit:
#                 raise ValueError("Превышен лимит суммы в строке")
#
#         if len(row) != n:
#             raise ValueError(f"В каждой строке должно быть {n} натуральных чисел")
#         else:
#             matrix.append(row)
#
#     if limit:
#         for i in range(n):
#             if sum([matrix[i][j] for j in range(n)]) > limit:
#                 raise ValueError(f"В каждом столбце должно быть {n} натуральных чисел")
#
#     return Field(matrix)
#
#
# def main() -> int:
#     limit = 0
#
#     print(
#         """
#     Это программа, решающая головоломку Hitori!
#     Введите "-solve (РАЗМЕР ПОЛЯ)" для решения или команду -help для справки
#     """
#     )
#
#     while True:
#         command = input()
#
#         args = command.split()
#
#         if not len(args):
#             continue
#
#         if args[0] in ("-help", "--h", "-h"):
#             print(
#                 """
#     Это программа, решающая головоломку Hitori!
#     Для решения введите "-solve (РАЗМЕР ПОЛЯ)", а затем - построчно игровое поле Hitori
#     Поле должно быть квадратным и состоять только из натуральных чисел
#
#     Чтобы ограничить сумму чисел в столбцах и строках до N введите:
#         -limit N
#                 """
#             )
#
#         elif args[0] in ("-exit", "-quit"):
#             print("Пока-пока!")
#             return 0
#
#         if len(args) == 1:
#             continue
#
#         if args[0] in ("-solve", "--s", "-s") and args[1].isdigit() and (int(args[1]) > 0):
#             print(f"Введите {args[1]} строк по {args[1]} натуральных чисел")
#
#             try:
#                 hitori_field = get_field(int(args[1]), limit)
#             except ValueError as e:
#                 print(e)
#                 continue
#
#             print("Считаю...")
#             solver = Solver(hitori_field)
#
#             result = solver.solve()
#
#             n = len(result)
#
#             if n == 0:
#                 print("Решений нет")
#
#             elif n == 1:
#                 print("Найдено единственное минимальное решение:")
#                 hitori_field.print_painted_over(result[0])
#
#             else:
#                 print(f"Найдено {n} минимальных решений, вот первое:")
#                 hitori_field.print_painted_over(result[0])
#                 print("Сколько еще вывести?")
#
#                 string = input()
#
#                 if string.isdigit() and (int(string) > 0):
#                     for i in range(1, int(string) + 1):
#                         try:
#                             print("-------------------------")
#                             hitori_field.print_painted_over(result[i])
#                         except IndexError:
#                             print("Выведены все минимальные решения")
#                             break
#
#         elif args[0] == "-limit" and args[1].isdigit() and int(args[1]) >= 0:
#             limit = int(args[1])
#             if int(args[1]) > 0:
#                 print("Теперь в сумма числе в строке/столбце не превысит " + args[1])
#             else:
#                 print("Ограничение на сумму в строках/столбцах снято")
#


def interactive_loop() -> None:
    """
    Основной цикл программы, принимает ввод и выводит соответствующую команду при совпадении с вводом
    Команды:
        solve/sol/s - ввод и решение головоломки
        limit/lim/l - изменение макс. суммы в строках и столбцах
        help/h - справка
        exit - выход
    """

    handler = Handler()

    while True:
        command = click.prompt("> ", type=str).strip().lower()

        if command == "exit":
            break

        elif command in ("help", "h", "-h"):
            click.echo(
                """
Это программа, решающая головоломку Hitori!
Поле Hitori должно быть квадратным и состоять только из натуральных чисел

Команды:
    help - вывести это окно
    solve - начать решение
    limit - ограничить сумму чисел в столбцах и строках
    exit - выйти
                """
            )

        elif command in ("solve", "s", "-s"):
            size = click.prompt("Введите размер поля", type=int)

            try:
                handler.input_field(size)
            except ValueError as e:
                print(e)
                continue

            handler.solve_and_print()

        elif command in ("limit", "lim", "l"):
            size = click.prompt("Введите максимальное допустимое значение суммы чисел в столбцах и строках", type=int)

            handler.change_limit(size)

        else:
            click.echo("Неизвестная команда, попробуйте 'help'")


@click.command()
def cli() -> None:
    """Interactive CLI application"""
    click.echo(
        "Это программа, решающая головоломку Hitori!\nВведите 'solve' для решения или команду 'help' для справки"
    )
    interactive_loop()


if __name__ == "__main__":
    cli()
