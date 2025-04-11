from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QSizePolicy
from PySide6.QtMultimedia import QCamera, QMediaCaptureSession, QMediaDevices, QVideoSink
from PySide6.QtCore import QTimer, Slot, Signal
from PySide6.QtGui import QImage
import numpy as np
import cv2
import sys
import os
from threading import Thread

sys.path.append(os.path.abspath("./widgets"))
sys.path.append(os.path.abspath("./utils"))

from image import Image
from mode_select import ModeSelect
from detector import Detector
from controls import Controller


class Tab(QWidget):
    update_result_signal = Signal(np.ndarray)  # Custom signal to safely update result image

    def __init__(self, title):
        super().__init__()
        self.title = title

        self.setStyleSheet("""
            QWidget {
                background-color: #f2f2f2;
                font-family: Arial;
            }
            QGroupBox {
                border: 2px solid #999;
                border-radius: 8px;
                margin-top: 10px;
                font-weight: bold;
                background-color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                top: -7px;
                background-color: transparent;
                padding: 0 3px;
            }
        """)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(12)

        # Image previews
        self.image = Image()
        self.result = Image()
        self.image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.result.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        image_layout = QHBoxLayout()
        image_layout.setSpacing(10)
        image_layout.addWidget(self.image)
        image_layout.addWidget(self.result)

        image_group = QGroupBox("Camera Feed & Result")
        image_group.setLayout(image_layout)

        # Controls section
        self.mode_selector = ModeSelect(["None", "Detection", "Segmentation", "Pose Detection"])
        self.controller = Controller()

        control_layout = QHBoxLayout()
        control_layout.setSpacing(10)
        control_layout.addWidget(self.mode_selector)
        control_layout.addWidget(self.controller)

        control_group = QGroupBox("Controls")
        control_group.setLayout(control_layout)

        # Add groups to main layout
        self.layout.addWidget(image_group)
        self.layout.addWidget(control_group)

        # Setup detector
        self.detector = Detector()

        # Setup Qt Camera
        self.capture_session = QMediaCaptureSession()
        self.video_sink = QVideoSink()
        self.capture_session.setVideoSink(self.video_sink)
        self.video_sink.videoFrameChanged.connect(self.process_frame)

        cameras = QMediaDevices.videoInputs()
        if not cameras:
            print("No camera found!")
            return

        self.camera = QCamera(cameras[0])
        self.capture_session.setCamera(self.camera)
        self.camera.start()

        # Connect signal to display function
        self.update_result_signal.connect(self._update_result_image)

    def threaded_predict(self, frame_np, mode):
        def run():
            try:
                res_frame, _ = self.detector.predict(frame_np.copy(), mode)
                self.update_result_signal.emit(res_frame)  # Emit result frame to main thread
            except Exception as e:
                print("Threaded detection error:", e)
        Thread(target=run, daemon=True).start()

    @Slot(np.ndarray)
    def _update_result_image(self, result_frame):
        self.result.display(result_frame, "Result")

    @Slot("QVideoFrame")
    def process_frame(self, frame):
        if not frame.isValid():
            return

        img = frame.toImage().convertToFormat(QImage.Format.Format_BGR888)
        width = img.width()
        height = img.height()
        bytes_per_line = img.bytesPerLine()

        ptr = img.bits()
        arr = bytes(ptr)
        frame_np = np.frombuffer(arr, dtype=np.uint8).reshape(
            (height, bytes_per_line // 3, 3)
        )[:, :width]

        # Show original frame
        self.image.display(frame_np.copy(), "Local Feed")

        # Get selected mode and run prediction in thread
        mode = self.mode_selector.get_selected_mode().lower() or "none"
        self.threaded_predict(frame_np.copy(), mode)
