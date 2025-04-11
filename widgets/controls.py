from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt


class Controller(QWidget):

    def __button_hold_action(self):
        self.command = self.sender().text()
        self.__command_label.setText(f"{self.command}")

    def __button_release_action(self):
        self.command = None
        self.__command_label.setText(f"{self.command}")

    def __controls(self):

        forward_btn = QPushButton("Forward")
        forward_btn.pressed.connect(self.__button_hold_action)
        forward_btn.released.connect(self.__button_release_action)
        self.__layout.addWidget(forward_btn, 0, 1)

        backward_btn = QPushButton("Backward")
        backward_btn.pressed.connect(self.__button_hold_action)
        backward_btn.released.connect(self.__button_release_action)
        self.__layout.addWidget(backward_btn, 2, 1)

        left_btn = QPushButton("Left")
        left_btn.pressed.connect(self.__button_hold_action)
        left_btn.released.connect(self.__button_release_action)
        self.__layout.addWidget(left_btn, 1, 0)

        right_btn = QPushButton("Right")
        right_btn.pressed.connect(self.__button_hold_action)
        right_btn.released.connect(self.__button_release_action)
        self.__layout.addWidget(right_btn, 1, 2)

        self.__layout.addWidget(self.__command_label, 1, 1)
        self.__command_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.__layout)

    def __init__(self):
        super().__init__()
        self.command = None
        self.__device = None
        self.__command_label = QLabel(f"{self.command}")
        self.__layout = QGridLayout()

        self.setStyleSheet(
            """
    QWidget {
        font-family: 'Segoe UI';
        background-color: transparent;
    }

    QPushButton {
        height: 40px;
        width: 80px;
        border: 1px solid #444;
        border-radius: 10px;
        background-color: #2e2e2e;
        color: #f0f0f0;
        font-size: 14px;
        font-weight: 500;
    }

    QPushButton:hover {
        background-color: #3a3a3a;
        border: 1px solid #666;
    }

    QLabel {
        background-color: #1a1a1a;
        color: #f0f0f0;
        font-size: 14px;
        border-radius: 6px;
        padding: 6px 12px;
        border: 1px solid #333;
        min-width: 80px;
    }
    """
        )

        self.__controls()
