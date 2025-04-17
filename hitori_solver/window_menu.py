from PIL.ImageQt import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator, QValidator
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QVBoxLayout, QWidget

from hitori_solver.field_generator import FieldGenerator
from hitori_solver.shared_models import Cell
from hitori_solver.table import Table


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
    """Меню для ввода своей головоломки и получения решения на нее"""

    def __init__(self) -> None:
        super().__init__()

        self.main_layout = QVBoxLayout()

        self.table = self._create_table_field(5)

        self.main_layout.insertWidget(0, self.table, alignment=Qt.AlignmentFlag.AlignCenter, stretch=1)

        self.info_label = MenuUtils.create_label("Введите все поля или измените размер поля")

        self.main_layout.addLayout(MenuUtils.pack_layout(self.info_label))
        self.main_layout.addSpacing(30)

        self.edit_line_size = MenuUtils.create_line_edit("Введите размер поля", QIntValidator(5, 10))
        self.button_change_table = MenuUtils.create_button("Создать таблицу", (250, 40))

        self.main_layout.addLayout(MenuUtils.pack_layout(self.edit_line_size, self.button_change_table))
        self.main_layout.addSpacing(50)

        self.button_menu = MenuUtils.create_button("Назад")
        self.button_solve = MenuUtils.create_button("Решить")

        self.button_change_table.clicked.connect(
            lambda: self._recreate_field(int(self.edit_line_size.text()))
            if self.edit_line_size.text() != ""
            else self.info_label.setText("Введите размер поля")
        )

        self.button_solve.clicked.connect(self._try_to_solve)

        self.main_layout.addLayout(MenuUtils.pack_layout(self.button_menu, self.button_solve))
        self.setLayout(self.main_layout)

    def _recreate_field(self, size: int) -> None:
        """Пересоздает QTable размера size и добавляет ее в main_layout"""

        MenuUtils.unlock_buttons(self.button_solve)
        if size < 3 or size > 10:
            self.info_label.setText("Размер поля должен быть в пределах от 3 до 10")
            return

        self.main_layout.removeWidget(self.table)
        self.table.deleteLater()

        self.table = self._create_table_field(size)

        self.main_layout.insertWidget(0, self.table, alignment=Qt.AlignmentFlag.AlignCenter, stretch=1)

    def _create_table_field(self, size: int) -> Table:
        """Создает QTable заданного размера, в ячейки которой можно вписать только числа от 0 до 99"""

        table = Table(size)
        table.fill_with_lines(QIntValidator(0, 10))

        return table

    def _try_to_solve(self) -> None:
        """
        Пытается решить введенное в self.field поле Hitori
        При нахождении такового закрашивает клетки соответствующие первому найденному решению
        Результат работы выписывает в self.info_label
        """

        # matrix = MenuUtils.get_matrix(self.table)

        # if not self.table.isEnabled():
        #     self.info_label.setText("Решение уже найдено")
        #     return

        try:
            # solves = self.table.solve()
            #
            # if solves:
            #     tiling = solves[0]
            #     MenuUtils.lock_buttons(self.button_solve)
            #     self.info_label.setText("Найдено решение")
            #
            #     for x in range(0, self.table.size):
            #         for y in range(0, self.table.size):
            #             if tiling(Cell(x, y)):
            #                 self.table.removeCellWidget(x, y)
            #                 item = QTableWidgetItem()
            #                 item.setBackground(QColor(23, 29, 37))
            #                 self.table.setItem(x, y, item)
            #
            #     self.table.setEnabled(False)
            #
            # else:
            #     self.info_label.setText("Решений нет")
            MenuUtils.lock_buttons(self.button_solve)
            self.table.solve_and_paint()
            self.info_label.setText("Найдено решение")

        except ValueError:
            self.info_label.setText("Решений нет")


