from PySide6.QtWidgets import QTabWidget, QMenuBar, QInputDialog
from PySide6.QtGui import QAction
import sys
import os

sys.path.append(os.path.abspath("./tabs"))
from tab import Tab


class TabWidget(QTabWidget):
    def __create_tab_action_fn(self):
        input, status = QInputDialog.getText(
            self, "kurma bot GUI", "Enter the name for the new tab"
        )
        if status:
            title = self.__manage_tab_titles(input)
            self.__createTab(title)

    def __delete_tab_action_fn(self, index):
        tab_counted_title = self.tabText(index)
        tab_title_key = tab_counted_title[:-4]

        self.__tab_names[tab_title_key].remove(tab_counted_title)
        self.__tab_names[tab_title_key].sort()
        self.__deleteTab(index)

    def __createTab(self, title):
        self.addTab(Tab(title), title)

    def __deleteTab(self, index):
        self.removeTab(index)

    def __manage_tab_titles(self, title):
        res = None
        if not title:
            res = "Untitled Tab"
        else:
            res = title

        uncounted_res = res

        if uncounted_res in self.__tab_names.keys():
            missing_ct = None
            for i, tab in enumerate(self.__tab_names[uncounted_res]):
                print(f"{tab}, {i}")
                if tab != f"{uncounted_res} ({i})":
                    missing_ct = i
                    break

            if missing_ct == None:
                missing_ct = len(self.__tab_names[res])

            res = f"{res} ({missing_ct})"
            print(res)
            self.__tab_names[uncounted_res].append(res)
            self.__tab_names[uncounted_res].sort()
        else:
            res = f"{res} ({0})"
            self.__tab_names[uncounted_res] = [res]

        print(self.__tab_names)
        return res

    def getSelectedTab(self):
        return self.currentIndex()

    def menubar(self):
        # Menu Bar
        menubar = QMenuBar()
        menubar.setStyleSheet(
            """
                QMenuBar {
                    background: #000000;
                    padding: 8px;
                    color: #ffffff;
                    font-size: 16px;
                    font-weight: bold;
                }
            """
        )
        # Tab Menu
        tab_menu = menubar.addMenu("Tabs")

        ## Create Tab
        create_tab = QAction("Create a New Tab", self)
        create_tab.triggered.connect(self.__create_tab_action_fn)
        create_tab.setShortcut("Ctrl+Shift+N")

        ## Delete Tab
        delete_tab = QAction("Delete Tab", self)
        delete_tab.triggered.connect(self.__delete_tab_action_fn)
        delete_tab.setShortcut("Ctrl+Shift+del")

        # Camera Menu

        tab_menu.addAction(create_tab)
        tab_menu.addAction(delete_tab)

        return menubar

    def __init__(self):
        super().__init__()
        self.__tab_names = {"Untitled Tab": ["Untitled Tab (0)"]}

        self.setTabsClosable(True)
        self.setMovable(True)

        self.setStyleSheet("""
        QTabWidget::pane { 
            border: 0.5px solid white; 
            background-color: black; 
        }

        QTabBar::tab {
            background-color: black;
            color: white;
            padding: 8px 15px;
            border: 0.5px solid white;
            border-radius: 4px 4px 0px 0px;
        }

        QTabBar::tab:selected {
            background-color: white;
            color: black;
        }

        QTabBar::tab:hover {
            background-color: gray;
        }

        QInputDialog {
            background-color: black;
            color: white;
            border: 1px solid white;
        }

        QLineEdit {
            background-color: black;
            color: white;
            border: none;
            border-bottom: 2px solid white;
            padding: 5px;
            font-size: 16px;
        }

        QDialogButtonBox {
            background-color: black;
            color: white;
        }

        QDialogButtonBox QPushButton {
            background-color: black;
            color: white;
            border: 1px solid white;
            padding: 5px 10px;
        }

        QDialogButtonBox QPushButton:hover {
            background-color: gray;
        }
        """)

        self.addTab(Tab("Untitled Tab (0)"), "Untitled Tab (0)")
        self.tabCloseRequested.connect(self.__delete_tab_action_fn)
