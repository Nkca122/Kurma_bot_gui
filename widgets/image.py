from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt

class Image(QWidget):
    def __init__(self):
        super().__init__()
        self.__layout = QVBoxLayout()
        self.__layout.setContentsMargins(10, 10, 10, 10)
        self.__layout.setSpacing(6)

        # Title Label
        self.__title_label = QLabel()
        self.__title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__title_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: 600;
                color: #333333;
            }
        """)

        # Image Label
        self.__image_label = QLabel()
        self.__image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__image_label.setStyleSheet("""
            QLabel {
                border: 2px solid #cccccc;
                border-radius: 12px;
                background-color: #ffffff;
            }
            QLabel:hover {
                border: 2px solid #7aa9ff;
                background-color: #f8faff;
            }
        """)
        self.__image_label.setMinimumSize(320, 240)
        self.__image_label.setScaledContents(True)

        # Assemble layout
        self.__layout.addWidget(self.__title_label)
        self.__layout.addWidget(self.__image_label)
        self.__layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.__layout)

        # Outer style for widget
        self.setStyleSheet("""
            QWidget {
                background-color: transparent;
                border-radius: 10px;
            }
        """)

    def display(self, frame, title="Untitled"):
        # Convert OpenCV frame to QImage
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        qImg = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_BGR888)

        # Set image
        self.__image_label.setPixmap(QPixmap.fromImage(qImg))

        # Set title
        self.__title_label.setText(title)
