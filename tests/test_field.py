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

    def setUp(self) -> None:
        self.matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.field = Field(self.matrix)

    def test_print_painted_over_wrong_size(self) -> None:
        tiling = Tiling(4)

        with self.assertRaises(ValueError):
            Field(self.matrix).print_painted_over(tiling)

    def test_print_painted_over(self) -> None:
        tiling = Tiling(3)

        tiling.paint_over((0, 0))
        tiling.paint_over((1, 1))
        tiling.paint_over((1, 2))

        with patch("sys.stdout", new=StringIO()) as fake_out:
            Field(self.matrix).print_painted_over(tiling)

            self.assertEqual("█   2   3   \n4   █   █   \n7   8   9", fake_out.getvalue().strip())

    def test_call(self) -> None:
        assert self.field(1, 2) == 6
        assert self.field(2, 2) == 9

    def test_erase(self) -> None:
        self.field.erase(1, 2)
        assert self.field(1, 2) == 0
