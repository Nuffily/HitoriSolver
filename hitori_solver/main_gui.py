from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget

from hitori_solver.window_menu import MainMenu, PlayMenu, RulesMenu, SolverMenu


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Hitori")
        self.setWindowIcon(QIcon("../images/icon.png"))

        self.resize(800, 800)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        menu = MainMenu()
        solver = SolverMenu()
        play = PlayMenu()
        rules = RulesMenu()

        self.stacked_widget.addWidget(menu)
        self.stacked_widget.addWidget(solver)
        self.stacked_widget.addWidget(play)
        self.stacked_widget.addWidget(rules)

        menu.button_solve.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(solver))
        menu.button_play.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(play))
        menu.button_rules.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(rules))
        solver.button_menu.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(menu))
        play.button_menu.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(menu))
        rules.button_menu.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(menu))

    # def to_main_menu(self):
    #
    #     self.clear()
    #
    #     self.image_label = QLabel()
    #     self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    #     self.load_image("../images/base.png")
    #     self.main_layout.addWidget(self.image_label, stretch=1)
    #
    #     button_layout = QHBoxLayout()
    #     button_layout.addStretch(1)
    #
    #     button_play = QPushButton("Играть")
    #     button_play.setFixedSize(150, 40)
    #     button_layout.addWidget(button_play)
    #
    #     button_solve = QPushButton("Решить")
    #     button_solve.setFixedSize(150, 40)
    #     button_layout.addWidget(button_solve)
    #
    #     button_rules = QPushButton("Правила")
    #     button_rules.setFixedSize(150, 40)
    #     button_layout.addWidget(button_rules)
    #
    #     button_layout.addStretch(1)
    #     self.main_layout.addLayout(button_layout)
    #
    #     button_solve.clicked.connect(self.to_solver)
    #
    # def to_solver(self):
    #
    #     self.clear()

    #     self.table = QTableWidget(8, 8)
    #
    #
    #     self.table.verticalHeader().hide()
    #     self.table.horizontalHeader().hide()
    #
    #     self.table.resizeColumnsToContents()
    #     self.table.resizeRowsToContents()
    #
    #     self.table.setStyleSheet("""
    #        QTableWidget {
    #            background-color: #171d25;
    #            gridline-color: #333;
    #        }
    #        QTableWidget::item {
    #            background-color: #9ba2aa;  /* Основной цвет ячеек */
    #            color: #222222;  /* Цвет текста */
    #            border: 0px solid #171d25;  /* Границы ячеек */
    #                        font-size: 30px;
    #        }
    #        QLineEdit {
    #            background-color: #dddddd;
    #            color: #222222;
    #            border: none;
    #                        font-size: 30px;
    #        }
    #    """)
    #
    #     self.table.setFixedSize(
    #         self.table.horizontalHeader().length() + self.table.verticalHeader().width(),
    #         self.table.verticalHeader().length() + self.table.horizontalHeader().height(),
    #     )
    #
    #     self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    #     self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    #
    #     validator = QIntValidator()
    #     validator.setBottom(1)
    #
    #     # Заполняем таблицу с валидацией
    #     for i in range(8):
    #         for j in range(8):
    #             item = QTableWidgetItem("0")
    #
    #             # item.setBackground(QBrush(QColor(0, 230, 255)))
    #             # item.setForeground(QBrush(QColor(0, 0, 139)))
    #
    #             item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
    #
    #             # Важно: устанавливаем флаги перед добавлением
    #             item.setFlags(
    #             item.flags() | Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
    #             )
    #
    #             self.table.setItem(i, j, item)
    #
    #             # Создаем виджет для ячейки и применяем валидатор
    #             self.table.setCellWidget(i, j, self._create_validated_cell(validator))
    #
    #     button_layout = QHBoxLayout()
    #
    #     # button_layout.addWidget(self.table, alignment=Qt.AlignmentFlag.AlignCenter)
    #
    #     self.main_layout.addWidget(self.table, alignment=Qt.AlignmentFlag.AlignCenter)
    #
    #     button_layout.addStretch(1)
    #
    #
    #
    #     button_play = QPushButton("Назад")
    #     button_play.setFixedSize(150, 40)
    #     button_layout.addWidget(button_play)
    #
    #     button_solve = QPushButton("Решить")
    #     button_solve.setFixedSize(150, 40)
    #     button_layout.addWidget(button_solve)
    #
    #     button_layout.addStretch(1)
    #     self.main_layout.addLayout(button_layout)
    #
    #     button_play.clicked.connect(self.to_main_menu)
    #
    # def _create_validated_cell(self, validator):
    #     """Создает валидируемый виджет для ячейки"""
    #     widget = QLineEdit()
    #     widget.setValidator(validator)
    #     widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
    #     return widget
    #
    # def get_matrix_values(self):
    #     matrix = []
    #     for i in range(self.table.rowCount()):
    #         row = []
    #         for j in range(self.table.columnCount()):
    #             widget = self.table.cellWidget(i, j)
    #             if widget and isinstance(widget, QLineEdit):
    #                 text = widget.text()
    #                 row.append(int(text) if text else 0)
    #             else:
    #                 row.append(0.0)
    #         matrix.append(row)
    #     print(matrix)

    # def load_image(self, path):
    #     """Загрузка и масштабирование изображения"""
    #     pixmap = QPixmap(path)
    #
    #     if not pixmap.isNull():
    #         pixmap = pixmap.scaled(
    #             600, 400,
    #             Qt.AspectRatioMode.KeepAspectRatio,
    #             Qt.TransformationMode.SmoothTransformation
    #         )
    #         self.image_label.setPixmap(pixmap)
    #
    # def clear(self):
    #
    #     old_central = self.centralWidget()
    #     if old_central:
    #         old_central.deleteLater()

    # central_widget = QWidget()
    # self.setCentralWidget(central_widget)
    # self.main_layout = QVBoxLayout()
    # central_widget.setLayout(self.main_layout)


def start() -> None:
    app = QApplication([])
    app.setStyleSheet(
        """
        QMainWindow {
            background-color: #171d25;
        }
      QPushButton {
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
        }
        QTableWidget {
            background-color: #3c3f41;
            gridline-color: #000000;
            color: #000000;
                        padding: 0px 0px ;
                                    font-size: 12px;
        }
        QTableWidget::item {
            padding: 0px 0px ;
            font-size: 12px;
    }

        QLineEdit {
            background-color: #9ba2aa;
            color: #171d25;
            padding: 0px 10px ;
            border: none;
            font-size: 20px;
        }
        QHeaderView::section {
            background-color: #171d25;
            color: #171d25;
            padding: 12px 16px;
        }
        QLabel {
            color: #9ba2aa;
            font-size: 20px;

        }
        QMainWindow {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #1a3143, stop:1 #1b3239);
        }
        QLineEdit::item:selected {
        background-color: 171d25;  /* Цвет фона выделенного элемента */
        color: 9ba2aa;                 /* Цвет текста выделенного элемента */
        }

    """
    )
    window = MainWindow()

    window.show()
    app.exec()


if __name__ == "__main__":
    start()
