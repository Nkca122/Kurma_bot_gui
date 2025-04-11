from PySide6.QtWidgets import (
    QTabWidget, QMenuBar, QInputDialog, QPushButton,
    QWidgetAction, QMenu
)

from PySide6.QtGui import QAction
from PySide6.QtMultimedia import QMediaDevices
from tabs.tab import Tab


class TabWidget(QTabWidget):
    def menubar(self):
        menubar = QMenuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #1e1e1e;
                padding: 6px 12px;
                color: #f0f0f0;
                font-size: 15px;
                font-weight: bold;
            }
            QMenuBar::item {
                background: transparent;
                padding: 4px 10px;
                margin: 0 4px;
            }
            QMenuBar::item:selected {
                background: #2d2d2d;
                border-radius: 6px;
            }
            QMenu {
                background-color: #1e1e1e;
                color: #f0f0f0;
                border: 1px solid #3a3a3a;
            }
            QMenu::item {
                padding: 6px 20px;
            }
            QMenu::item:selected {
                background-color: #3a3a3a;
            }
            QPushButton {
                background-color: #282828;
                color: #ffffff;
                border: 1px solid #555;
                padding: 4px 12px;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #444;
            }
        """)

        # Tabs Menu
        tab_menu = menubar.addMenu("Tabs")

        create_tab_action = QAction("Create New Tab", self)
        create_tab_action.setShortcut("Ctrl+Shift+N")
        create_tab_action.triggered.connect(self.__create_tab_action_fn)

        delete_tab_action = QAction("Delete Current Tab", self)
        delete_tab_action.setShortcut("Ctrl+Shift+Del")
        delete_tab_action.triggered.connect(
            lambda: self.__delete_tab_action_fn(self.currentIndex())
        )

        tab_menu.addAction(create_tab_action)
        tab_menu.addAction(delete_tab_action)

        # Camera Menu
        camera_menu = menubar.addMenu("Camera")
        self.camera_actions = []

        def update_camera(device):
            self.widget[self.getSelectedTab()].shared_camera_manager.set_camera(device)

        for device in QMediaDevices.videoInputs():
            action = QAction(device.description(), self)
            action.triggered.connect(lambda checked=False, d=device: update_camera(d))
            camera_menu.addAction(action)
            self.camera_actions.append(action)

        # Add quick create button
        create_tab_button = QPushButton("➕ New Tab")
        create_tab_button.clicked.connect(self.__create_tab_action_fn)

        create_tab_widget_action = QWidgetAction(self)
        create_tab_widget_action.setDefaultWidget(create_tab_button)
        menubar.addAction(create_tab_widget_action)

        return menubar

    def __init__(self):
        super().__init__()
        self.__tab_names = {"Untitled Tab": ["Untitled Tab (0)"]}
        self.setTabsClosable(True)
        self.setMovable(True)

        self.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: #121212;
            }
            QTabBar::tab {
                background-color: #2c2c2c;
                color: #ddd;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: 600;
                font-size: 14px;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
                color: #1a1a1a;
            }
            QTabBar::tab:hover {
                background-color: #444;
            }
        """)

        self.addTab(Tab("Untitled Tab (0)"), "Untitled Tab (0)")
        self.tabCloseRequested.connect(self.__delete_tab_action_fn)

    def __create_tab_action_fn(self):
        title_input, confirmed = QInputDialog.getText(
            self, "Fasal Guru", "Enter a name for the new tab:"
        )
        if confirmed:
            tab_title = self.__generate_unique_tab_title(title_input)
            self.__create_tab(tab_title)

    def __delete_tab_action_fn(self, index):
        if index < 0:
            return
        tab_label = self.tabText(index)
        base_title = tab_label.rsplit(" (", 1)[0]
        self.__tab_names[base_title].remove(tab_label)
        if not self.__tab_names[base_title]:
            del self.__tab_names[base_title]
        self.__remove_tab(index)

    def __create_tab(self, title):
        self.addTab(Tab(title), title)

    def __remove_tab(self, index):
        self.removeTab(index)

    def __generate_unique_tab_title(self, base_title: str) -> str:
        base_title = base_title.strip() or "Untitled Tab"
        if base_title not in self.__tab_names:
            self.__tab_names[base_title] = [f"{base_title} (0)"]
            return f"{base_title} (0)"
        existing_titles = self.__tab_names[base_title]
        used_indices = {int(title.rsplit("(", 1)[-1][:-1]) for title in existing_titles}
        new_index = next(i for i in range(len(used_indices) + 1) if i not in used_indices)
        new_title = f"{base_title} ({new_index})"
        self.__tab_names[base_title].append(new_title)
        return new_title

    def getSelectedTab(self):
        return self.currentIndex()
