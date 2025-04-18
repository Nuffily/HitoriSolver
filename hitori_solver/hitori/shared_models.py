from typing import NamedTuple


class Cell(NamedTuple):
    x: int
    y: int


class MenuState(NamedTuple):
    table_state: "TableState"
    text: str


class TableState(NamedTuple):
    values: list[list[int]]
    toggled: list[list[bool]] | None
    painted: list[list[bool]]
    size: int
