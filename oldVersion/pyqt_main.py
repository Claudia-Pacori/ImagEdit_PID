import sys

import cv2
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QLabel,
    QMainWindow,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)


class ImageEditor(QMainWindow):
    def __init__(self):
        super(ImageEditor, self).__init__()

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setScaledContents(True)

        self.capture_button = QPushButton("Capturar desde Webcam", self)
        self.load_image_button = QPushButton("Cargar Imagen", self)
        self.load_video_button = QPushButton("Cargar Video", self)

        self.capture_image_button = QPushButton("Capturar Imagen", self)
        self.pause_button = QPushButton("Pausar", self)

        self.video_slider = QSlider(Qt.Horizontal, self)
        self.video_slider.setEnabled(False)

        self.frame = QFrame(self)
        self.layout = QVBoxLayout(self.frame)
        self.layout.addWidget(self.capture_button)
        self.layout.addWidget(self.load_image_button)
        self.layout.addWidget(self.load_video_button)
        self.layout.addWidget(self.capture_image_button)
        self.layout.addWidget(self.pause_button)
        self.layout.addWidget(self.video_slider)
        self.layout.addWidget(self.image_label)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.addWidget(self.frame)

        self.capture_button.clicked.connect(self.capture_from_webcam)
        self.load_image_button.clicked.connect(self.load_image)
        self.load_video_button.clicked.connect(self.load_video)
        self.capture_image_button.clicked.connect(self.capture_image)
        self.pause_button.clicked.connect(self.toggle_pause)
        self.video_slider.valueChanged.connect(self.update_frame_position)

        self.video_capture = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.paused = False
        self.image_captured = False

    def capture_from_webcam(self):
        self.video_capture = cv2.VideoCapture(0)
        self.timer.start(30)
        self.video_slider.setEnabled(False)

    def load_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, "Cargar Imagen", "", "Images (*.png *.jpg *.bmp)"
        )
        if file_path:
            self.video_capture = None
            self.timer.stop()
            image = cv2.imread(file_path)
            self.display_image(image)

    def load_video(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, "Cargar Video", "", "Videos (*.mp4 *.avi)"
        )
        if file_path:
            self.video_capture = cv2.VideoCapture(file_path)
            self.timer.start(30)
            self.video_slider.setEnabled(True)

    def update_frame(self):
        ret, frame = self.video_capture.read()
        if ret and not self.paused:
            frame = self.resize_image(frame)
            self.display_image(frame)
            current_frame = int(self.video_capture.get(cv2.CAP_PROP_POS_FRAMES))
            total_frames = int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
            slider_value = int(current_frame * 100 / total_frames)
            self.video_slider.setValue(slider_value)

    def display_image(self, image):
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        q_image = QImage(
            image.data, width, height, bytes_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap)

    def capture_image(self):
        if self.video_capture is not None and self.paused and not self.image_captured:
            ret, frame = self.video_capture.read()
            if ret:
                frame = self.resize_image(frame)
                cv2.imwrite("captured_image.png", frame)
                self.image_captured = True

    def toggle_pause(self):
        self.paused = not self.paused
        if not self.paused:
            self.image_captured = False

    def update_frame_position(self, value):
        if self.video_capture is not None:
            total_frames = int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
            target_frame = int(value * total_frames / 100)
            self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
            self.update_frame()

    def resize_image(self, image, max_width=800, max_height=600):
        height, width, _ = image.shape
        if width > max_width or height > max_height:
            ratio = min(max_width / width, max_height / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            resized_image = cv2.resize(image, (new_width, new_height))
            return resized_image
        return image


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = ImageEditor()
    editor.show()
    sys.exit(app.exec_())
