import pickle
from enum import IntEnum

from PyQt6.QtGui import QCloseEvent, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget

from hitori_solver.shared_models import TableState
from hitori_solver.window_menu import MainMenu, PlayMenu, RulesMenu, SolverMenu


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Hitori")
        self.setWindowIcon(QIcon("../images/icon.png"))

        self.resize(800, 800)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.menu = MainMenu()
        self.rules = RulesMenu()

        current_widget = MainWidget.MAIN

        try:
            with open("../saved_data.pickle", "rb") as file:
                state: AppState = pickle.load(file)
                self.solver = SolverMenu(state.solver, state.solver_text)
                self.play = PlayMenu(state.play, state.play_text)
                current_widget = state.current_widget

        except (EOFError, FileNotFoundError, TypeError, AttributeError, IndexError) as e:
            print("Сгорел" + str(e))
            self.solver = SolverMenu()
            self.play = PlayMenu()

        self.stacked_widget.addWidget(self.menu)
        self.stacked_widget.addWidget(self.solver)
        self.stacked_widget.addWidget(self.play)
        self.stacked_widget.addWidget(self.rules)

        if current_widget:
            if current_widget == MainWidget.MAIN:
                self.stacked_widget.setCurrentWidget(self.menu)
            elif current_widget == MainWidget.SOLVER:
                self.stacked_widget.setCurrentWidget(self.solver)
            elif current_widget == MainWidget.PLAY:
                self.stacked_widget.setCurrentWidget(self.play)
            elif current_widget == MainWidget.RULES:
                self.stacked_widget.setCurrentWidget(self.rules)

        self.menu.button_solve.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.solver))
        self.menu.button_play.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.play))
        self.menu.button_rules.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.rules))

        self.solver.button_menu.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.menu))
        self.play.button_menu.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.menu))
        self.rules.button_menu.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.menu))

    def closeEvent(self, event: QCloseEvent | None) -> None:
        try:
            state = AppState(self)
            with open("../saved_data.pickle", "wb") as file:
                pickle.dump(state, file)
        except Exception as e:
            print(str(e))

        if event:
            event.accept()


class AppState:
    def __init__(self, main: MainWindow):
        self.solver_text: str = main.solver.info_label.text()

        self.solver: TableState = TableState(
            text=main.solver.table.get_matrix(),
            painted=main.solver.table.get_painted_cells(),
            toggled=None,
            size=main.solver.table.size,
        )
        self.play_text: str = main.play.info_label.text()

        self.play: TableState = TableState(
            text=main.play.table.get_matrix(),
            painted=main.play.table.get_painted_cells(),
            toggled=main.play.table.get_toggled_cells(),
            size=main.play.table.size,
        )
        self.current_widget: MainWidget = MainWidget.MAIN

        if main.stacked_widget.currentWidget() == main.rules:
            self.current_widget = MainWidget.RULES
        elif main.stacked_widget.currentWidget() == main.solver:
            self.current_widget = MainWidget.SOLVER
        elif main.stacked_widget.currentWidget() == main.play:
            self.current_widget = MainWidget.PLAY


class MainWidget(IntEnum):
    MAIN = 0
    SOLVER = 1
    PLAY = 2
    RULES = 3


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
