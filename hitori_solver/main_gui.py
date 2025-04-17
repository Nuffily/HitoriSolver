from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget

from hitori_solver.window_menu import MainMenu, MenuUtils, PlayMenu, RulesMenu, SolverMenu


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Hitori")
        self.setWindowIcon(QIcon("../images/icon.png"))

        self.resize(800, 800)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # try:
        #     with open("saved_data.pickle", "rb") as file:
        #         state = pickle.load(file)
        #         matr = state.solve_table
        #         # for x in range(len(state.solve_table)):
        #         #     for y in range(len(state.solve_table)):
        #         #         if state.solve_table[x][y]:
        #         #             self.solver.table.cellWidget(x, y).setText(str(state.solve_table[x][y]))
        #         #         else:
        #         #             self.solver.table.removeCellWidget(x, y)
        #         #             item = QTableWidgetItem()
        #         #             item.setBackground(QColor(23, 29, 37))
        #         #             self.solver.table.setItem(x, y, item)
        #         #         self.play.table.cellWidget(x, y).setText(str(state.play_table[x][y]))
        #
        # except (EOFError, pickle.UnpicklingError, TypeError, AttributeError, IndexError) as e:
        #     print("Сгорел" + str(e))

        self.menu = MainMenu()
        self.solver = SolverMenu()
        self.play = PlayMenu()
        self.rules = RulesMenu()

        self.stacked_widget.addWidget(self.menu)
        self.stacked_widget.addWidget(self.solver)
        self.stacked_widget.addWidget(self.play)
        self.stacked_widget.addWidget(self.rules)

        self.menu.button_solve.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.solver))
        self.menu.button_play.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.play))
        self.menu.button_rules.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.rules))

        self.solver.button_menu.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.menu))
        self.play.button_menu.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.menu))
        self.rules.button_menu.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.menu))

    # def closeEvent(self, event):
    #     state = AppState(self)
    #     try:
    #         with open("saved_data.pickle", "wb") as file:
    #             pickle.dump(state, file)
    #     except Exception as e:
    #         print(str(e))
    #
    #     event.accept()


class AppState:
    def __init__(self, main: MainWindow):
        self.solve_table = MenuUtils.get_matrix(main.solver.table)
        self.solve_state = main.solver.info_label.text()
        self.play_table = MenuUtils.get_matrix(main.play.table)
        self.play_state = main.play.info_label.text()
        print(self.solve_table)
        print(main.play.table.cellWidget(1, 1).text())


def start() -> None:
    app = QApplication([])
    configure_app(app)
    window = MainWindow()
    window.show()
    app.exec()


def configure_app(app: QApplication) -> None:
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


if __name__ == "__main__":
    start()
