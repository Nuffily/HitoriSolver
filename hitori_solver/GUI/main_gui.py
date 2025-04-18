import pickle
from enum import IntEnum

from PyQt6.QtGui import QCloseEvent, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget

from hitori_solver.GUI.shared_models import MenuState
from hitori_solver.GUI.window_menus import MainMenu, PlayMenu, RulesMenu, SolverMenu


class MainWindow(QMainWindow):
    """Основное окно программы"""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Hitori")
        self.setWindowIcon(QIcon("../../images/icon.png"))

        self.resize(800, 800)

        self._stacked_widget = QStackedWidget()
        self.setCentralWidget(self._stacked_widget)

        self._menu = MainMenu()
        self._rules = RulesMenu()

        current_widget = MainWidget.MAIN

        try:
            with open("../../saved_data.pickle", "rb") as file:
                state: AppState = pickle.load(file)
                self.play = PlayMenu(state.play_state.table_state, state.play_state.text)
                self.solver = SolverMenu(state.solver_state.table_state, state.solver_state.text)
                current_widget = state.current_widget

        except (EOFError, FileNotFoundError, TypeError, AttributeError, IndexError):
            self.solver = SolverMenu()
            self.play = PlayMenu()

        self._stacked_widget.addWidget(self._menu)
        self._stacked_widget.addWidget(self.solver)
        self._stacked_widget.addWidget(self.play)
        self._stacked_widget.addWidget(self._rules)

        self._stacked_widget.setCurrentWidget(self._enum_to_widget(current_widget))

        self._menu.button_solve.clicked.connect(lambda: self._stacked_widget.setCurrentWidget(self.solver))
        self._menu.button_play.clicked.connect(lambda: self._stacked_widget.setCurrentWidget(self.play))
        self._menu.button_rules.clicked.connect(lambda: self._stacked_widget.setCurrentWidget(self._rules))

        self.solver.button_menu.clicked.connect(lambda: self._stacked_widget.setCurrentWidget(self._menu))
        self.play.button_menu.clicked.connect(lambda: self._stacked_widget.setCurrentWidget(self._menu))
        self._rules.button_menu.clicked.connect(lambda: self._stacked_widget.setCurrentWidget(self._menu))

    def _enum_to_widget(self, current_widget: "MainWidget") -> QWidget:
        """Возвращает QWidget из self, cоответствующий enum'у current_widget"""
        if current_widget == MainWidget.MAIN:
            return self._menu
        elif current_widget == MainWidget.SOLVER:
            return self.solver
        elif current_widget == MainWidget.PLAY:
            return self.play
        elif current_widget == MainWidget.RULES:
            return self._rules

    def widget_to_enum(self) -> "MainWidget":
        """Возвращает enum MainWidget, соответсвующий текущему QWidget"""
        if self._stacked_widget.currentWidget() == self._rules:
            return MainWidget.RULES
        elif self._stacked_widget.currentWidget() == self.solver:
            return MainWidget.SOLVER
        elif self._stacked_widget.currentWidget() == self.play:
            return MainWidget.PLAY
        else:
            return MainWidget.MAIN

    def closeEvent(self, event: QCloseEvent | None) -> None:
        """Сохраняет состояние при выходе"""
        try:
            state = AppState(self)
            with open("../../saved_data.pickle", "wb") as file:
                pickle.dump(state, file)
        except Exception as e:
            print("Не возможно сохранить. ", str(e))

        if event:
            event.accept()


class AppState:
    """Содержит нужную информацию о MainWindow для ее сохранения"""

    def __init__(self, main: MainWindow):
        self.solver_state: MenuState = main.solver.get_state()
        self.play_state: MenuState = main.play.get_state()
        self.current_widget: MainWidget = main.widget_to_enum()


class MainWidget(IntEnum):
    """Определяет окно класса MainWindow"""

    MAIN = 0
    SOLVER = 1
    PLAY = 2
    RULES = 3


def start() -> None:
    """Запускает программу"""
    app = QApplication([])
    configure_app(app)
    window = MainWindow()
    window.show()
    app.exec()


def configure_app(app: QApplication) -> None:
    """Конфигурирует внешний вид программы"""
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
            padding: 0px 0px;
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
        background-color: 171d25;
        color: 9ba2aa;
        }
    """
    )


if __name__ == "__main__":
    start()