class PlayMenu(QWidget):
    """Меню для ввода своей головоломки и получения решения на нее"""

    def __init__(self) -> None:
        super().__init__()

        self.generator = FieldGenerator()

        self.main_layout = QVBoxLayout()

        self.info_label = MenuUtils.create_label("")

        self.table = self._create_table_field(5)
        self.main_layout.insertWidget(0, self.table, alignment=Qt.AlignmentFlag.AlignCenter, stretch=1)

        self.main_layout.addLayout(MenuUtils.pack_layout(self.info_label))
        self.main_layout.addSpacing(30)

        self.edit_line_size = MenuUtils.create_line_edit("Введите размер поля", QIntValidator(5, 10))
        self.button_change_table = MenuUtils.create_button("Сгенерировать поле", (250, 40))

        self.main_layout.addLayout(MenuUtils.pack_layout(self.edit_line_size, self.button_change_table))
        self.main_layout.addSpacing(50)

        self.button_menu = MenuUtils.create_button("Назад")
        self.button_solve = MenuUtils.create_button("Проверить")
        self.button_surrender = MenuUtils.create_button("Сдаться")

        self.button_solve.clicked.connect(self._check_answer)
        self.button_surrender.clicked.connect(self._surrender)

        self.button_change_table.clicked.connect(
            lambda: self._recreate_field(int(self.edit_line_size.text()))
            if self.edit_line_size.text() != ""
            else self.info_label.setText("Введите размер поля")
        )

        self.main_layout.addLayout(MenuUtils.pack_layout(self.button_menu, self.button_solve, self.button_surrender))
        self.setLayout(self.main_layout)

    def _recreate_field(self, size: int) -> None:
        """Пересоздает QTable размера size и добавляет ее в main_layout"""

        MenuUtils.unlock_buttons(self.button_solve, self.button_surrender)
        if size < 3 or size > 8:
            self.info_label.setText("Размер поля должен быть в пределах от 3 до 8")
            return

        self.main_layout.removeWidget(self.table)
        self.table.deleteLater()

        self.table = self._create_table_field(size)

        self.main_layout.insertWidget(0, self.table, alignment=Qt.AlignmentFlag.AlignCenter, stretch=1)

    def _create_table_field(self, size: int) -> "Table":
        """Создает QTable заданного размера, в ячейки которой можно вписать только числа от 0 до 99"""

        self.field = self.generator.generate_hitori_field(size)

        table = Table(size)
        table.fill_with_buttons(self.field)

        self.info_label.setText("Решайте!")

        return table

    # def _field_cell(self, table: QTableWidget, x: int, y: int, num: int) -> None:
    #     """Форматирует ячейку QTable по координатам (x, y), добавляя в нее validator"""
    #     item = MenuUtils.ToggleButton(str(num))
    #     table.setCellWidget(x, y, item)
    #
    # def _get_tiling(self) -> Tiling:
    #     """Достает и возвращает матрицу из self.field"""
    #     tiling = Tiling(self.field.get_size())
    #
    #     for x in range(self.table.rowCount()):
    #         row = []
    #         for y in range(self.table.columnCount()):
    #             widget = self.table.cellWidget(x, y)
    #             if widget and isinstance(widget, MenuUtils.ToggleButton):
    #                 if self.table.cellWidget(x, y).is_painted:
    #                     tiling.paint_over(Cell(x, y))
    #             else:
    #                 row.append(0)
    #
    #     return tiling

    def _check_answer(self) -> None:
        """
        Пытается решить введенное в self.field поле Hitori
        При нахождении такового закрашивает клетки соответствующие первому найденному решению
        Результат работы выписывает в self.info_label
        """
        tiling = self.table.get_tiling()

        for x in range(self.table.size):
            for y in range(self.table.size):
                if tiling(Cell(x, y)) and not tiling.can_be_painted_over(Cell(x, y)):
                    self.info_label.setText("Неверно... Закрашенные клетки вплотную")
                    return

        answer = self.table.solve()

        for a in answer:
            if a <= tiling:
                if tiling.check_connection():
                    self.info_label.setText("Решение верно!")
                    MenuUtils.lock_buttons(self.button_solve, self.button_surrender)
                    return
                else:
                    self.info_label.setText("Неверно... Связность нарушена")
                    return

        self.info_label.setText("Неверно... Нужно закрасить больше")

    def _surrender(self) -> None:
        """
        Пытается решить введенное в self.field поле Hitori
        При нахождении такового закрашивает клетки соответствующие первому найденному решению
        Результат работы выписывает в self.info_label
        """
        MenuUtils.lock_buttons(self.button_solve, self.button_surrender)
        self.table.solve_and_paint()
        self.info_label.setText("Решение")


