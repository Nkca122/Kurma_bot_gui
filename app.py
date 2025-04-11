from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QIcon
import sys

from widgets.toolbar import ToolBar
from widgets.tab_widget import TabWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fasal Guru")
        self.setGeometry(0, 0, 1200, 1000)
        self.addToolBar(ToolBar(self))
        self.setCentralWidget(TabWidget())

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()