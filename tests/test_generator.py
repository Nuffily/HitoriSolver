import pytest

from hitori_solver.hitori.field import Field
from hitori_solver.hitori.field_generator import FieldGenerator
from hitori_solver.hitori.solver import Solver


class TestGenerator:
    @pytest.fixture
    def generator(self) -> FieldGenerator:
        return FieldGenerator()

    @pytest.mark.parametrize("size", [3, 4, 5, 6, 7, 8])
    def test_is_solvable(self, generator: FieldGenerator, size: int) -> None:
        field = Field(generator.generate_hitori_field(size))
        assert len(Solver(field).solve())

    @pytest.mark.parametrize("size", [3, 4, 5, 6, 7, 8])
    def test_has_correct_numbers(self, generator: FieldGenerator, size: int) -> None:
        field = Field(generator.generate_hitori_field(size))
        for x in range(size):
            for y in range(size):
                assert field(x, y) in range(1, size + 1)