class RulesMenu(QWidget):
    """Меню для ввода своей головоломки и получения решения на нее"""

    def __init__(self) -> None:
        super().__init__()

        self.generator = FieldGenerator()

        self.main_layout = QVBoxLayout()

        self.info_label = MenuUtils.create_label(
            """
    Hitori - это логическая головоломка с простыми правилами и сложным решением.

    Правила игры Hitori просты: Необходимо закрасить некоторые ячейки таблицы, выполнив следующие условия:

    1. В любой строке/столбце ни одно число не должно повторяться
    2. чёрных ячейки не могут быть расположены рядом по горизонтали или вертикали
    3. Все незакрашенные ячейки должны быть объединены в одну группу

    В этой программке вы можете либо попробовать решить сгенерированную ею, либо вписать свою и получить на нее решение

    Сделано на МатМехе
        """
        )

        self.info_label.setWordWrap(True)

        self.main_layout.addLayout(MenuUtils.pack_layout(self.info_label))

        self.button_menu = MenuUtils.create_button("Назад")

        self.main_layout.addLayout(MenuUtils.pack_layout(self.button_menu))
        self.setLayout(self.main_layout)


class MenuUtils:
    """Класс для упрощения создания элементов графического интерфейса"""

    def __init__(self) -> None:
        raise TypeError("Это статический класс")

    # class ToggleButton(QPushButton):
    #     def __init__(self, inscr: str) -> None:
    #         super().__init__(inscr)
    #         self.clicked.connect(self.toggle_color)
    #         self.is_painted = False
    #         self.update_button_color()
    #
    #     def toggle_color(self) -> None:
    #         self.is_painted = not self.is_painted
    #         self.update_button_color()
    #
    #     def update_button_color(self) -> None:
    #         self.setStyleSheet(
    #             f"""
    #             QPushButton {{
    #             border-style: solid;
    #             border-color: black;
    #             border-width: 0px;
    #             border-radius: 0px;
    #             background-color: #{"171d25" if self.is_painted else "9ba2aa"};
    #             color: #{"9ba2aa" if self.is_painted else "171d25"};
    #             border: none;
    #             padding: 0px;
    #             font-size: 20px;
    #             border-radius: 0px;
    #             }}
    #             QPushButton:hover {{
    #                 background-color: #171d35;
    #             }}
    #             QPushButton:pressed {{
    #                 background-color: #070d15;
    #             }}
    #         """
    #         )

    @staticmethod
    def create_table(size: int) -> QTableWidget:
        table = QTableWidget(size, size)

        table.verticalHeader().hide()
        table.horizontalHeader().hide()
        table.resizeColumnsToContents()
        table.resizeRowsToContents()

        table.setStyleSheet(
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

        table.setFixedSize(
            table.horizontalHeader().length() + table.verticalHeader().width(),
            table.verticalHeader().length() + table.horizontalHeader().height(),
        )

        table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        return table

    @staticmethod
    def get_matrix(table: QTableWidget) -> list[list[int]]:
        """Достает и возвращает матрицу из self.field"""
        matrix = []

        for x in range(table.rowCount()):
            row = []
            for y in range(table.columnCount()):
                widget = table.cellWidget(x, y)
                if widget and isinstance(widget, QLineEdit | QPushButton):
                    text = widget.text()
                    row.append(int(text) if text else 0)
                else:
                    row.append(0)
            matrix.append(row)

        return matrix

    @staticmethod
    def create_button(inscription: str, size: tuple[int, int] = (150, 40)) -> QPushButton:
        """Создает и возвращает кнопку с поданной надписью размера 150x40"""
        button = QPushButton(inscription)
        button.setFixedSize(size[0], size[1])
        return button

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
        """Создает и возвращает QLineEdit с поданным валидатором"""
        qline = QLineEdit()
        qline.setValidator(validator)
        qline.setFixedSize(250, 40)
        qline.setPlaceholderText(inscription)
        return qline

    @staticmethod
    def lock_buttons(*args: QPushButton) -> None:
        for button in args:
            button.setEnabled(False)
            button.setStyleSheet(
                """QPushButton {
                                            background-color: #30353f;
                                            color: #171d25;
                                            }"""
            )

    @staticmethod
    def unlock_buttons(*args: QPushButton) -> None:
        for button in args:
            button.setEnabled(True)
            button.setStyleSheet(
                """QPushButton {
                background-color: #171d25;
                color: #;
                border: none;9ba2aa
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #171d35;
            }
            QPushButton:pressed {
                background-color: #070d15;
            }"""
            )
