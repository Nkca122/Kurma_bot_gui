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

class Tab(QWidget):
    cap = cv2.VideoCapture(0)

    # def __change_camera(self, idx):
    #     Tab.cap = cv2.VideoCapture(idx)
    
    # def __get_all_cameras(self):
    #     cameras = QMediaDevices.videoInputs()
    #     return [(i, cam.description()) for i, cam in enumerate(cameras)]

    # def __menubar(self):
        # menubar = QMenuBar()

        # camera_selection = QComboBox()
        # cameras = self.__get_all_cameras()
        # for cam in cameras:
        #     camera_selection.addItem(cam[1])
        
        # if camera_selection.children():
        #     camera_selection.setCurrentIndex(0)
        
        # camera_selection_action = QWidgetAction(self)
        # camera_selection_action.setDefaultWidget(camera_selection)
        # camera_selection.currentIndexChanged.connect(self.__change_camera)

        # menubar.addAction(camera_selection_action)

        # self.layout.setMenuBar(menubar)
    def __init__(self, title):
        super().__init__()
        self.title = title
        self.layout = QVBoxLayout()

        # Add mode selector local vs wifi connectivity ( Later )

        self.image = Image()
        self.result = Image()
        image_layout = QHBoxLayout()

        image_layout.addWidget(self.image)
        image_layout.addWidget(self.result)

        self.mode_selector = ModeSelect(["None", "Detection", "Segmentation", "Pose Detection"])

        self.layout.addLayout(image_layout)
        self.layout.addWidget(self.mode_selector)

        self.setLayout(self.layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(30)

        self.detector = Detector()

    def update(self):
        
        if Tab.cap.isOpened():
            ret, frame = Tab.cap.read()
            if ret:
                self.image.display(frame, "Local Feed")
                mode = self.mode_selector.get_selected_mode()
                if mode == None: 
                    mode = "none"
                res_frame, res = self.detector.predict(frame, mode)
                self.result.display(res_frame, "Result")


                


        

        

