import pytest

from hitori_solver.hitori.shared_models import Cell
from hitori_solver.hitori.tiling import Tiling


class TestTiling:
    @pytest.fixture
    def tiling(self) -> Tiling:
        return Tiling(3)

    def test_init(self, tiling: Tiling) -> None:
        assert tiling._size == 3
        assert tiling.get_matrix() == [[False, False, False], [False, False, False], [False, False, False]]

    def test_call_operator(self, tiling: Tiling) -> None:
        assert not tiling(Cell(0, 0))
        tiling.paint_over(Cell(1, 1))
        assert tiling(Cell(1, 1))

    def test_copy(self, tiling: Tiling) -> None:
        tiling.paint_over(Cell(2, 1))
        copy_tiling = tiling.__copy__()

        assert copy_tiling.get_matrix() == tiling.get_matrix()

        copy_tiling.paint_over(Cell(2, 2))
        assert not tiling(Cell(2, 2))

    def test_paint_over(self, tiling: Tiling) -> None:
        assert tiling.paint_over(Cell(0, 0))
        assert tiling(Cell(0, 0))
        assert not tiling.paint_over(Cell(0, 0))

    def test_erase(self, tiling: Tiling) -> None:
        tiling.paint_over(Cell(2, 2))
        tiling.erase(Cell(2, 2))
        assert not tiling(Cell(2, 2))

    def test_can_be_painted_over(self, tiling: Tiling) -> None:
        assert tiling.can_be_painted_over(Cell(0, 0))

        tiling.paint_over(Cell(2, 1))
        assert not tiling.can_be_painted_over(Cell(1, 1))
        assert tiling.can_be_painted_over(Cell(0, 0))

    def test_is_enclosed(self, tiling: Tiling) -> None:
        assert not tiling.is_enclosed(Cell(1, 1))

        for i in range(3):
            for j in range(3):
                if not (i == 1 and j == 1):
                    tiling.paint_over(Cell(i, j))

        assert tiling.is_enclosed(Cell(1, 1))
        assert tiling.is_enclosed(Cell(0, 0))

    def test_is_a_enclosed_in_row_column(self, tiling: Tiling) -> None:
        for i in range(3):
            for j in range(3):
                if not (i == 1 and j == 1):
                    tiling.paint_over(Cell(i, j))

        assert tiling.is_a_enclosed_in_row(1)
        assert tiling.is_a_enclosed_in_column(1)

        tiling.erase(Cell(0, 1))
        assert not tiling.is_a_enclosed_in_row(1)
        assert not tiling.is_a_enclosed_in_column(1)

    def test_check_connection(self, tiling: Tiling) -> None:
        assert tiling.check_connection()

        tiling.paint_over(Cell(1, 1))
        assert tiling.check_connection()

        tiling.paint_over(Cell(0, 1))
        tiling.paint_over(Cell(1, 0))
        tiling.paint_over(Cell(1, 2))
        tiling.paint_over(Cell(2, 1))
        assert not tiling.check_connection()

    def test_get_int_matrix(self, tiling: Tiling) -> None:
        assert tiling.get_int_matrix() == [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        tiling.paint_over(Cell(0, 0))
        tiling.paint_over(Cell(1, 1))
        tiling.paint_over(Cell(2, 2))
        assert tiling.get_int_matrix() == [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
