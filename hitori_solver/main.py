import click

from hitori_solver.handler import Handler


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
