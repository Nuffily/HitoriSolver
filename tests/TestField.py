import unittest
from io import StringIO
from unittest.mock import patch

from src.Field import Field
from src.Tiling import Tiling


class TestField(unittest.TestCase):
    def test_init_error_not_square(self) -> None:
        matrix = [[1, 2], [1, 2, 3]]
        with self.assertRaises(ValueError):
            Field(matrix)

    # def test_init_error_not_int(self) -> None:
    #     matrix: list[list[???]] = [[1, 2], [1, "g"]] # mypy не позволяет(
    #     with self.assertRaises(ValueError):
    #         Field(matrix)

    def test_init_error_not_positive(self) -> None:
        matrix = [[1, 2], [1, -9]]
        with self.assertRaises(ValueError):
            Field(matrix)

    def test_print_painted_over_wrong_size(self) -> None:
        tiling = Tiling(3)
        matrix = [[1, 2], [1, 9]]
        with self.assertRaises(ValueError):
            Field(matrix).print_painted_over(tiling)

    def test_print_painted_over(self) -> None:
        tiling = Tiling(3)
        matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

        tiling.paint_over((0, 0))
        tiling.paint_over((1, 1))
        tiling.paint_over((1, 2))

        with patch("sys.stdout", new=StringIO()) as fake_out:
            Field(matrix).print_painted_over(tiling)

            # Проверяем, что вывод соответствует ожидаемому
            self.assertEqual("█   2   3   \n4   █   █   \n7   8   9", fake_out.getvalue().strip())
