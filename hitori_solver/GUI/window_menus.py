from PIL.ImageQt import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator, QValidator
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

from hitori_solver.hitori.field_generator import FieldGenerator
from hitori_solver.GUI.shared_models import Cell, TableState
from hitori_solver.GUI.table import Table


class MainMenu(QWidget):
    """Главное меню приложения"""

    def __init__(self) -> None:
        super().__init__()

        self.main_layout = QVBoxLayout()

        self.image_label = self._create_image_label("../../images/base.png")
        self.main_layout.addWidget(self.image_label, stretch=1)

        self.button_play = MenuUtils.create_button("Играть")
        self.button_solve = MenuUtils.create_button("Решить")
        self.button_rules = MenuUtils.create_button("Правила")

        self.main_layout.addLayout(MenuUtils.pack_layout(self.button_play, self.button_solve, self.button_rules))

        self.setLayout(self.main_layout)

    def _create_image_label(self, path: str) -> QLabel:
        """Загружает изображение и возвращает QLabel с ним"""
        pixmap = QPixmap(path)
        image_label = QLabel()

        if not pixmap.isNull():
            pixmap = pixmap.scaled(
                600, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
            )
            image_label.setPixmap(pixmap)
        else:
            print("123")

        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return image_label


class SolverMenu(QWidget):
    """Меню для ввода своей головоломки и получения решения на нее"""

    def __init__(self, table_state: TableState | None = None, state_text: str | None = None) -> None:
        super().__init__()

        self.main_layout = QVBoxLayout()

        if table_state:
            self.table = self._create_table_field(table_state.size)
            self.table.set_text_in_cells(table_state.text)
            self.table.paint_over_cells(table_state.painted)
        else:
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

        if state_text:
            self.info_label.setText(state_text)
            if state_text == "Найдено решение":
                MenuUtils.lock_buttons(self.button_solve)
                self.table.setEnabled(False)

        self.main_layout.addLayout(MenuUtils.pack_layout(self.button_menu, self.button_solve))
        self.setLayout(self.main_layout)

    def _recreate_field(self, size: int) -> None:
        """Пересоздает Table размера size и добавляет ее в main_layout"""
        MenuUtils.unlock_buttons(self.button_solve)
        if size < 3 or size > 10:
            self.info_label.setText("Размер поля должен быть в пределах от 3 до 10")
            return

        self.main_layout.removeWidget(self.table)
        self.table.deleteLater()

        self.table = self._create_table_field(size)

        self.info_label.setText("Введите поля таблицы")
        self.main_layout.insertWidget(0, self.table, alignment=Qt.AlignmentFlag.AlignCenter, stretch=1)

    def _create_table_field(self, size: int) -> Table:
        """Создает Table заданного размера, в ячейки которой можно вписать только числа от 0 до 99"""

        table = Table(size)
        table.fill_with_lines(QIntValidator(0, 10))

        return table

    def _try_to_solve(self) -> None:
        """
        Пытается решить введенное в self.field поле Hitori
        При нахождении такового закрашивает клетки соответствующие первому найденному решению, а также запрещает
        изменение таблицы и выключает кнопку "Решить"
        Результат работы выписывает в self.info_label
        """
        try:
            MenuUtils.lock_buttons(self.button_solve)
            self.table.solve_and_paint()
            self.info_label.setText("Найдено решение")

        except ValueError:
            self.info_label.setText("Решений нет")
            MenuUtils.unlock_buttons(self.button_solve)


class PlayMenu(QWidget):
    """Меню для генерации головоломки и позволения пользователю попытаться ее решить"""

    def __init__(self, table_state: TableState | None = None, state_text: str | None = None) -> None:
        super().__init__()

        self.generator = FieldGenerator()

        self.main_layout = QVBoxLayout()
        self.info_label = MenuUtils.create_label("")

        if table_state:
            self.table = self._create_table_field(table_state.size, table_state.text)
            self.table.paint_over_cells(table_state.painted)
            if table_state.toggled:
                self.table.toggle_cells(table_state.toggled)
        else:
            self.table = self._create_table_field(5, self.generator.generate_hitori_field(5))

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

        if state_text:
            self.info_label.setText(state_text)
            if state_text in ("Решение верно!", "Решение"):
                MenuUtils.lock_buttons(self.button_solve, self.button_surrender)
                self.table.setEnabled(False)

        self.main_layout.addLayout(MenuUtils.pack_layout(self.button_menu, self.button_solve, self.button_surrender))
        self.setLayout(self.main_layout)

    def _recreate_field(self, size: int) -> None:
        """Пересоздает Table размера size и добавляет ее в main_layout"""

        MenuUtils.unlock_buttons(self.button_solve, self.button_surrender)
        if size < 3 or size > 8:
            self.info_label.setText("Размер поля должен быть в пределах от 3 до 8")
            return
        self.main_layout.removeWidget(self.table)
        self.table.deleteLater()

        self.table = self._create_table_field(size, self.generator.generate_hitori_field(size))

        # for x in range(self.table.size):
        #     for y in range(self.table.size):
        #         print(str(self.table.cellWidget(x,y)))

        self.main_layout.insertWidget(0, self.table, alignment=Qt.AlignmentFlag.AlignCenter, stretch=1)


    def _create_table_field(self, size: int, field: list[list[int]]) -> "Table":
        """Создает Table заданного размера c кнопка, в которых записываются значения из field"""
        table = Table(size)
        table.fill_with_buttons(field)

        self.info_label.setText("Решайте!")

        return table

    def _check_answer(self) -> None:
        """
        Проверяет введенное решение
        Если оно оказалось верным, выключает таблицу и кнопки "Проверить" и "Сдаться"
        Иначе - пишет в info_label причину
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
        Решает текущее поле и закрашивает клетки соответствующие решению
        После выключает таблицу и кнопки "Проверить" и "Сдаться"
        """
        MenuUtils.lock_buttons(self.button_solve, self.button_surrender)
        self.table.solve_and_paint()
        self.info_label.setText("Решение")


class RulesMenu(QWidget):
    """Меню с правилами игры"""

    def __init__(self) -> None:
        super().__init__()

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

    @staticmethod
    def create_button(inscription: str, size: tuple[int, int] = (150, 40)) -> QPushButton:
        """Создает и возвращает кнопку с поданной надписью и поданного размера"""
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
        """Меняет цвет поданных кнопок и выключает их"""
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
        """Возвращает цвет поданных кнопок в норму и включает их"""
        for button in args:
            button.setEnabled(True)
            button.setStyleSheet(
                """QPushButton {
                background-color: #171d25;
                color: #9ba2aa;
                border: none;
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
