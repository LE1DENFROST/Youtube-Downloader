import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPalette, QColor, QMovie
from PyQt6.QtWidgets import (
    QLabel, QMessageBox, QFileDialog, QMainWindow, 
    QVBoxLayout, QHBoxLayout, QWidget, QPushButton,
    QComboBox, QLineEdit, QProgressBar, QApplication
)
import yt_dlp

class VideoQuality(Enum):
    BEST = "En İyi Kalite"
    LOWEST = "En Düşük Kalite"
    AUDIO = "MP3"
    P1080 = "1080p"
    P720 = "720p"
    P480 = "480p"

@dataclass
class DownloadConfig:
    url: str
    quality: VideoQuality
    save_path: Path


class DownloadManager(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    status_update = pyqtSignal(str)

    def __init__(self, config: DownloadConfig):
        super().__init__()
        self.config = config
        self.is_cancelled = False
        self._setup_download_options()

    def _setup_download_options(self):
        self.ydl_opts = {
            'format': self._get_format_string(),
            'outtmpl': str(self.config.save_path / '%(title)s.%(ext)s'),
            'progress_hooks': [self._progress_hook],
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'quiet': False,
            'no_warnings': False,
            'extract_flat': False,
            'postprocessors': self._get_postprocessors()
        }

    def _get_format_string(self) -> str:
        if self.config.quality == VideoQuality.AUDIO:
            return 'bestaudio/best'
        elif self.config.quality == VideoQuality.BEST:
            return 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        elif self.config.quality == VideoQuality.P1080:
            return 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]'
        elif self.config.quality == VideoQuality.P720:
            return 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]'
        elif self.config.quality == VideoQuality.P480:
            return 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]'
        else:
            return 'worstvideo[ext=mp4]+worstaudio[ext=m4a]/worst[ext=mp4]/worst'

    def _get_postprocessors(self) -> list:
        if self.config.quality == VideoQuality.AUDIO:
            return [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        return []

    def run(self):
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                self.status_update.emit("Video bilgileri alınıyor...")
                info = ydl.extract_info(self.config.url, download=True)
                title = info.get('title', 'Video')
                self.finished.emit(f"{title} başarıyla indirildi")
        except Exception as e:
            self.error.emit(f"İndirme hatası: {str(e)}")

    def _progress_hook(self, d):
        if self.is_cancelled:
            raise Exception("İndirme iptal edildi")
        
        if d['status'] == 'downloading':
            try:
                total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                downloaded = d.get('downloaded_bytes', 0)
                if total > 0:
                    percentage = int((downloaded / total) * 100)
                    self.progress.emit(percentage)
                    speed = d.get('speed', 0)
                    if speed:
                        speed_mb = speed / (1024 * 1024)
                        eta = d.get('eta', 0)
                        minutes = eta // 60
                        seconds = eta % 60
                        time_str = ""
                        if minutes > 0:
                            time_str = f"{int(minutes)} dakika "
                        time_str += f"{int(seconds)} saniye"
                        self.status_update.emit(
                            f"İndiriliyor... {speed_mb:.1f} MB/s - Kalan süre: {time_str}"
                        )
            except Exception as e:
                print(f"Progress calculation error: {e}")

class MinimalistDownloaderUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SR YT Downloader v2.15")
        self.setFixedSize(370, 589)
        self.init_ui()
        self.download_manager = None
        
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setup_header()
        layout.addWidget(self.header_widget)
        self.setup_controls()
        layout.addWidget(self.controls_widget)

    def setup_header(self):
        self.header_widget = QWidget()
        header_layout = QVBoxLayout(self.header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)
        self.gif_label = QLabel()
        movie = QMovie('images/whatever.gif')
        self.gif_label.setMovie(movie)
        movie.start()
        self.gif_label.setFixedHeight(300)
        self.gif_label.setScaledContents(True)
        header_layout.addWidget(self.gif_label)
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(30)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: red;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #3498db;
            }
        """)
        header_layout.addWidget(self.progress_bar)
        self.status_label = QLabel("Hazır")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                padding: 5px;
                background-color: #000000;
                color: white;
            }
        """)
        header_layout.addWidget(self.status_label)
        
    def setup_controls(self):
        self.controls_widget = QWidget()
        controls_layout = QVBoxLayout(self.controls_widget)
        controls_layout.setContentsMargins(10, 10, 10, 10)
        controls_layout.setSpacing(10)

        url_label = QLabel("YouTube URL")
        url_label.setStyleSheet("color: white; font-size: 12pt;")
        controls_layout.addWidget(url_label)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("YouTube URL'sini yapıştırın")
        self.url_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid yellow;
                border-radius: 5px;
                background-color: #000000;
                color: white;
            }
            QLineEdit:focus {
                border-color: yellow;
                color: white;
            }
        """)
        controls_layout.addWidget(self.url_input)

        quality_label = QLabel("Video Kalitesi")
        quality_label.setStyleSheet("color: white; font-size: 12pt;")
        controls_layout.addWidget(quality_label)

        self.quality_combo = QComboBox()
        self.quality_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid green;
                border-radius: 5px;
                background-color: #000000;
                color: white;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid none;
                border-right: 5px solid none;
                border-top: 5px solid white;
                width: 0;
                height: 0;
                margin-right: 5px;
            }
        """)
        for quality in VideoQuality:
            self.quality_combo.addItem(quality.value)
        controls_layout.addWidget(self.quality_combo)

        button_layout = QHBoxLayout()
        self.download_button = QPushButton("İndir")
        self.download_button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 12pt;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #2475a8;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        self.download_button.clicked.connect(self.start_download)
        button_layout.addWidget(self.download_button)

        self.cancel_button = QPushButton("İptal")
        self.cancel_button.setEnabled(False)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 12pt;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        self.cancel_button.clicked.connect(self.cancel_download)
        button_layout.addWidget(self.cancel_button)
        controls_layout.addLayout(button_layout)

    def start_download(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Hata", "Lütfen bir URL girin!")
            return

        selected_quality = self.quality_combo.currentText()
        if selected_quality not in [q.value for q in VideoQuality]:
            QMessageBox.warning(self, "Hata", "Geçerli bir kalite seçin (1080p, 720p, 480p veya diğerleri)!")
            return

        save_path = QFileDialog.getExistingDirectory(
            self, "İndirme Konumu Seç", 
            str(Path.home() / "Downloads")
        )
        if not save_path:
            return

        config = DownloadConfig(
            url=url,
            quality=VideoQuality(selected_quality),
            save_path=Path(save_path)
        )
        self.download_manager = DownloadManager(config)
        self.download_manager.progress.connect(self.progress_bar.setValue)
        self.download_manager.status_update.connect(self.status_label.setText)
        self.download_manager.finished.connect(self.download_finished)
        self.download_manager.error.connect(self.show_error)
        self.download_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.progress_bar.setValue(0)
        self.download_manager.start()

    def cancel_download(self):
        if self.download_manager and self.download_manager.isRunning():
            self.download_manager.is_cancelled = True
            self.download_manager.terminate()
            self.download_manager.wait()
            self.status_label.setText("İndirme iptal edildi")
            self.reset_ui()

    def show_error(self, message):
        QMessageBox.critical(self, "Hata", message)
        self.reset_ui()

    def download_finished(self, message):
        QMessageBox.information(self, "Başarılı", message)
        self.reset_ui()
        self.status_label.setText(message)

    def reset_ui(self):
        self.download_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        self.progress_bar.setValue(0)

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('images/icon.png'))
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Base, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Button, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
    app.setPalette(palette)
    window = MinimalistDownloaderUI()
    window.setWindowIcon(QtGui.QIcon('images/icon.png'))
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
