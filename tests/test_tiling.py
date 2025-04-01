import unittest

from src.Tiling import Tiling


class TestTiling(unittest.TestCase):
    def setUp(self) -> None:
        self.size = 3
        self.tiling = Tiling(self.size)

    def test_init(self) -> None:
        self.assertEqual(self.tiling.size, self.size)
        self.assertEqual(
            self.tiling.get_matrix(), [[False, False, False], [False, False, False], [False, False, False]]
        )

    def test_call_operator(self) -> None:
        self.assertFalse(self.tiling((0, 0)))
        self.tiling.paint_over((1, 1))
        self.assertTrue(self.tiling((1, 1)))

    def test_copy(self) -> None:
        self.tiling.paint_over((2, 1))

        copy_tiling = self.tiling.__copy__()
        self.assertEqual(copy_tiling.get_matrix(), self.tiling.get_matrix())

        copy_tiling.paint_over((2, 2))
        self.assertFalse(self.tiling((2, 2)))

    def test_paint_over(self) -> None:
        self.assertTrue(self.tiling.paint_over((0, 0)))
        self.assertTrue(self.tiling((0, 0)))

        self.assertFalse(self.tiling.paint_over((0, 0)))

    def test_erase(self) -> None:
        self.tiling.paint_over((2, 2))
        self.tiling.erase((2, 2))
        self.assertFalse(self.tiling((2, 2)))

    def test_can_be_painted_over(self) -> None:
        self.assertTrue(self.tiling.can_be_painted_over((0, 0)))

        self.tiling.paint_over((2, 1))
        self.assertFalse(self.tiling.can_be_painted_over((1, 1)))

        self.assertTrue(self.tiling.can_be_painted_over((0, 0)))

    def test_is_enclosed(self) -> None:
        self.assertFalse(self.tiling.is_enclosed((1, 1)))

        for i in range(3):
            for j in range(3):
                if not (i == 1 and j == 1):
                    self.tiling.paint_over((i, j))

        self.assertTrue(self.tiling.is_enclosed((1, 1)))
        self.assertTrue(self.tiling.is_enclosed((0, 0)))

    def test_is_a_enclosed_in_row_column(self) -> None:
        for i in range(3):
            for j in range(3):
                if not (i == 1 and j == 1):
                    self.tiling.paint_over((i, j))

        self.assertTrue(self.tiling.is_a_enclosed_in_row(1))
        self.assertTrue(self.tiling.is_a_enclosed_in_column(1))

        self.tiling.erase((0, 1))
        self.assertFalse(self.tiling.is_a_enclosed_in_row(1))
        self.assertFalse(self.tiling.is_a_enclosed_in_column(1))

    def test_check_connection(self) -> None:
        self.assertTrue(self.tiling.check_connection())

        self.tiling.paint_over((1, 1))
        self.assertTrue(self.tiling.check_connection())

        self.tiling.paint_over((0, 1))
        self.tiling.paint_over((1, 0))
        self.tiling.paint_over((1, 2))
        self.tiling.paint_over((2, 1))
        self.assertFalse(self.tiling.check_connection())

    def test_get_int_matrix(self) -> None:
        self.assertEqual(self.tiling.get_int_matrix(), [[0, 0, 0], [0, 0, 0], [0, 0, 0]])

        self.tiling.paint_over((0, 0))
        self.tiling.paint_over((1, 1))
        self.tiling.paint_over((2, 2))
        self.assertEqual(self.tiling.get_int_matrix(), [[1, 0, 0], [0, 1, 0], [0, 0, 1]])
