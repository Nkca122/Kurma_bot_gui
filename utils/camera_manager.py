from PySide6.QtMultimedia import (
    QMediaCaptureSession,
    QMediaDevices,
    QCamera,
    QVideoSink
)
from PySide6.QtCore import QObject, Signal


class CameraManager(QObject):
    frame_ready = Signal(object)

    def __init__(self):
        super().__init__()
        self.capture_session = QMediaCaptureSession()
        self.video_sink = QVideoSink()
        self.capture_session.setVideoSink(self.video_sink)
        self.video_sink.videoFrameChanged.connect(self.__on_frame)

        default_camera = QMediaDevices.videoInputs()[0] if QMediaDevices.videoInputs() else None
        self.camera = None
        if default_camera:
            self.set_camera(default_camera)

    def set_camera(self, camera_device):
        if self.camera:
            self.camera.stop()
            self.camera.deleteLater()
        self.camera = QCamera(camera_device)
        self.capture_session.setCamera(self.camera)
        self.camera.start()

    def __on_frame(self, frame):
        if frame and frame.isValid():
            self.frame_ready.emit(frame)
