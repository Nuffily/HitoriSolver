import random

from hitori_solver.field import Field
from hitori_solver.shared_models import Cell
from hitori_solver.solver import Solver
from hitori_solver.tiling import Tiling


class Generator:
    """Генератор полей для Hitori"""

    # def generate_hitori_board(self, size):
    #     """
    #     Генерирует поле для головоломки Hitori заданного размера и сложности.
    #
    #     Параметры:
    #     size - размер поля (size x size)
    #     difficulty - уровень сложности ('easy', 'medium', 'hard')
    #
    #     Возвращает:
    #     Двумерный список (матрицу) с числами от 1 до size
    #     """
    #
    #     # Проверка входных параметров
    #     if size < 3:
    #         raise ValueError("Размер поля должен быть не менее 3x3")
    #
    #     # Генерация базового поля (каждое число от 1 до size встречается в каждой строке и столбце)
    #     board = [[(i + j) % size + 1 for i in range(size)] for j in range(size)]
    #
    #     atts = 200
    #
    #
    #     while True:
    #
    #         solves = 1000
    #         # Выбираем случайную строку или столбец и меняем местами две ячейки
    #         if random.random() < 0.75:
    #             # Перемешиваем строку
    #             point_1 = Cell(random.randint(0, size - 1), random.randint(0, size - 1))
    #             point_2 = Cell(random.randint(0, size - 1), random.randint(0, size - 1))
    #             temp = board[point_1.x][point_1.y]
    #             board[point_1.x][point_1.y] = board[point_2.x][point_2.y]
    #             board[point_2.x][point_2.y] = temp
    #
    #             result = len(Solver(Field(board)).solve())
    #
    #             # if result > 0 & result <= solves:
    #             #     solves = result
    #             #     pass
    #             if result > 0:
    #                 pass
    #             else:
    #                 atts -= 1
    #
    #                 temp = board[point_1.x][point_1.y]
    #                 board[point_1.x][point_1.y] = board[point_2.x][point_2.y]
    #                 board[point_2.x][point_2.y] = temp
    #
    #         else:
    #             point_1 = Cell(random.randint(0, size - 1), random.randint(0, size - 1))
    #             was = board[point_1.x][point_1.y]
    #             board[point_1.x][point_1.y] = random.randint(1, size)
    #
    #             result = len(Solver(Field(board)).solve())
    #
    #             # if result > 0 & result <= solves:
    #             #     solves = result
    #             #     pass
    #             if result > 0:
    #                 pass
    #             else:
    #                 atts -= 1
    #
    #                 board[point_1.x][point_1.y] = was
    #
    #         if atts == 0:
    #             return board
    #
    # def hash_generate_hitori_board(self, size):
    #     """
    #     Генерирует поле для головоломки Hitori заданного размера и сложности.
    #
    #     Параметры:
    #     size - размер поля (size x size)
    #     difficulty - уровень сложности ('easy', 'medium', 'hard')
    #
    #     Возвращает:
    #     Двумерный список (матрицу) с числами от 1 до size
    #     """
    #
    #     # Проверка входных параметров
    #     if size < 3:
    #         raise ValueError("Размер поля должен быть не менее 3x3")
    #
    #     # Генерация базового поля (каждое число от 1 до size встречается в каждой строке и столбце)
    #     board = [[(i + j) % size + 1 for i in range(size)] for j in range(size)]
    #
    #     atts = 2000
    #
    #
    #     while True:
    #
    #         painted = 0
    #         # Выбираем случайную строку или столбец и меняем местами две ячейки
    #         if random.random() < 0.75:
    #             # Перемешиваем строку
    #             point_1 = Cell(random.randint(0, size - 1), random.randint(0, size - 1))
    #             point_2 = Cell(random.randint(0, size - 1), random.randint(0, size - 1))
    #
    #             temp = board[point_1.x][point_1.y]
    #             board[point_1.x][point_1.y] = board[point_2.x][point_2.y]
    #             board[point_2.x][point_2.y] = temp
    #
    #             result = Solver(Field(board)).solve()
    #             # if result > 0 & result <= solves:
    #             #     solves = result
    #             #     pass
    #             if result and result[0].__hash__() >= painted:
    #                 painted = result[0].__hash__()
    #                 pass
    #             else:
    #                 atts -= 1
    #
    #                 temp = board[point_1.x][point_1.y]
    #                 board[point_1.x][point_1.y] = board[point_2.x][point_2.y]
    #                 board[point_2.x][point_2.y] = temp
    #
    #         else:
    #             point_1 = Cell(random.randint(0, size - 1), random.randint(0, size - 1))
    #             was = board[point_1.x][point_1.y]
    #             board[point_1.x][point_1.y] = random.randint(1, size)
    #
    #             result = Solver(Field(board)).solve()
    #             # if result > 0 & result <= solves:
    #             #     solves = result
    #             #     pass
    #             if result and result[0].__hash__() >= painted:
    #                 painted = result[0].__hash__()
    #                 pass
    #             else:
    #                 atts -= 1
    #
    #                 board[point_1.x][point_1.y] = was
    #
    #         if atts == 0:
    #             return board
    #
    #         print(atts)
    def generate_hitori_field(self, size: int) -> Field:
        """
        Генерирует решаемое поле для головоломки Hitori заданного размера size.
        Возвращает его в виде экземпляра Field
        2 < size < 9
        """

        if size < 3:
            raise ValueError("Размер поля должен быть не менее 3x3")
        elif size > 8:
            raise ValueError("Размер поля должен быть не более 8x8")

        field = [[(i + j) % size + 1 for i in range(size)] for j in range(size)]

        atts = 1000

        tiling = Tiling(size)

        while True:
            if atts == 0:
                return Field(field)

            if random.random() < 0.75:
                point_1 = Cell(random.randint(0, size - 1), random.randint(0, size - 1))
                point_2 = Cell(random.randint(0, size - 1), random.randint(0, size - 1))

                if tiling(point_2) or tiling(point_1):
                    atts -= 1
                    continue

                temp = field[point_1.x][point_1.y]
                field[point_1.x][point_1.y] = field[point_2.x][point_2.y]
                field[point_2.x][point_2.y] = temp

                result = Solver(Field(field)).solve()

                if result:
                    tiling = result[0]
                    pass
                else:
                    atts -= 1

                    temp = field[point_1.x][point_1.y]
                    field[point_1.x][point_1.y] = field[point_2.x][point_2.y]
                    field[point_2.x][point_2.y] = temp

            else:
                point_1 = Cell(random.randint(0, size - 1), random.randint(0, size - 1))

                if tiling(point_1):
                    atts -= 1
                    continue

                was = field[point_1.x][point_1.y]
                field[point_1.x][point_1.y] = random.randint(1, size)

                result = Solver(Field(field)).solve()

                if result:
                    tiling = result[0]
                    pass
                else:
                    atts -= 1

                    field[point_1.x][point_1.y] = was


gen = Generator()
f = gen.generate_hitori_field(8)

solver = Solver(f)
solve = solver.solve()
f.print_painted_over(solve[0])
# while True:
#     g = gen.generate_hitori_board(8)
#     f = Field(g)
#     solver = Solver(f)
#     solve = solver.solve()
#     if solve:
#         for r in g:
#             print(r)
#
#         for s in solve:
#             f.print_painted_over(s)
#         print(len(solve))
#         break
