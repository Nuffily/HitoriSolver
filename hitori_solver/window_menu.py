from PIL.ImageQt import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QIntValidator, QValidator
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from hitori_solver.field import Field
from hitori_solver.shared_models import Cell
from hitori_solver.solver import Solver


class MainMenu(QWidget):
    """Главное меню приложения"""

    def __init__(self) -> None:
        super().__init__()

        self.main_layout = QVBoxLayout()

        self.image_label = self.create_image_label("../images/base.png")
        self.main_layout.addWidget(self.image_label, stretch=1)

        self.button_play = MenuUtils.create_button("Играть")
        self.button_solve = MenuUtils.create_button("Решить")
        self.button_rules = MenuUtils.create_button("Правила")

        self.main_layout.addLayout(MenuUtils.pack_layout(self.button_play, self.button_solve, self.button_rules))

        self.setLayout(self.main_layout)

    # def create_button(self, inscription: str) -> QPushButton:
    #     """Создает и возвращает кнопку с поданной надписью размера 150x40"""
    #     button = QPushButton(inscription)
    #     button.setFixedSize(150, 40)
    #     return button
    #
    # def create_main_button_layout(self, *args: QPushButton) -> QHBoxLayout:
    #     """Собирает полученные кнопки в QHBoxLayout и возвращает его"""
    #     button_layout = QHBoxLayout()
    #
    #     button_layout.addStretch(1)
    #     for button in args:
    #         button_layout.addWidget(button)
    #     button_layout.addStretch(1)
    #
    #     return button_layout

    def create_image_label(self, path: str) -> QLabel:
        """Загружает изображение и возвращает QLabel с ним"""
        pixmap = QPixmap(path)
        image_label = QLabel()

        if not pixmap.isNull():
            pixmap = pixmap.scaled(
                600, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
            )
            image_label.setPixmap(pixmap)

        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return image_label


