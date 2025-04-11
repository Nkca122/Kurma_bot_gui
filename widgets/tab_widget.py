from PySide6.QtWidgets import (
    QTabWidget,
    QMenuBar,
    QInputDialog,
    QPushButton,
    QWidgetAction,
    QMenu,
)

from PySide6.QtGui import QAction
from PySide6.QtMultimedia import QMediaDevices
from tabs.tab import Tab
from tabs.model_tab import ModelTab


class TabWidget(QTabWidget):
    def menubar(self):
        menubar = QMenuBar()
        menubar.setStyleSheet(
            """
    QMenuBar {
        background-color: #1e1e1e;
        padding: 6px 12px;
        color: #f0f0f0;
        font-size: 12px;
        font-weight: 500;
    }

    QMenuBar::item {
        background: transparent;
        padding: 6px 12px;
        margin: 0 4px;
        border-radius: 6px;
    }

    QMenuBar::item:selected {
        background-color: #2a2a2a;
    }

    QMenu {
        background-color: #232323;
        color: #f0f0f0;
        border: 1px solid #3a3a3a;
        font-size: 13px;
    }

    QMenu::item {
        padding: 6px 18px;
        border-radius: 4px;
    }

    QMenu::item:selected {
        background-color: #3a3a3a;
    }

    QPushButton {
        background-color: #303030;
        color: #ffffff;
        border: 1px solid #555;
        padding: 6px 16px;
        border-radius: 8px;
        font-size: 13px;
    }

    QPushButton:hover {
        background-color: #3e3e3e;
        border: 1px solid #777;
    }
    """
        )

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
            Tab.shared_camera_manager.set_camera(device)

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

        self.setStyleSheet(
            """
    QTabWidget::pane {
        border: none;
        background-color: #121212;
    }

    QTabBar {
        qproperty-drawBase: 0;
        background-color: #1e1e1e;
        padding: 4px 8px;
    }

    QTabBar::tab {
        background-color: #2a2a2a;
        color: #cccccc;
        padding: 6px 14px;
        margin-right: 4px;
        border-top-left-radius: 10px;
        border-top-right-radius: 10px;
        font-weight: normal;
        font-size: 12px;
        min-width: 80px;
    }

    QTabBar::tab:selected {
        background-color: #3a3a3a;
        color: #ffffff;
    }

    QTabBar::tab:hover {
        background-color: #444444;
    }

    QTabBar::close-button {
        image: url(./assets/close.svg);
        subcontrol-position: left;
        padding: 1px;
        margin-left: 4px;
        background-color: #ff4444;
        border-radius: 4px;
    }

    QTabBar::close-button:hover {
        background-color: #ff0000;
        
    }
"""
        )

        self.addTab(ModelTab("Untitled Tab (0)"), "Untitled Tab (0)")
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
        self.addTab(ModelTab(title), title)

    def __remove_tab(self, index):
        self.removeTab(index)

    def __generate_unique_tab_title(self, base_title: str) -> str:
        base_title = base_title.strip() or "Untitled Tab"
        if base_title not in self.__tab_names:
            self.__tab_names[base_title] = [f"{base_title} (0)"]
            return f"{base_title} (0)"
        existing_titles = self.__tab_names[base_title]
        used_indices = {int(title.rsplit("(", 1)[-1][:-1]) for title in existing_titles}
        new_index = next(
            i for i in range(len(used_indices) + 1) if i not in used_indices
        )
        new_title = f"{base_title} ({new_index})"
        self.__tab_names[base_title].append(new_title)
        return new_title

    def getSelectedTab(self):
        return self.currentIndex()
