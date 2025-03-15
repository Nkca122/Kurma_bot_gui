from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt

class Image(QWidget):
    def __init__(self):
        super().__init__()
        self.__layout = QVBoxLayout()

        # Title Label
        self.__title_label = QLabel()
        # Image Label to display the cv2 frame
        self.__image_label = QLabel()

        # Creation of Widget
        self.__layout.addWidget(self.__title_label)
        self.__layout.addWidget(self.__image_label)
        self.__layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setStyleSheet(
        """
            QWidget QLabel::pane {
                background-color: red;
            }
        """
        )

        self.setLayout(self.__layout)
    
    def display(self, frame, title = "Untitled"):
        # Frame Processing
        h, w, ch = frame.shape
        bytes_per_line = ch*w
        qImg = QImage(frame.data, w, h, bytes_per_line, QImage.Format_BGR888)

        # Image Label
        self.__image_label.setMaximumSize(w, h)
        self.__image_label.setPixmap(QPixmap.fromImage(qImg))

        # Title Label
        self.__title_label.setText(title)
