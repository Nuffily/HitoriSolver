import sys

from hitori_solver.CLI.main_cli import cli
from hitori_solver.GUI.main_gui import start


def main() -> None:
    if len(sys.argv) < 2:
        print(
            """
        Для запуска в консольном режиме при запуске введите аргумент '-c'
        Для запуска графического интерфейса - '-g'
        """
        )

    elif sys.argv[1] in ("c", "console", "cli"):
        cli()
    elif sys.argv[1] in ("g", "graphic", "gui"):
        start()

    else:
        print(
            """
        Для запуска в консольном режиме при запуске введите аргумент '-c'
        Для запуска графического интерфейса - '-g'
        """
        )


if __name__ == "__main__":
    main()
