import sys
import os

from colorama import init, Fore, Style
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer

class MP3player(QWidget):
    def __init__(self):
        super().__init__()
        self.state = "Start"
        self.playlist = []
        self.position = 0



        self.init_ui()

    def init_ui(self):
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "img/play.png")))
        vb = QVBoxLayout()
        self.setLayout(vb)
        vb.setAlignment(Qt.AlignCenter)

        #label ui
        self.label = QLabel("""
    ░█▀▄░█▀█░█▄█░█▀█░█▀▀
    ░█▀▄░█▀█░█░█░█▀▀░▀▀█
    ░▀░▀░▀░▀░▀░▀░▀░░░▀▀▀       
                                         """)
        self.label.setFont(QFont("Calibri", 20))
        self.label.setAlignment(Qt.AlignCenter)
        vb.addWidget(self.label)
        #box
        
        #button
        

        #import song
        self.songlist = QListWidget()
        vb.addWidget(self.songlist)
        #toolbar
        self.toolbar = QToolBar()
        vb.addWidget(self.toolbar)
        hb2 = QHBoxLayout()
        hb = QHBoxLayout()
        vb.addLayout(hb)

        
        #second box
        
        vb.addLayout(hb2)
        font = QFont("Helvetica", 14)
        self.openfile = QPushButton()
        self.openfile.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "img/folder.png")))
        self.openfile.setFont(font)
        hb2.addWidget(self.openfile)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position) #connect ke fungsi set_position
        hb2.addWidget(self.slider)

        #self.skipbackward = QPushButton()
        #self.skipbackward.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipBackward))
        #hb.addWidget(self.skipbackward)
        self.backward = QPushButton()
        self.backward.setIconSize(QSize(64, 64))
        self.backward.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "img/backward.png")))
        self.backward.setFont(font)
        hb.addWidget(self.backward)
        self.playbutton = QPushButton()
        self.playbutton.setEnabled(False)
        self.playbutton.setIconSize(QSize(64, 64))
        self.playbutton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "img/play.png")))
        self.playbutton.setFont(font)
        hb.addWidget(self.playbutton)
        self.forward = QPushButton()
        self.forward.setIconSize(QSize(64, 64))
        self.forward.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "img/forward.png")))
        self.forward.setFont(font)
        hb.addWidget(self.forward)
        #self.skipforward = QPushButton()
        #self.skipforward.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
        #hb.addWidget(self.skipforward)
        
        
        self.openfileact = QAction()
        self.openfileact.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "img/folder.png")))
        self.openfileact.setFont(font)
        self.toolbar.addSeparator()
        #volume

        self.player = QMediaPlayer(self)

        self.openfile.clicked.connect(self.open_song)
        self.playbutton.clicked.connect(self.play_song)
        self.player.positionChanged.connect(self.position_change)
        self.player.durationChanged.connect(self.duration_changed)
        self.player.stateChanged.connect(self.state_changed)
        self.backward.clicked.connect(self.m_backward)
        self.forward.clicked.connect(self.m_forward)
        self.songlist.clicked.connect(self.set_state)
        self.songlist.doubleClicked.connect(self.play_song) #supaya gak usah pencet play, klik 2 kali aja!

        self.playbutton.setFlat(True)
        #do you know that you can use css in PyQt? if you are frontend developer, you can easily make a design to this weird design.
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #616161,
                    stop:1 #000000
                );
                background-repeat: no-repeat;
                color: white;
                font-family: 'Segoe UI';
            }

            QPushButton {
                background-color: #3a3a3a;
                border: 2px solid #555;
                border-radius: 10px;
                padding: 8px;
            }

            QPushButton:hover {
                background-color: #505050;
            }

            QPushButton:pressed {
                background-color: #2e2e2e;
            }

            QListWidget {
                background-color: #252525;
                border: 1px solid #444;
            }

            QSlider::groove:horizontal {
                background: #555;
                height: 6px;
                border-radius: 3px;
            }

            QSlider::handle:horizontal {
                background: green;
                width: 14px;
                border-radius: 7px;
                margin: -4px 0;
            }
        """)
        self.forward.setStyleSheet("""
            QPushButton{
                border: none;
                background: transparent;             
            }
            QPushButton:hover{
                border: none;
            QPushButton:pressed {
                border: none;  
            }
        """)
        self.backward.setStyleSheet("""
            QPushButton{
                border: none;
                background: transparent;             
            }
            QPushButton:hover{
                border: none;
            QPushButton:pressed {
                border: none;  
            }
        """)
        self.playbutton.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: white;
            }
            QPushButton {
                border: none;
                background: transparent;
            }
            QPushButton:hover {
                opacity: 0.8;
            }
        """)


    def open_song(self):
        file = QFileDialog()
        file.setFileMode(QFileDialog.ExistingFiles)
        name = file.getOpenFileNames(self, "Open Files", os.getenv("HOME"))
        song = name[0]
        self.songlist.addItems(song)

    def set_state(self):
        self.playbutton.setEnabled(True)
        self.state = "Play" #supaya enggak perlu pencet 2 kali!
        self.playbutton.setIconSize(QSize(64, 64))
        self.playbutton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "img/play.png")))

    def play_song(self):
        if self.state == "Play":
            self.playbutton.setIconSize(QSize(64, 64))
            self.playbutton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "img/pause.png")))
            self.state = "Pause"
            path = self.songlist.currentItem().text()
            url = QUrl.fromLocalFile(path)
            content = QMediaContent(url)
            self.player.setMedia(content)
            self.player.setPosition(self.position)
            self.playlist.append(path)
            if len(self.playlist) > 2:
                self.playlist.pop()
            if self.songlist.currentItem().text() != self.playlist[0]:
                self.position = 0
                self.player.setPosition(self.position)
            self.player.play()
        else:
            self.playbutton.setIconSize(QSize(64, 64))  # contoh ukuran besar
            self.playbutton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "img/pause.png")))
            self.state = "Play"
            self.player.pause()
            paused = self.player.position()
            self.position = paused

    def set_position(self, position):
        self.player.setPosition(position)

    def position_change(self, position):
        self.slider.setValue(position)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def state_changed(self, state):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.playbutton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "img/pause.png")))
        else:
            self.playbutton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "img/play.png")))

    def m_forward(self):
        self.player.setPosition(int(self.player.position()) + 2000)

    def m_backward(self):
        self.player.setPosition(int(self.player.position()) -  2000)

        
def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("D:/RangS_Git/RangS-mp3/img/play.png"))
    ui = MP3player()
    ui.setWindowTitle("RangS MP3 Player 🎧")
    ui.setWindowIcon(QIcon("D:/RangS_Git/RangS-mp3/img/play.png"))
    ui.setGeometry(600, 200, 600, 500)
    ui.show()
    sys.exit(app.exec_()) 

if __name__ == '__main__':
    main()
