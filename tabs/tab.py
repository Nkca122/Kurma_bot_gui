from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal
from utils.camera_manager import CameraManager

import numpy as np

class Tab(QWidget):
    update_result_signal = Signal(np.ndarray)
    camera_manager = CameraManager()
    def __init__(self):
        super().__init__()
