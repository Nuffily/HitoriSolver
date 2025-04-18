from typing import cast

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QValidator
from PyQt6.QtWidgets import QHeaderView, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem

from hitori_solver.hitori.field import Field
from hitori_solver.hitori.shared_models import Cell
from hitori_solver.hitori.solver import Solver
from hitori_solver.hitori.tiling import Tiling


class Table(QTableWidget):
    """Таблица QTable с методами для игры в Hitori"""

    def __init__(self, size: int):
        super().__init__(size, size)

        vertical = cast(QHeaderView, self.verticalHeader())
        horizontal = cast(QHeaderView, self.horizontalHeader())

        self.matrix_size = size
        vertical.hide()
        horizontal.hide()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

        self.setStyleSheet(
            """
           QTableWidget {
               background-color: #171d25;
               gridline-color: #171d25;
               border: 0px;
               font-size: 20px;
               padding: 0px 0px ;
           }
           QLineEdit {
               background-color: #9ba2aa;
               color: #171d25;
               border: none;
               font-size: 25px;
               padding: 2px 2px;
           }
            QTableWidget::item:selected {
                background-color: #171d25;
                color: #9ba2aa;
            }
        """
        )

        self.setFixedSize(horizontal.length() + vertical.width(), vertical.length() + horizontal.height())

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def fill_with_buttons(self, matrix: list[list[int]]) -> None:
        """Добавляет в каждую ячейку таблицы ToggleButton с текстом из поданной матрицы"""
        for x in range(self.matrix_size):
            for y in range(self.matrix_size):
                self.setCellWidget(x, y, self.ToggleButton(str(matrix[x][y])))

    def get_matrix(self) -> list[list[int]]:
        """Возвращает матрицу значений Table"""
        matrix = []

        for x in range(self.matrix_size):
            row = []
            for y in range(self.matrix_size):
                widget = self.cellWidget(x, y)
                if widget and isinstance(widget, QLineEdit | QPushButton):
                    text = widget.text()
                    row.append(int(text) if text else 0)
                else:
                    row.append(0)
            matrix.append(row)

        return matrix

    def get_tiling(self) -> Tiling:
        """Возвращает Tiling из закрашенных ячеек таблицы"""
        tiling = Tiling(self.rowCount())

        for x in range(self.matrix_size):
            for y in range(self.matrix_size):
                widget = self.cellWidget(x, y)
                if widget and isinstance(widget, self.ToggleButton) and widget.is_painted:
                    tiling.paint_over(Cell(x, y))

        return tiling

    def get_toggled_cells(self) -> list[list[bool]]:
        """Возвращает матрицу соответствующую закрашенным ячейкам, если те - ToggleButton"""
        matrix = [[False] * self.matrix_size for _ in range(self.matrix_size)]
        for x in range(self.matrix_size):
            for y in range(self.matrix_size):
                widget = self.cellWidget(x, y)
                if isinstance(widget, self.ToggleButton) and widget.is_painted:
                    matrix[x][y] = True
                else:
                    matrix[x][y] = False
        return matrix

    def set_text_in_cells(self, matrix: list[list[int]]) -> None:
        """Записывает значения из matrix в таблицу"""
        for x in range(self.matrix_size):
            for y in range(self.matrix_size):
                widget = self.cellWidget(x, y)
                if isinstance(widget, self.ToggleButton | QLineEdit):
                    if matrix[x][y]:
                        widget.setText(str(matrix[x][y]))
                    else:
                        widget.setText("")

    def toggle_cells(self, matrix: list[list[bool]]) -> None:
        """Переключает в закрашенное состояние кнопки таблицы соответствующие единицам в matrix"""
        for x in range(self.matrix_size):
            for y in range(self.matrix_size):
                widget = self.cellWidget(x, y)
                if matrix[x][y] and isinstance(widget, self.ToggleButton) and not widget.is_painted:
                    widget.toggle_color()

    def paint_over_cells(self, matrix: list[list[bool]]) -> None:
        """Закрашивает ячейки таблицы соответствующие единицам в matrix"""
        for x in range(self.matrix_size):
            for y in range(self.matrix_size):
                if matrix[x][y]:
                    self._paint_over(x, y)

    def get_painted_cells(self) -> list[list[bool]]:
        """Возвращает булеву таблицу, единицы в которой соответствуют закрашенным ячейкам"""
        matrix = [[False] * self.matrix_size for _ in range(self.matrix_size)]
        for x in range(self.matrix_size):
            for y in range(self.matrix_size):
                if not self.cellWidget(x, y):
                    matrix[x][y] = True
                else:
                    matrix[x][y] = False
        return matrix

    def solve(self) -> list[Tiling]:
        """Обращает значения таблицы в поле hitori и возвращает список решений для этого поля"""
        return Solver(Field(self.get_matrix())).solve()

    def fill_with_lines(self, validator: QValidator) -> None:
        """Забивает ячейки таблицы с QLineEdit с поданным валидатором"""
        for x in range(self.matrix_size):
            for y in range(self.matrix_size):
                valid_line_edit = QLineEdit()
                valid_line_edit.setValidator(validator)
                valid_line_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setCellWidget(x, y, valid_line_edit)

    def _paint_over(self, x: int, y: int) -> None:
        """Закрашивает ячейку таблицы по поданным координатам"""
        self.removeCellWidget(x, y)
        item = QTableWidgetItem()
        item.setBackground(QColor(23, 29, 37))
        self.setItem(x, y, item)

    def solve_and_paint(self) -> None:
        """
        Пытается решить введенное в self.field поле Hitori
        При нахождении такового закрашивает клетки соответствующие первому найденному решению
        При не наличии решений выдает ValueError
        """

        for x in range(self.matrix_size):
            for y in range(self.matrix_size):
                widget = self.cellWidget(x, y)
                if isinstance(widget, self.ToggleButton):
                    if widget.is_painted:
                        widget.toggle_color()

        try:
            tiling = self.solve()[0]
        except IndexError:
            raise ValueError("Решений нет")

        for x in range(self.matrix_size):
            for y in range(self.matrix_size):
                if tiling(Cell(x, y)):
                    self._paint_over(x, y)

        self.setEnabled(False)

    class ToggleButton(QPushButton):
        """Класс расширяющий QPushButton, которой при нажатии переключает цвет"""

        def __init__(self, inscr: str) -> None:
            super().__init__(inscr)
            self.clicked.connect(self.toggle_color)
            self.is_painted = False
            self._update_button_color()

        def toggle_color(self) -> None:
            """Переключает цвет кнопки"""
            self.is_painted = not self.is_painted
            self._update_button_color()

        def _update_button_color(self) -> None:
            """Переключает цвет кнопки"""
            self.setStyleSheet(
                f"""
                QPushButton {{
                border-style: solid;
                border-color: black;
                border-width: 0px;
                border-radius: 0px;
                background-color: #{"171d25" if self.is_painted else "9ba2aa"};
                color: #{"9ba2aa" if self.is_painted else "171d25"};
                border: none;
                padding: 0px;
                font-size: 20px;
                border-radius: 0px;
                }}
                QPushButton:hover {{
                    background-color: #171d35;
                }}
                QPushButton:pressed {{
                    background-color: #070d15;
                }}
            """
            )
