
import sys
import os
import requests
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, QThread, pyqtSignal 
from PyQt6.QtGui import QPalette, QColor, QMovie, QIcon ,QPixmap
from pytube import YouTube
from PyQt6.QtWidgets import QLabel
import yt_dlp
import webbrowser


class DownloadThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)

    def __init__(self, video_url, selected_quality):
        super().__init__()
        self.video_url = video_url
        self.selected_quality = selected_quality

    def run(self):
        try:
            if self.selected_quality == "mp3":
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'outtmpl': 'indirilen_mp3/%(title)s.%(ext)s',
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(self.video_url, download=True)
                    if 'entries' in info_dict:
                        video_title = info_dict['entries'][0]['title']
                    else:
                        video_title = info_dict['title']

                self.finished.emit(f"{video_title} indirildi")
            else:
                yt = YouTube(self.video_url)

                if self.selected_quality == "En Düşük Kalite":
                    video = yt.streams.get_lowest_resolution()
                elif self.selected_quality == "En İyi Kalite":
                    video = yt.streams.get_highest_resolution()

                download_path = "indirilen_videolar/"
                if not os.path.exists(download_path):
                    os.makedirs(download_path)

                response = requests.get(video.url, stream=True)
                total_size_in_bytes = int(response.headers.get('content-length', 0))
                block_size = 1024  

                with open(os.path.join(download_path, video.default_filename), 'wb') as file:
                    bytes_downloaded = 0
                    for data in response.iter_content(block_size):
                        file.write(data)
                        bytes_downloaded += len(data)
                        percentage = int(bytes_downloaded / total_size_in_bytes * 100)
                        self.progress.emit(percentage)

                self.finished.emit("Video başarıyla indirildi.")
        except Exception as e:
            self.finished.emit(f"Hata: {str(e)}")
            print(str(e))
            
      
          

            
class Ui_MainWindow(object):
   

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(370, 589)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        icon = QIcon(r"images\icon.png")  
        self.setWindowIcon(icon)
        
        
        self.gif = QLabel(parent=self.centralwidget)
        self.gif.setGeometry(QtCore.QRect(0, 0, 371, 301))
        self.gif.setCursor(Qt.CursorShape.PointingHandCursor)
        image_path = r"images\background.gif"
        movie = QMovie(image_path)
        self.gif.setMovie(movie)
        self.gif.setScaledContents(True)
        
        
        
        
        self.gif2 = QLabel(parent=self.centralwidget)
        self.gif2.setGeometry(QtCore.QRect(210, 430, 151, 121))
        self.gif2.setCursor(Qt.CursorShape.PointingHandCursor)
        image_path2 = r"images\loading.gif"
        movie2 = QMovie(image_path2)
        self.gif2.setMovie(movie2)
        self.gif2.setScaledContents(True)
        movie2.start()
        movie.start()
        self.gif2.mousePressEvent = self.open_youtube
          
        pixmap = QPixmap(r"images\indir.png")
        self.download = QLabel(parent=self.centralwidget)
        self.download.setGeometry(QtCore.QRect(10, 470, 131, 81))
        self.download.setPixmap(pixmap)  
        self.download.mousePressEvent = self.start_download
        self.download.setScaledContents(True)
          
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        self.setPalette(palette)
        self.progressBar = QtWidgets.QProgressBar(parent=self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(0, 300, 371, 31))
        self.progressBar.setProperty("value", 0)  
        self.progressBar.setObjectName("progressBar")
        self.lineEdit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(0, 380, 371, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(120, 350, 121, 21))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 330, 231, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.comboBox = QtWidgets.QComboBox(parent=self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(0, 440, 141, 21))
        self.comboBox.setObjectName("comboBox")
        self.comboBox = QtWidgets.QComboBox(parent=self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(0, 440, 141, 21))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("En İyi Kalite")
        self.comboBox.addItem("En Düşük Kalite")
        self.comboBox.addItem("mp3")
        self.label_3 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(0, 420, 81, 20))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(9)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.line = QtWidgets.QFrame(parent=self.centralwidget)
        self.line.setGeometry(QtCore.QRect(159, 410, 31, 141))
        self.line.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Savitar YT Downloader v2.0 Final"))
        self.label.setText(_translate("MainWindow", "Youtube URL"))
        self.label_2.setText(_translate("MainWindow", "İlerleme..."))
        self.label_3.setText(_translate("MainWindow", " Kalite :"))

    def open_youtube(self, event):
        webbrowser.open("https://www.youtube.com/watch?v=Ds5bR72gNzc")
    
    
    
    def start_download(self,event):
        video_url = self.lineEdit.text()
        selected_quality = self.comboBox.currentText()

        if not video_url:
            QtWidgets.QMessageBox.critical(None, "Hata", "Video URL'si boş olamaz.")
            return

        self.label_2.setText("Videoyu indirmeye başlandı...")
        self.download.setEnabled(False)
        self.download_thread = DownloadThread(video_url, selected_quality)
        self.download_thread.finished.connect(self.download_finished)
        self.download_thread.progress.connect(self.update_progress_bar)
        self.download_thread.start()

    def download_finished(self, message):
        self.label_2.setText(message)
        self.download.setEnabled(True)
        self.progressBar.setValue(0)

    def update_progress_bar(self, percentage):
        self.progressBar.setValue(percentage)

class YouTubeDownloader(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = YouTubeDownloader()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 
