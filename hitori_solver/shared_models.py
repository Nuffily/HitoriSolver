from typing import NamedTuple


class Cell(NamedTuple):
    x: int
    y: int


class TableState(NamedTuple):
    text: list[list[int]]
    toggled: list[list[bool]] | None
    painted: list[list[bool]]
    size: int
