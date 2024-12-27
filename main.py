from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QPushButton,
    QSlider,
    QFileDialog,
    QWidget,
    QHBoxLayout,
    QStatusBar,
)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl


class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Мой маленький плеер")
        self.setGeometry(500, 100, 1000, 800)
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_widget = QVideoWidget()
        self.play_button = QPushButton("ПУСК")
        self.stop_button = QPushButton("СТОП")
        self.open_button = QPushButton("ОТКРЫТЬ")
        self.mute_button = QPushButton("Без звука")
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setRange(0, 0)
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        control_layout_1 = QHBoxLayout()
        control_layout_1.addWidget(self.play_button)
        control_layout_1.addWidget(self.stop_button)
        control_layout_1.addWidget(self.open_button)

        control_layout_2 = QHBoxLayout()
        control_layout_2.addWidget(self.mute_button)
        control_layout_2.addWidget(self.volume_slider)

        control_layout_3 = QHBoxLayout()
        control_layout_3.addWidget(self.position_slider)

        layout = QVBoxLayout()
        layout.addWidget(self.video_widget)
        layout.addLayout(control_layout_1)
        layout.addLayout(control_layout_2)
        layout.addLayout(control_layout_3)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.media_player.setVideoOutput(self.video_widget)

        self.play_button.clicked.connect(self.switch_play)
        self.stop_button.clicked.connect(self.stop)
        self.open_button.clicked.connect(self.open_file)
        self.mute_button.clicked.connect(self.switch_mute)
        self.volume_slider.valueChanged.connect(self.volume)
        self.position_slider.sliderMoved.connect(self.set_position)
        self.media_player.positionChanged.connect(self.update_position)
        self.media_player.durationChanged.connect(self.update_duration)
        self.media_player.stateChanged.connect(self.update_buttons)

        self.is_muted = False

    def switch_play(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def stop(self):
        self.media_player.stop()

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Открыть видеофайлы", "", "(*.mp4 *.avi *.mkv)"
        )
        if file_name:
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_name)))
            self.media_player.play()
            self.status_bar.showMessage(f"Проигрывание: {file_name}")

    def set_position(self, position):
        self.media_player.setPosition(position)

    def update_position(self, position):
        self.position_slider.setValue(position)

    def update_duration(self, duration):
        self.position_slider.setRange(0, duration)

    def update_buttons(self, state):
        if state == QMediaPlayer.PlayingState:
            self.play_button.setText("ПАУЗА")
        else:
            self.play_button.setText("СТАРТ")

    def switch_mute(self):
        self.is_muted = not self.is_muted
        self.media_player.setMuted(self.is_muted)
        if self.is_muted:
            self.mute_button.setText("Включить звук")
        else:
            self.mute_button.setText("Без звука")

    def volume(self, volume):
        self.media_player.setVolume(volume)


if __name__ == "__main__":
    app = QApplication([])
    player = VideoPlayer()
    player.show()
    app.exec_()
