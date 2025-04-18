from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QMenuBar, QMenu, QComboBox, QWidgetAction
from PySide6.QtCore import QTimer
import cv2
import sys
import os

sys.path.append(os.path.abspath("./widgets"))
sys.path.append(os.path.abspath("./utils"))
from image import Image
from mode_select import ModeSelect
from detector import Detector
from controls import Controller

class Tab(QWidget):
    cap = cv2.VideoCapture(0)
    def __init__(self, title):
        super().__init__()
        self.title = title
        self.layout = QVBoxLayout()
        self.image = Image()
        self.result = Image()
        image_layout = QHBoxLayout()
        control_layout = QHBoxLayout()
        self.mode = "Local"

        image_layout.addWidget(self.image)
        image_layout.addWidget(self.result)

        self.mode_selector = ModeSelect(["None", "Detection", "Segmentation", "Pose Detection"])
        self.controller = Controller() 

        control_layout.addWidget(self.mode_selector)
        control_layout.addWidget(self.controller)

        self.layout.addLayout(image_layout)
        self.layout.addLayout(control_layout)

        self.setLayout(self.layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(30)

        self.detector = Detector()

    def update(self):
        if self.mode == "Local":
            if Tab.cap.isOpened():
                ret, frame = Tab.cap.read()
                if ret:
                    self.image.display(frame, "Local Feed")
                    mode = self.mode_selector.get_selected_mode()
                    if mode == None: 
                        mode = "none"
                    res_frame, res = self.detector.predict(frame, mode)
                    self.result.display(res_frame, "Result")


                


        

        

