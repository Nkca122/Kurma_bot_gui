from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt
import sys

from widgets.toolbar import ToolBar
from widgets.tab_widget import TabWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KURMA BOT")
        self.setGeometry(0, 0, 1200, 1000)
        self.setWindowFlags(Qt.WindowType.Window)
        self.setStyleSheet(self.__get_style())

        self.addToolBar(ToolBar(self))
        self.setCentralWidget(TabWidget())
        self.setMenuBar(self.centralWidget().menubar())

    def __get_style(self):
        return """
        QMainWindow {
            background-color: #1a1a1a;
        }

        QToolBar {
            background-color: #1e1e1e;
            spacing: 6px;
            padding: 6px;
            border-bottom: 1px solid #333;
        }

        QToolButton {
            background-color: #2c2c2c;
            color: #fff;
            padding: 6px 10px;
            border-radius: 6px;
            font-size: 14px;
        }

        QToolButton:hover {
            background-color: #444;
        }

        QStatusBar {
            background-color: #1e1e1e;
            color: #aaa;
        }
        """

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
