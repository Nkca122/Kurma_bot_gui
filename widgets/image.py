from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt


class Image(QWidget):
    def __init__(self):
        super().__init__()
        self.__layout = QVBoxLayout()
        self.__layout.setContentsMargins(8, 8, 8, 8)
        self.__layout.setSpacing(4)

        # Title Label
        self.__title_label = QLabel()
        self.__title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.__title_label.setStyleSheet(
            """
            QLabel {
                font-size: 13px;
                font-weight: 500;
                color: #cccccc;
                padding-left: 4px;
            }
        """
        )

        # Image Label
        self.__image_label = QLabel()
        self.__image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__image_label.setMinimumSize(320, 240)
        self.__image_label.setScaledContents(True)
        self.__image_label.setStyleSheet(
            """
            QLabel {
                background-color: #1e1e1e;
                border-radius: 8px;
            }
            QLabel:hover {
                border: 1px solid #7aa9ff;
            }
        """
        )

        # Assemble layout
        self.__layout.addWidget(self.__title_label)
        self.__layout.addWidget(self.__image_label)
        self.__layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.__layout)

        # Outer widget style
        self.setStyleSheet(
            """
            QWidget {
                background-color: transparent;
                border-radius: 8px;
            }
        """
        )

    def display(self, frame, title="Untitled"):
        # Convert OpenCV frame to QImage
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        qImg = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_BGR888)

        # Set image
        self.__image_label.setPixmap(QPixmap.fromImage(qImg))

        # Set title
        self.__title_label.setText(title)
