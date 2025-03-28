from src.Solver import Solver


class TestSolver:
    def test_simple5x5(self) -> None:
        matrix_1 = [[2, 3, 3, 4, 1], [5, 2, 4, 4, 3], [1, 2, 2, 5, 1], [3, 4, 2, 2, 5], [4, 3, 5, 3, 3]]
        solver = Solver(matrix_1)

        result = solver.solve()

        assert result == [[[0, 1, 0, 0, 0], [0, 0, 0, 1, 0], [0, 1, 0, 0, 1], [0, 0, 1, 0, 0], [0, 1, 0, 0, 1]]]

        matrix_2 = [[1, 1, 2, 5, 1], [2, 3, 5, 4, 1], [1, 4, 1, 2, 1], [5, 3, 1, 3, 4], [2, 5, 2, 1, 2]]
        solver = Solver(matrix_2)

        result = solver.solve()

        assert result == [[[1, 0, 1, 0, 1], [0, 0, 0, 0, 0], [0, 0, 1, 0, 1], [0, 1, 0, 0, 0], [1, 0, 0, 0, 1]]]

        matrix_3 = [[4, 5, 5, 1, 3], [3, 1, 4, 3, 1], [3, 2, 4, 5, 4], [2, 3, 5, 3, 2], [5, 4, 3, 2, 3]]
        solver = Solver(matrix_3)

        result = solver.solve()

        assert result == [[[0, 0, 1, 0, 0], [1, 0, 0, 0, 1], [0, 0, 1, 0, 0], [1, 0, 0, 1, 0], [0, 0, 0, 0, 1]]]
