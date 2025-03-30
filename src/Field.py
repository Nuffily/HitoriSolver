from src.Tiling import Tiling


class Field:
    def __init__(self, matrix: list[list[int]]) -> None:
        for i in range(len(matrix)):
            if len(matrix[i]) != len(matrix):
                raise ValueError("Поле Hitori должно быть квадратным")
            for j in range(len(matrix)):
                try:
                    matrix[i][j] = int(matrix[i][j])
                except ValueError:
                    raise ValueError("В поле Hitori должны быть лишь целые числа")

                if matrix[i][j] < 1:
                    raise ValueError("В поле Hitori должны быть лишь положительные целые числа")

        self.field = matrix
        self.size = len(matrix)

    def __call__(self, x: int, y: int) -> int:
        return self.field[x][y]

    def erase(self, x: int, y: int) -> None:
        self.field[x][y] = 0

    # def paint_over_matrix(self, tiling: list[list[int]]) -> list[list[str]]:
    #
    #     result: list[list[str]] = [["▮"] * self.size for _ in range(self.size)]
    #
    #     for row in range(self.size):
    #         for column in range(self.size):
    #             if not tiling[row][column]:
    #                 result[row][column] = self.field[row][column]
    #
    #
    #     return result

    def print_painted_over(self, tiling: Tiling) -> None:
        for row in range(self.size):
            for column in range(self.size):
                if not tiling((row, column)):
                    print(str(self.field[row][column]) + " " * (3 - len(str(self.field[row][column]))), end="")
                else:
                    print("█" + " " * 2, end="")

            print()
