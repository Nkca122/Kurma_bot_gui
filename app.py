from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QMenuBar, QToolBar, QTabWidget, QComboBox, QWidgetAction
from PySide6.QtMultimedia import QMediaDevices
from PySide6.QtGui import QIcon, QAction, QPixmap
from PySide6.QtCore import Qt, QTimer

from datetime import datetime
import sys
import os
import cv2

sys.path.append(os.path.abspath("./tabs"))
from tab import Tab

class CameraList(QComboBox):
    def __init__(self):
        super().__init__()

class TabWidget(QTabWidget):
    def __update_camera_list(self):
        video_inputs = QMediaDevices.videoInputs()
        cams = [(i, cam.description()) for i, cam in enumerate(video_inputs)]
        self.camera_selection.clear()
        for cam in cams:
            self.camera_selection.addItem(cam[1])

        if self.camera_selection.count() > 0:
            self.__change_camera(0)

    def __create_camera_menu(self, camera_menu):
        self.camera_selection = QComboBox(self)
        video_inputs = QMediaDevices.videoInputs()
        cams = [(i, cam.description()) for i, cam in enumerate(video_inputs)]
        for cam in cams:
            self.camera_selection.addItem(cam[1])
        self.camera_selection.setCurrentIndex(0)  # Default camera
        # Create a QWidgetAction to add the QComboBox to the menu
        camera_selection_action = QWidgetAction(self)
        camera_selection_action.setDefaultWidget(self.camera_selection)
        # Set the first camera as active
        self.__change_camera(0)
        # Update camera selection
        self.camera_selection.currentIndexChanged.connect(self.__change_camera)
        camera_menu.addAction(camera_selection_action)

    def selectedTab(self):
        return self.currentIndex()

    def __delete_current_tab(self):
        index = self.selectedTab()
        self.__deleteTab(index)

    def __change_camera(self, idx):
        Tab.cap = cv2.VideoCapture(idx)
    
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

        # Camera Menu
        camera_menu = menubar.addMenu("Camera")
        self.__create_camera_menu(camera_menu)

        tab_menu.addAction(create_tab)
        tab_menu.addAction(delete_tab)

        return menubar
    def __init__(self):
        super().__init__()
        self.setTabsClosable(True)
        self.setMovable(True)
        self.tabCloseRequested.connect(self.__deleteTab)
        self.addTab(Tab("New Tab"), "New Tab")

        self.camera_refresh_timer = QTimer(self)
        self.camera_refresh_timer.timeout.connect(self.__update_camera_list)
        self.camera_refresh_timer.start(3000)  # Refresh every 3 seconds

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
        self.camera_selection = None
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
