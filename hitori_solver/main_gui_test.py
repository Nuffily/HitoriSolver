# from PyQt6.QtCore import Qt
# from PyQt6.QtGui import QIntValidator
# from PyQt6.QtWidgets import (
#     QApplication,
#     QLineEdit,
#     QMainWindow,
#     QPushButton,
#     QTableWidget,
#     QTableWidgetItem,
#     QVBoxLayout,
#     QWidget,
# )
#
#
# class MatrixInputWindow(QMainWindow):
#     def __init__(self, rows=15, cols=15):
#         super().__init__()
#
#         self.setStyleSheet(
#             """
#             QMainWindow {
#                 background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
#                     stop:0 #1a3143, stop:1 #1b3239);
#             }
#         """
#         )
#
#         self.setWindowTitle("Matrix Validator Example")
#         self.resize(800, 800)
#
#         # Создаем таблицу
#         self.table = QTableWidget(rows, cols)
#
#         self.table.horizontalHeader().setDefaultSectionSize(20)  # Ширина в пикселях
#
#         self.table.verticalHeader().hide()
#         self.table.horizontalHeader().hide()
#
#         self.table.resizeColumnsToContents()
#         self.table.resizeRowsToContents()
#
#         self.table.setStyleSheet(
#             """
#                     QTableWidget {
#                         background-color: #171d25;
#                         gridline-color: #333;
#                     }
#                     QTableWidget::item {
#                         background-color: #9ba2aa;  /* Основной цвет ячеек */
#                         color: #222222;  /* Цвет текста */
#                         border: 0px solid #171d25;  /* Границы ячеек */
#                     }
#                     QLineEdit {
#                         background-color: #dddddd;
#                         color: #222222;
#                         border: none;
#                     }
#                 """
#         )
#
#         self.table.setFixedSize(
#             self.table.horizontalHeader().length() + self.table.verticalHeader().width(),
#             self.table.verticalHeader().length() + self.table.horizontalHeader().height(),
#         )
#
#         self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
#         self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
#
#         # Запрещаем изменение размера таблицы
#         # self.table.setSizeAdjustPolicy(QTableWidget.SizeAdjustPolicy.AdjustToContents)
#
#         # Установка высоты строк
#
#         # Настраиваем валидатор
#         validator = QIntValidator()
#         validator.setBottom(1)
#
#         # Заполняем таблицу с валидацией
#         for i in range(rows):
#             for j in range(cols):
#                 item = QTableWidgetItem("0")
#
#                 # item.setBackground(QBrush(QColor(0, 230, 255)))
#                 # item.setForeground(QBrush(QColor(0, 0, 139)))
#
#                 item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
#
#                 # Важно: устанавливаем флаги перед добавлением
#                 item.setFlags(
#      item.flags() | Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
#                 )
#
#                 self.table.setItem(i, j, item)
#
#                 # Создаем виджет для ячейки и применяем валидатор
#                 self.table.setCellWidget(i, j, self._create_validated_cell(validator))
#
#         button = QPushButton("Press Me!")
#         button.setCheckable(True)
#         button.clicked.connect(self.get_matrix_values)
#
#         # Размещаем в layout
#         central_widget = QWidget()
#
#         self.layout = QVBoxLayout(central_widget)
#         # Помещаем таблицу в центр сетки (строка 1, столбец 1)
#         zbutton = QPushButton("Press Me!")
#
#         self.layout.addWidget(zbutton)
#         self.layout.addWidget(self.table, alignment=Qt.AlignmentFlag.AlignCenter)
#
#         self.layout.addWidget(button)
#
#         container = QWidget()
#         container.setLayout(self.layout)
#         self.setCentralWidget(container)
#         self.table.viewport().update()
#
#     def _create_validated_cell(self, validator):
#         """Создает валидируемый виджет для ячейки"""
#         widget = QLineEdit()
#         widget.setValidator(validator)
#         widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         return widget
#
#     def get_matrix_values(self):
#         matrix = []
#         for i in range(self.table.rowCount()):
#             row = []
#             for j in range(self.table.columnCount()):
#                 widget = self.table.cellWidget(i, j)
#                 # Проверяем существование виджета и его класс
#                 if widget and isinstance(widget, QLineEdit):
#                     text = widget.text()
#                     row.append(int(text) if text else 0)
#                 else:
#                     row.append(0.0)
#             matrix.append(row)
#         print(matrix)
#
#
# # app.setStyle(QStyleFactory.create("Fusion"))
# #
# # dark_palette = QPalette()
# # dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
# # dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
# # # ... дополнительные настройки палитры ...
# # app.setPalette(dark_palette)
# def cli() -> None:
#     app = QApplication([])
#     app.setStyleSheet(
#         """
#         QMainWindow {
#             background-color: #2b2b2b;
#         }
#       QPushButton {
#             background-color: #171d25;  /* Зеленый */
#             color: #9ba2aa;
#             border: none;
#             padding: 10px 20px;
#             font-size: 16px;
#             border-radius: 5px;
#         }
#         QPushButton:hover {
#             background-color: #171d35;  /* Темно-зеленый при наведении */
#         }
#         QPushButton:pressed {
#             background-color: #070d15;  /* Еще темнее при нажатии */
#         }
#         QTableWidget {
#             background-color: #3c3f41;
#             gridline-color: #000000;
#             color: #000000;
#         }
#         QHeaderView::section {
#             background-color: #171d25;
#             color: #171d25;
#             padding: 4px;
#         }
#     """
#     )
#     window = MatrixInputWindow()  # 4x4 матрица
#     window.show()
#     app.exec()
#
#
# if __name__ == "__main__":
#     cli()