class SolverMenu(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.main_layout = QVBoxLayout()

        self.field = self._create_table_field(5)
        self.main_layout.insertWidget(0, self.field, alignment=Qt.AlignmentFlag.AlignCenter, stretch=1)

        self.info_label = MenuUtils.create_label("Введите все поля или измените размер поля")

        self.main_layout.addLayout(MenuUtils.pack_layout(self.info_label))
        self.main_layout.addSpacing(30)

        self.edit_line_size = MenuUtils.create_line_edit("Введите размер поля", QIntValidator(5, 10))
        self.button_change_table = MenuUtils.create_button("Создать таблицу", (250, 40))

        self.button_change_table.clicked.connect(
            lambda: self._recreate_field(int(self.edit_line_size.text()))
            if self.edit_line_size.text() != ""
            else self.info_label.setText("Введите размер поля")
        )

        self.main_layout.addLayout(MenuUtils.pack_layout(self.edit_line_size, self.button_change_table))
        self.main_layout.addSpacing(50)

        self.button_menu = MenuUtils.create_button("Назад")
        self.button_solve = MenuUtils.create_button("Решить")

        self.button_solve.clicked.connect(self._try_to_solve)

        self.main_layout.addLayout(MenuUtils.pack_layout(self.button_menu, self.button_solve))
        self.setLayout(self.main_layout)

    # def _create_table(self, size):
    #
    #     if size < 3 or size > 10:
    #         self.info_label.setText("Размер поля должен быть в пределах от 3 до 10")
    #         return
    #
    #     if hasattr(self, 'table'):
    #         self.main_layout.removeWidget(self.table)
    #         self.table.deleteLater()
    #
    #     self.table = QTableWidget(size, size)
    #     self.table.verticalHeader().hide()
    #     self.table.horizontalHeader().hide()
    #     self.table.resizeColumnsToContents()
    #     self.table.resizeRowsToContents()
    #
    #     self.table.setStyleSheet("""
    #                        QTableWidget {
    #                            background-color: #171d25;
    #                            gridline-color: #171d25;
    #                            border: 0px;
    #                            font-size: 20px;
    #                            padding: 0px 0px ;
    #                        }
    #
    #                        QLineEdit {
    #                            background-color: #9ba2aa;
    #                            color: #171d25;
    #                            border: none;
    #                            font-size: 25px;
    #                            padding: 2px 2px ;
    #                        }
    #                          QTableWidget::item:selected {
    #                             background-color: #171d25;
    #                             color: #9ba2aa;
    #                         }
    #                    """)
    #
    #     self.table.setFixedSize(
    #         self.table.horizontalHeader().length() + self.table.verticalHeader().width(),
    #         self.table.verticalHeader().length() + self.table.horizontalHeader().height(),
    #     )
    #
    #     self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    #     self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    #
    #     validator = QIntValidator(0, 10)
    #     validator.setBottom(1)
    #
    #     for x in range(size):
    #         for y in range(size):
    #             item = QTableWidgetItem("0")
    #
    #             item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
    #
    #             self.table.setItem(x, y, item)
    #
    #             self.table.setCellWidget(x, y, self._create_validated_cell(validator))
    #
    #     self.main_layout.insertWidget(0, self.table, alignment=Qt.AlignmentFlag.AlignCenter, stretch=1)

    def _recreate_field(self, size: int) -> None:
        """Пересоздает QTable размера size и добавляет ее в main_layout"""

        if size < 3 or size > 10:
            self.info_label.setText("Размер поля должен быть в пределах от 3 до 10")
            return

        self.main_layout.removeWidget(self.field)
        self.field.deleteLater()

        self.field = self._create_table_field(size)

        self.main_layout.insertWidget(0, self.field, alignment=Qt.AlignmentFlag.AlignCenter, stretch=1)

    def _create_table_field(self, size: int) -> QTableWidget:
        """Создает QTable заданного размера, в ячейки которой можно вписать только числа от 0 до 99"""

        field = QTableWidget(size, size)

        field.verticalHeader().hide()
        field.horizontalHeader().hide()
        field.resizeColumnsToContents()
        field.resizeRowsToContents()

        field.setStyleSheet(
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

        field.setFixedSize(
            field.horizontalHeader().length() + field.verticalHeader().width(),
            field.verticalHeader().length() + field.horizontalHeader().height(),
        )

        field.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        field.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        validator = QIntValidator(0, 10)

        for x in range(size):
            for y in range(size):
                self._field_cell(field, x, y, validator)

        return field

    def _field_cell(self, field: QTableWidget, x: int, y: int, validator: QValidator) -> None:
        """Форматирует ячейку QTable по координатам (x, y), добавляя в нее validator"""
        item = QTableWidgetItem("0")
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        field.setItem(x, y, item)

        valid_line_edit = QLineEdit()
        valid_line_edit.setValidator(validator)
        valid_line_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        field.setCellWidget(x, y, valid_line_edit)

    def _get_matrix(self) -> list[list[int]]:
        matrix = []

        for x in range(self.field.rowCount()):
            row = []
            for y in range(self.field.columnCount()):
                widget = self.field.cellWidget(x, y)
                if widget and isinstance(widget, QLineEdit):
                    text = widget.text()
                    row.append(int(text) if text else 0)
                else:
                    row.append(0)
            matrix.append(row)

        return matrix

    def _try_to_solve(self) -> None:
        matrix = self._get_matrix()

        if not self.field.isEnabled():
            self.info_label.setText("Решение уже найдено")
            return

        try:
            field = Field(matrix)
            solver = Solver(field)
            solves = solver.solve()

            if solves:
                tiling = solves[0]

                self.info_label.setText("Найдено решение")

                for x in range(0, len(matrix)):
                    for y in range(0, len(matrix)):
                        if tiling(Cell(x, y)):
                            self.field.removeCellWidget(x, y)
                            item = QTableWidgetItem()
                            item.setBackground(QColor(23, 29, 37))
                            self.field.setItem(x, y, item)

                self.field.setEnabled(False)

            else:
                self.info_label.setText("Решений нет")

        except ValueError as e:
            self.info_label.setText(str(e))


class MenuUtils:
    def __init__(self) -> None:
        raise TypeError("Это статический класс")

    @staticmethod
    def create_button(inscription: str, size: tuple[int, int] = (150, 40)) -> QPushButton:
        """Создает и возвращает кнопку с поданной надписью размера 150x40"""
        button = QPushButton(inscription)
        button.setFixedSize(size[0], size[1])
        return button

    # @staticmethod
    # def create_button_layout(*args: QPushButton) -> QHBoxLayout:
    #     """Собирает полученные кнопки в QHBoxLayout и возвращает его"""
    #     button_layout = QHBoxLayout()
    #
    #     button_layout.addStretch(1)
    #     for button in args:
    #         button_layout.addWidget(button, stretch=0)
    #     button_layout.addStretch(1)
    #
    #     return button_layout
    #
    # @staticmethod
    # def create_label_layout(label: QLabel) -> QHBoxLayout:
    #     """Собирает полученный QLabel в QHBoxLayout и возвращает его"""
    #     label_layout = QHBoxLayout()
    #     label_layout.addWidget(label, stretch=0)
    #     return label_layout

    @staticmethod
    def pack_layout(*args: QLabel | QPushButton | QLineEdit) -> QHBoxLayout:
        """Собирает полученные объекты в QHBoxLayout и возвращает его"""
        button_layout = QHBoxLayout()

        button_layout.addStretch(1)
        for button in args:
            button_layout.addWidget(button, stretch=0)
        button_layout.addStretch(1)

        return button_layout

    @staticmethod
    def create_label(inscription: str) -> QLabel:
        """Создает и возвращает QLabel с поданной надписью"""

        label = QLabel(inscription)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        return label

    @staticmethod
    def create_line_edit(inscription: str, validator: QValidator) -> QLineEdit:
        qline = QLineEdit()
        qline.setValidator(validator)
        qline.setFixedSize(250, 40)
        qline.setPlaceholderText(inscription)
        return qline
