from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QValidator
from PyQt6.QtWidgets import QLineEdit, QPushButton, QTableWidget, QTableWidgetItem

from hitori_solver.field import Field
from hitori_solver.shared_models import Cell
from hitori_solver.solver import Solver
from hitori_solver.tiling import Tiling


class Table(QTableWidget):
    def __init__(self, size: int):
        super().__init__(size, size)
        self.size = size
        self.verticalHeader().hide()
        self.horizontalHeader().hide()
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
               padding: 2px 2px ;
           }
            QTableWidget::item:selected {
                background-color: #171d25;
                color: #9ba2aa;
            }
        """
        )

        self.setFixedSize(
            self.horizontalHeader().length() + self.verticalHeader().width(),
            self.verticalHeader().length() + self.horizontalHeader().height(),
        )

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def configure(self) -> None:
        pass

    def fill_with_buttons(self, matrix: list[list[int]]) -> None:
        for x in range(self.size):
            for y in range(self.size):
                self.setCellWidget(x, y, self.ToggleButton(str(matrix[x][y])))

    def get_matrix(self) -> list[list[int]]:
        """Достает и возвращает матрицу из self.field"""
        matrix = []

        for x in range(self.size):
            row = []
            for y in range(self.size):
                widget = self.cellWidget(x, y)
                if widget and isinstance(widget, QLineEdit | QPushButton):
                    text = widget.text()
                    row.append(int(text) if text else 0)
                else:
                    row.append(0)
            matrix.append(row)

        return matrix

    def get_tiling(self) -> Tiling:
        """Достает и возвращает матрицу из self.field"""
        tiling = Tiling(self.rowCount())

        for x in range(self.size):
            for y in range(self.size):
                widget = self.cellWidget(x, y)
                if widget and isinstance(widget, self.ToggleButton) and widget.is_painted:
                    tiling.paint_over(Cell(x, y))

        return tiling

    def solve(self) -> list[Tiling]:
        return Solver(Field(self.get_matrix())).solve()

    def fill_with_lines(self, validator: QValidator) -> None:
        """Форматирует ячейку QTable по координатам (x, y), добавляя в нее validator"""
        for x in range(self.size):
            for y in range(self.size):
                valid_line_edit = QLineEdit()
                valid_line_edit.setValidator(validator)
                valid_line_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setCellWidget(x, y, valid_line_edit)

    # def _fill_ready_table(self, table: QTableWidget, size: int, matrix: list[list[int]]) -> None:
    #     validator = QIntValidator(0, 10)
    #
    #     for x in range(size):
    #         for y in range(size):
    #             self._field_cell(table, x, y, validator)
    #             if matrix[x][y]:
    #                 table.cellWidget(x, y).setText(str(matrix[x][y]))
    #             else:
    #                 table.setEnabled(False)
    #                 table.removeCellWidget(x, y)
    #                 item = QTableWidgetItem()
    #                 item.setBackground(QColor(23, 29, 37))
    #                 table.setItem(x, y, item)

    # def _field_cell(self, field: QTableWidget, x: int, y: int, validator: QValidator) -> None:
    #     """Форматирует ячейку QTable по координатам (x, y), добавляя в нее validator"""
    #     # item = QTableWidgetItem("0")
    #     # item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
    #     # field.setItem(x, y, item)
    #
    #     valid_line_edit = QLineEdit()
    #     valid_line_edit.setValidator(validator)
    #     valid_line_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
    #
    #     field.setCellWidget(x, y, valid_line_edit)
    def paint_over(self, x: int, y: int) -> None:
        self.removeCellWidget(x, y)
        item = QTableWidgetItem()
        item.setBackground(QColor(23, 29, 37))
        self.setItem(x, y, item)

    def solve_and_paint(self) -> None:
        """
        Пытается решить введенное в self.field поле Hitori
        При нахождении такового закрашивает клетки соответствующие первому найденному решению
        Результат работы выписывает в self.info_label
        """

        for x in range(self.size):
            for y in range(self.size):
                if isinstance(self.cellWidget(x, y), self.ToggleButton):
                    if self.cellWidget(x, y).is_painted:
                        self.cellWidget(x, y).toggle_color()
                    print("2133")

        try:
            tiling = self.solve()[0]
        except IndexError:
            raise ValueError("Решений нет")

        for x in range(self.size):
            for y in range(self.size):
                if tiling(Cell(x, y)):
                    self.paint_over(x, y)

        self.setEnabled(False)

    class ToggleButton(QPushButton):
        def __init__(self, inscr: str) -> None:
            super().__init__(inscr)
            self.clicked.connect(self.toggle_color)
            self.is_painted = False
            self.update_button_color()

        def toggle_color(self) -> None:
            self.is_painted = not self.is_painted
            self.update_button_color()

        def update_button_color(self) -> None:
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
