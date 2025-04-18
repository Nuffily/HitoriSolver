from io import StringIO
from unittest.mock import patch

import pytest

from hitori_solver.hitori.field import Field
from hitori_solver.GUI.shared_models import Cell
from hitori_solver.hitori.tiling import Tiling


class TestField:
    @pytest.fixture
    def field(self) -> Field:
        matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        return Field(matrix)

    @pytest.mark.parametrize(
        "input_value",
        [[[1, 2], [3, 4, 5]], [[1, 2, 3], [4, 5, 6]], [[1, 2], [1, -9]]],
        ids=["wrong form", "rectangle", "negative"],
    )
    def test_init_error(self, input_value: list[list[int]]) -> None:
        with pytest.raises(ValueError):
            Field(input_value)

    def test_print_painted_over_wrong_size(self, field: Field) -> None:
        tiling = Tiling(4)
        with pytest.raises(ValueError):
            field.print_painted_over(tiling)

    def test_print_painted_over(self, field: Field) -> None:
        tiling = Tiling(3)
        tiling.paint_over(Cell(0, 0))
        tiling.paint_over(Cell(1, 1))
        tiling.paint_over(Cell(1, 2))

        with patch("sys.stdout", new=StringIO()) as fake_out:
            field.print_painted_over(tiling)
            assert fake_out.getvalue().strip() == "█   2   3   \n4   █   █   \n7   8   9"

    def test_call(self, field: Field) -> None:
        assert field(1, 2) == 6
        assert field(2, 2) == 9

    def test_erase(self, field: Field) -> None:
        field.erase(1, 2)
        assert field(1, 2) == 0
