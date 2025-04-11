from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QToolBar,
)
from PySide6.QtGui import QIcon, QAction, QPixmap, QImage
from PySide6.QtCore import Qt


from datetime import datetime
import sys
import os

sys.path.append(os.path.abspath("./tabs"))
sys.path.append(os.path.abspath("./widgets"))

from tab import Tab
from tab_widget import TabWidget

vw = 800
vh = 600


class MainWindow(QMainWindow):
    def take_screenshot(self):
        screenshot_bit_map = QPixmap(self.size())
        self.__tab_widget.currentWidget().render(screenshot_bit_map)

        save_path = f"./screenshots/{str(datetime.now())}.png"
        screenshot_bit_map.save(save_path)

    def __screenshot_action_btn(self):
        screenshot = QAction(QIcon("./assets/screenshot_icon.jpeg"), "Screenshot", self)
        screenshot.triggered.connect(self.take_screenshot)

        return screenshot

    def __toolbar(self):
        toolbar = QToolBar("Main Window", self)

        # Take Screenshot

        toolbar.setMovable(False)
        toolbar.setStyleSheet(
            """
            QToolBar {
                padding: 8px;
                background: #000000;
                color: #ffffff;
            }

            QToolBar QToolButton {
                background: #000000;
                border: 1px solid black;
                border-radius: 4px;
            }

            QToolBar QToolButton:hover {
                background: #000000;
                border: 1px solid white;
                border-radius: 4px;
            }

            QToolBar QToolTip {
                background: #000000;
                border-radius: 0px;
                border: none;
                padding: 8px;
            }
        """
        )
        toolbar.addAction(self.__screenshot_action_btn())
        # Finish Toolbar
        self.addToolBar(toolbar)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("kurma bot GUI")
        self.setGeometry(0, 0, vw, vh)

        self.setStyleSheet(
            """
            QMenuBar {
                background-color: black;
                color: white;
            }

            QMenuBar::item:selected {
                background-color: gray;
            }
            """
        )

        # Addition of toolbar
        self.__toolbar()
        # Display Tabs
        self.__tab_widget = TabWidget()
        self.setMenuBar(self.__tab_widget.menubar())
        self.setCentralWidget(self.__tab_widget)


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()


if __name__ == "__main__":
    main()
