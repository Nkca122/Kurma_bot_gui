from PySide6.QtWidgets import QToolBar, QLineEdit, QFileDialog, QMessageBox, QWidget
from PySide6.QtGui import QAction, QIcon, QPixmap, QImage, QDesktopServices
from PySide6.QtCore import Qt, QSize
import sys
import os


class ToolBar(QToolBar):
    def __init__(self, main_window):
        super().__init__()

        self.MainWindow = main_window
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.setIconSize(QSize(24, 24))
        self.setMovable(False)

        # Actions
        self.__screenshot()
        self.__version()
        self.__info()

    def __get_icon(self, icon_path):
        if hasattr(sys, "_MEIPASS"):  # Running as an .exe
            icon_path = os.path.join(sys._MEIPASS, icon_path)
        else:  # Running in normal Python
            icon_path = os.path.abspath(icon_path)

        icon_path = icon_path.replace("\\", "/")
        if not os.path.exists(icon_path):
            return None
        return QIcon(icon_path)

    def __screenshot_action(self):
        tab_widget = self.MainWindow.centralWidget()  # Assuming it's a QTabWidget
        selected_index = tab_widget.getSelectedTab()

        # Check if selected_index is valid
        if not isinstance(selected_index, int) or selected_index < 0 or selected_index >= tab_widget.count():
            QMessageBox.warning(
                self.MainWindow,
                "Desktop",
                "GUI:\n"
                "Unable to find selected tab, please select a tab to use this feature.\n\n"
                "© 2025",
                QMessageBox.Ok
            )
            return

        # Get the actual widget from the tab index
        selected_tab = tab_widget.widget(selected_index)
        screenshot_bitmap = QPixmap(selected_tab.size())
        selected_tab.render(screenshot_bitmap)

        # Ask the user where to save
        save_path, _ = QFileDialog.getSaveFileName(
            self.MainWindow,
            "Save Screenshot",
            "screenshot.png",
            "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)",
        )

        if save_path:
            if not screenshot_bitmap.save(save_path):
                QMessageBox.critical(self.MainWindow, "Error", "Failed to save screenshot!")

    def __version_action(self):
        QMessageBox.information(
            self.MainWindow,
            "Version Information",
            "Fasal Guru:\n"
            "This is version 1.0.0 of the Fasal Guru Desktop Application\n"
            "Release Date: 18/03/2025 \n"
            "© 2025 ",
        )

    def __info_action(self):
        url = "https://github.com/FasalGuru"
        QDesktopServices.openUrl(url)

    def __screenshot(self):
        ss_action = QAction(self.__get_icon("./assets/screenshot.png"), "", self)
        ss_action.triggered.connect(self.__screenshot_action)
        self.addAction(ss_action)

    def __version(self):
        version_action = QAction(self.__get_icon("./assets/version.png"), "", self)
        version_action.triggered.connect(self.__version_action)
        self.addAction(version_action)

    def __info(self):
        info_action = QAction(self.__get_icon("./assets/information.png"), "", self)
        info_action.triggered.connect(self.__info_action)
        self.addAction(info_action)
