from PySide6.QtWidgets import QMenu
from PySide6.QtMultimedia import QMediaDevices
from PySide6.QtCore import Qt, QTimer
class DeviceList(QMenu):
    def __update_camera_list(self):
        video_inputs = QMediaDevices.videoInputs()
        cams = [(i, cam.description()) for i, cam in enumerate(video_inputs)]
        self.camera_selection.clear()
        for cam in cams:
            self.camera_selection.addItem(cam[1])
    
    def __change_camera(self, idx):
        Tab.cap = cv2.VideoCapture(idx)
    

    def __init__(self):
        super().__init__()