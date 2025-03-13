from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QToolBar
from PySide6.QtGui import QIcon, QAction


from datetime import datetime
import sys
import os

sys.path.append(os.path.abspath("./tabs"))
sys.path.append(os.path.abspath("./widgets"))

from tab import Tab
from tab_widget import TabWidget




class MainWindow(QMainWindow):
    def __toolbar(self):
        toolbar = QToolBar("", self)

        
        # Take Screenshot
        screenshot = QAction(QIcon(), "Screenshot", self)
        screenshot.triggered.connect(self.take_screenshot)

        toolbar.setMovable(False)
        toolbar.setStyleSheet(
            """
            QToolBar {
                padding: 16px;
                background: #e3e3e3;
            }

            QToolBar QToolButton { /* Ensure it applies only to buttons inside the toolbar */
                background: #ff0000;
                border: 1px solid black; /* Ensure visible edges */
                padding: 5px;
                border-radius: 4px;
            }

            QToolBar QToolButton:hover {
                background: #00ff00;
            }

            QToolBar QToolButton:pressed {
                background: #0000ff;
            }
        """
        )

        toolbar.addAction(screenshot)

        # Finish Toolbar
        self.addToolBar(toolbar)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("KURMA BOT GUI")
        self.setGeometry(0, 0, 800, 600)

        # Addition of toolbar
        self.__toolbar()
        # Display Tabs
        self.tab_widget = TabWidget()
        self.setMenuBar(self.tab_widget.menubar())
        self.setCentralWidget(self.tab_widget)

    def take_screenshot(self):
        screenshot_bit_map = QPixmap(self.size())
        self.tab_widget.render(screenshot_bit_map)

        save_path = f"./screenshots/{str(datetime.now()).replace(" ", "_").replace(":", "_").replace(".", "_")}.png"
        screenshot_bit_map.save(save_path)


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()


if __name__ == "__main__":
    main()
