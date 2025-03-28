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
