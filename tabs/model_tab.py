from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QSizePolicy,
)
from PySide6.QtCore import Slot
from PySide6.QtGui import QImage
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import cv2

from widgets.image import Image
from widgets.mode_select import ModeSelect
from widgets.controls import Controller
from utils.detector import Detector
from tabs.tab import Tab


class ModelTab(Tab):
    def __init__(self, title):
        super().__init__()
        self.title = title
        self.detector = None
        self.processing = False
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.closed = False

        self._apply_theme()

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(10, 10, 10, 10)

        # Image display
        self.image = Image()
        self.result = Image()
        for widget in (self.image, self.result):
            widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            widget.setStyleSheet("border-radius: 10px; background-color: #1e1e1e;")

        image_layout = QHBoxLayout()
        image_layout.setSpacing(10)
        image_layout.addWidget(self.image)
        image_layout.addWidget(self.result)

        image_group = QGroupBox()
        image_group.setLayout(image_layout)
        image_group.setStyleSheet("border: none;")

        # Controls
        self.mode_selector = ModeSelect(
            ["None", "Detection", "Segmentation", "Pose Detection"]
        )
        self.controller = Controller()

        for widget in (self.controller, self.mode_selector):
            widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        control_layout = QHBoxLayout()
        control_layout.setSpacing(10)
        control_layout.addWidget(self.mode_selector)
        control_layout.addWidget(self.controller)

        control_group = QGroupBox()
        control_group.setLayout(control_layout)
        control_group.setStyleSheet("border: none;")

        self.layout.addWidget(image_group)
        self.layout.addWidget(control_group)

        # Camera
        self.camera_manager.frame_ready.connect(self.process_frame)

        self.update_result_signal.connect(self._update_result_image)
        self.frame_count = 0
        self.process_every_nth_frame = 2

    def threaded_predict(self, frame_np, mode):
        if self.processing or self.closed:
            return
        self.processing = True

        if self.detector is None:
            self.detector = Detector()

        def run():
            try:
                resized_frame = cv2.resize(frame_np, (320, 240))
                res_frame, _ = self.detector.predict(resized_frame, mode)
                res_frame = cv2.resize(
                    res_frame, (frame_np.shape[1], frame_np.shape[0])
                )
                if not self.closed:
                    self.update_result_signal.emit(res_frame)
            except Exception as e:
                print("Threaded detection error:", e)
            finally:
                self.processing = False

        self.executor.submit(run)

    @Slot(np.ndarray)
    def _update_result_image(self, result_frame):
        self.result.display(result_frame, "Result")

    @Slot("QVideoFrame")
    def process_frame(self, frame):
        if self.closed or not frame.isValid():
            return

        self.frame_count += 1
        if self.frame_count % self.process_every_nth_frame != 0:
            return

        img = frame.toImage().convertToFormat(QImage.Format.Format_BGR888)
        width = img.width()
        height = img.height()
        bytes_per_line = img.bytesPerLine()

        ptr = img.bits()
        arr = bytes(ptr)
        frame_np = (
            np.frombuffer(arr, dtype=np.uint8)
            .reshape((height, bytes_per_line // 3, 3))[:, :width]
            .copy()
        )

        self.image.display(frame_np, "Local Feed")

        mode = (self.mode_selector.get_selected_mode() or "none").lower()
        if mode == "none":
            self.update_result_signal.emit(frame_np)
        else:
            self.threaded_predict(frame_np, mode)

    def toggle_dark_mode(self, enabled):
        if enabled:
            self._apply_theme()
        else:
            self._apply_light_theme()

    def _apply_theme(self):
        self.setStyleSheet(
            """
            QWidget {
                font-family: 'Segoe UI';
                background-color: #121212;
                color: #e0e0e0;
                border: none;
            }
            QGroupBox {
                border: none;
            }
            QLabel, QPushButton, QComboBox {
                font-size: 14px;
                background: transparent;
                border: none;
            }
            QComboBox {
                padding: 6px 10px;
                border-radius: 8px;
                background-color: #2a2a2a;
            }
            QPushButton {
                padding: 6px 12px;
                border-radius: 8px;
                background-color: #2d2d2d;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
            }
            QCheckBox {
                padding: 4px;
            }
            """
        )


    def closeEvent(self, event):
        self.closed = True
        self.executor.shutdown(wait=False)
        super().closeEvent(event)
