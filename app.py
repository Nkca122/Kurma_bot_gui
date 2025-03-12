from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QMenuBar, QToolBar, QTabWidget
from PySide6.QtGui import QIcon, QAction, QPixmap
from PySide6.QtCore import Qt

from datetime import datetime
import sys
import os

sys.path.append(os.path.abspath("./tabs"))
from tab import Tab

class TabWidget(QTabWidget):
    def selectedTab(self):
        return self.currentIndex()

    def __delete_current_tab(self):
        index = self.selectedTab()
        self.__deleteTab(index)
    
    def menubar(self):
        # Menu Bar
        menubar = QMenuBar()
        # Tab Menu
        tab_menu = menubar.addMenu("Tabs")

        # Create Tab
        create_tab = QAction("Create a New Tab", self)
        create_tab.triggered.connect(self.__createTab)
        create_tab.setShortcut("Ctrl+Shift+N")

        # Delete Tab
        delete_tab = QAction("Delete Tab", self)
        delete_tab.triggered.connect(self.__delete_current_tab)
        delete_tab.setShortcut("Ctrl+Shift+del")

        tab_menu.addAction(create_tab)
        tab_menu.addAction(delete_tab)

        return menubar
    def __init__(self):
        super().__init__()
        self.setTabsClosable(True)
        self.setMovable(True)
        self.tabCloseRequested.connect(self.__deleteTab)
        self.addTab(Tab("New Tab"), "New Tab")

    def __createTab(self):
        self.addTab(Tab("New Tab"), "New Tab")
    
    def __deleteTab(self, index):
        self.removeTab(index)

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
    app = QApplication()
    win = MainWindow()
    win.show()
    app.exec()


if __name__ == "__main__":
    main()
