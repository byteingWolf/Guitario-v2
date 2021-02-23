import os
import threading
from pathlib import Path
from zipfile import ZipFile

import cv2
import tensorflow as tf
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRect, QSize, Qt, QUrl, pyqtSignal
from PyQt5.QtGui import QBrush, QColor, QIcon, QImage, QPalette
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QAction, QFileDialog, QHBoxLayout, QLabel,
                             QMainWindow, QMenuBar, QPushButton, QSizePolicy,
                             QVBoxLayout, QWidget)

from functions import create_onset_info, read_song
from modelPredict import model_predict
from settings import MODEL_PATH, SONG_DURATION


class MainWindow(QMainWindow):

    class EventWindow(QMainWindow):
        state = pyqtSignal(bool)

        def closeEvent(self, e):
            self.state.emit(False)

    @staticmethod
    def hhmmss(ms):
        h, r = divmod(ms, 360000) #60*60*1000 
        m, r = divmod(r, 60000) #60*1000
        s, _ = divmod(r, 1000) #1000
        return ("%02d:%02d:%02d" % (h, m, s)) if m else ("%02d:%02d" % (m, s))

    def setupUi(self, MainWindow):

        self.sizeWin = QSize(640, 360)
        self.setMinimumSize(self.sizeWin)

        self.central_widget = QWidget(MainWindow)
        size_policy = QSizePolicy(QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)

        size_policy.setHeightForWidth(
            self.central_widget.sizePolicy().hasHeightForWidth())

        self.central_widget.setSizePolicy(size_policy)

        self.horizontal_layout = QHBoxLayout(self.central_widget)
        self.horizontal_layout.setContentsMargins(11, 11, 11, 11)
        self.vertical_layout = QVBoxLayout()
        self.horizontal_layout_4 = QHBoxLayout()

        self.viewer = self.EventWindow(self)
        self.viewer.setWindowFlags(
            self.viewer.windowFlags() | Qt.WindowStaysOnTopHint)
        self.viewer.setMinimumSize(self.sizeWin)
        self.vertical_layout.addWidget(self.viewer)

        self.currentTimeLabel = QLabel(self.central_widget)
        self.currentTimeLabel.setMinimumSize(QSize(80, 0))
        self.currentTimeLabel.setAlignment(
            Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.horizontal_layout_4.addWidget(self.currentTimeLabel)

        self.timeSlider = QtWidgets.QSlider(self.central_widget)
        self.timeSlider.setOrientation(QtCore.Qt.Horizontal)

        self.horizontal_layout_4.addWidget(self.timeSlider)
        self.totalTimeLabel = QtWidgets.QLabel(self.central_widget)
        self.totalTimeLabel.setMinimumSize(QtCore.QSize(80, 0))
        self.totalTimeLabel.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.horizontal_layout_4.addWidget(self.totalTimeLabel)
        self.vertical_layout.addLayout(self.horizontal_layout_4)

        self.horizontal_layout_5 = QtWidgets.QHBoxLayout()
        self.horizontal_layout_5.setSpacing(6)

        self.play_button = QPushButton(QIcon("guiIcons/control.png"), "", self)
        self.horizontal_layout_5.addWidget(self.play_button)

        self.pause_button = QPushButton(QIcon("guiIcons/control-pause.png"), "", self)
        self.horizontal_layout_5.addWidget(self.pause_button)
        
        self.stopButton = QPushButton(QIcon("guiIcons/control-stop-square.png"), "", self)
        self.horizontal_layout_5.addWidget(self.stopButton)

        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontal_layout_5.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.central_widget)

        self.label.setPixmap(QtGui.QPixmap("guiIcons/speaker-volume.png"))
        self.horizontal_layout_5.addWidget(self.label)

        self.volumeSlider = QtWidgets.QSlider(self.central_widget)
        self.volumeSlider.setMaximum(100)
        self.volumeSlider.setProperty("value", 100)
        self.volumeSlider.setOrientation(QtCore.Qt.Horizontal)

        self.horizontal_layout_5.addWidget(self.volumeSlider)
        self.vertical_layout.addLayout(self.horizontal_layout_5)
        self.horizontal_layout.addLayout(self.vertical_layout)

        MainWindow.setCentralWidget(self.central_widget)

        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setGeometry(QRect(0, 0, 484, 22))

        self.menuFIle = QtWidgets.QMenu(self.menuBar)

        MainWindow.setMenuBar(self.menuBar)

        self.open_file_action = QAction(QIcon(
            "guiIcons\\directory.png"), "&Choose audio file in wav or mp3 format", self)
        self.menuFIle.addAction(self.open_file_action)
        self.menuBar.addAction(self.menuFIle.menuAction())

        self.currentTimeLabel.setText("0:00")
        self.totalTimeLabel.setText("0:00")
        self.menuFIle.setTitle("Open audio file")
        self.open_file_action.setText("Open audio file")

    def __init__(self):

        super(MainWindow, self).__init__()

        self.setWindowTitle("Guitario")
        self.setWindowIcon(QIcon('guiIcons\\music.png'))
        self.sizeWin = QSize(480, 360)
        self.setMinimumSize(self.sizeWin)

        # Fusion palettle, all thanks to author, https://gist.github.com/QuantumCD/6245215
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)

        oImage = QImage("guiIcons\\guitarWallPaper.png")
        sImage = oImage.scaled(self.sizeWin)
        palette.setBrush(QPalette.Background, QBrush(sImage))
        self.setPalette(palette)

        self.setupUi(self)

        # Setup QMediaPlayer
        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.player.error.connect(self.erroralert)

        videoWidget = QVideoWidget()
        self.viewer.setCentralWidget(videoWidget)
        self.player.setVideoOutput(videoWidget)

        # Connect control buttons/slides for QMediaPlayer
        self.play_button.pressed.connect(self.player.play)
        self.pause_button.pressed.connect(self.player.pause)
        self.stopButton.pressed.connect(self.player.stop)
        self.volumeSlider.valueChanged.connect(self.player.setVolume)

        self.player.durationChanged.connect(self.update_duration)
        self.player.positionChanged.connect(self.update_position)
        self.timeSlider.valueChanged.connect(self.player.setPosition)
        self.open_file_action.triggered.connect(self.open_file)

        #! LOADING MODEL
        self.working = False
        threading.Thread(target=self.load_model).start()

    def update_duration(self, duration):
        self.timeSlider.setMaximum(duration)

        if duration >= 0 and self.loading == False:
            self.totalTimeLabel.setText(self.hhmmss(duration))

    def update_position(self, position):
        if self.loading == False:
            if position >= 0:
                self.currentTimeLabel.setText(self.hhmmss(position))

            # Disable the events to prevent updating triggering a setPosition event
            self.timeSlider.blockSignals(True)
            self.timeSlider.setValue(position)
            self.timeSlider.blockSignals(False)

    def toggle_viewer(self, state):
        if state:
            self.viewer.show()
        else:
            self.viewer.hide()

    def extract_ziped_model(self):
        with ZipFile(MODEL_PATH + '.zip', 'r') as zip:
            print('Extracting model files! (first time program runs)')
            zip.extractall('models')
            print('Extracting model from zip file finished! (first time program runs)')
        os.remove(MODEL_PATH + '.zip')

    def load_model(self):
        print("Loading model!")
        if not os.path.isdir(MODEL_PATH):
            self.extract_ziped_model()
        self.model = tf.keras.models.load_model(MODEL_PATH)
        print("Ready to load the song!")

    def song_thread(self):
        self.working = True

        self.timeSlider.blockSignals(True)
        self.loading = True
        self.player.setMedia(QMediaContent(
            QUrl.fromLocalFile("guiIcons\\loading.gif")))
        self.viewer.setVisible(True)
        self.player.play

        print("Creating chords for song ", self.song)
        print("Please wait!")
        detection_list, duration_list = create_onset_info(
            self.song, SONG_DURATION, False)
        prediction_list = model_predict(self.model, detection_list)
        print("Found chord: ", prediction_list)

        #output frame resoultion for video
        image_shape = (200, 300)

        #creating folder saved_accords if does not exist
        Path("saved_accords").mkdir(parents=True, exist_ok=True)

        #!using cv2 to create videoClip
        VIDEO_FPS = 60
        VIDEO_PATH = "saved_accords\\" + os.path.basename(self.song[:-4])
        VIDEO_PATH_AVI = VIDEO_PATH + "_GENERATED.avi"
        out = cv2.VideoWriter(VIDEO_PATH_AVI, cv2.VideoWriter_fourcc(
            'M', 'J', 'P', 'G'), VIDEO_FPS, image_shape)
        timer = 0.0
        time_adder = 1/VIDEO_FPS

        for i in range(len(detection_list)):
            chord_image_path = "Guitar chords\\" + prediction_list[i] + '.png'
            chord_end = timer + duration_list[i]
            img = cv2.imread(chord_image_path)
            img = cv2.resize(img, image_shape, interpolation=cv2.INTER_AREA)

            while timer <= chord_end:
                out.write(img)
                timer += time_adder

        out.release()

        # adding sound to clip
        video = VideoFileClip(VIDEO_PATH_AVI, audio=False)
        audio = AudioFileClip(self.song)
        final = video.set_audio(audio)
        final.write_videofile(VIDEO_PATH + ".mp4", codec='mpeg4',
                              audio_codec='libvorbis', fps=VIDEO_FPS)
        self.player.stop
        self.loading = False
        self.player.setMedia(QMediaContent(
            QUrl.fromLocalFile(VIDEO_PATH + ".mp4")))
        self.timeSlider.blockSignals(False)
        self.player.play

        os.remove(VIDEO_PATH_AVI)
        self.working = False

    def open_file(self):

        path, _ = QFileDialog.getOpenFileName(
            self, "Open file", "", "wav or mp3 files (*.wav *.mp3)")
        if path != "" and self.working == False:
            self.song = read_song(path)
            if self.song != None:
                threading.Thread(target=self.song_thread).start()

    def erroralert(self, *args):
        print(args)
