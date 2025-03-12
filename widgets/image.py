from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt

class Image(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        # Title Label
        self.title_label = QLabel()
        # Image Label to display the cv2 frame
        self.image_label = QLabel()

        # Creation of Widget
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.image_label)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.layout)
    
    def display(self, frame, title):
        # Frame Processing
        h, w, ch = frame.shape
        bytes_per_line = ch*w
        qImg = QImage(frame.data, w, h, bytes_per_line, QImage.Format_BGR888)

        # Image Label
        self.image_label.setMaximumSize(w, h)
        self.image_label.setPixmap(QPixmap.fromImage(qImg))

        # Title Label
        self.title_label.setText(title)
