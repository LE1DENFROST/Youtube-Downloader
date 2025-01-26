# 🎥 Minimalist YouTube Downloader

A powerful, lightweight YouTube video and audio downloader built with PyQt6 and `yt_dlp`. This project provides a user-friendly GUI for seamless downloading of high-quality YouTube videos and audio files.

---

## 📝 Changelog

### Fixes and Updates (v2025):

- **Switched to ** for enhanced stability and compatibility.
- **Batch Script**: Automatically installs missing libraries before running the app.
- **Pythonw Integration**: Runs the application in the background for a seamless experience.
- **Improved Error Handling**: Detailed feedback for common issues.
- **Directory Checks**: Ensures necessary folders (`indirilen_mp3`, `indirilen_videolar`) are created.
- **UTF-8 Support**: Proper handling of Turkish characters in file paths and UI.
- **UI Enhancements**: Streamlined for a better user experience.

---

## ✨ Key Features

- **Multiple Quality Options**: Download videos in 1080p, 720p, 480p, and more.
- **Audio Downloads**: Easily convert and download audio in MP3 format.
- **Stable & Reliable**: Built using `yt_dlp` for enhanced stability and compatibility.
- **Custom Save Locations**: Choose where to save your downloads.
- **Real-Time Progress Updates**: See the download progress with detailed speed and ETA feedback.
- **Error Handling**: Provides clear and helpful error messages for common issues.
- **Turkish Language Support**: UTF-8 encoding ensures compatibility with Turkish characters.

---

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

- **Python 3.9 or higher**
---

### 💻 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/LE1DENFROST/Youtube-Downloader.git
   ```
2. Navigate to the project folder:
   ```bash
   cd Youtube-Downloader
   ```

3. Run the application:
   ```bash
   start.bat
   ```

---

## 🛠 Features in Detail

- **Video Quality Options**:

  - `1080p`, `720p`, `480p`, `Best Quality`, and `Lowest Quality` are supported.
  - If an unsupported quality is selected, the app prompts users to choose a valid option.

- **Audio Extraction**:

  - Converts videos to MP3 format with a bitrate of 192kbps.

- **Error Feedback**:

  - User-friendly messages for issues like invalid URLs, network failures, or unsupported formats.

- **Batch Script for Dependency Management**:

  - Checks for missing Python libraries and installs them automatically.

---

## 🎨 User Interface

The UI is built using **PyQt6** for a modern and intuitive experience:

- **Dynamic Progress Bar**: Real-time download progress and speed.
- **Status Updates**: Clear messages at each step of the download process.
- **Dark Mode**: Sleek black-themed interface for comfortable usage.

---

## 🔧 Troubleshooting

1. **Missing Libraries**: Run the following command to ensure all dependencies are installed:
   ```bash
   start.bat
   ```
2. **Invalid URL Error**: Ensure the provided URL is valid and points to a YouTube video or playlist.
3. **No Download Button**: Check your `PyQt6` installation by running:
   ```bash
   pip show pyqt6
   ```
   
## 🤝 Contributions

Contributions are welcome! Feel free to submit issues, fork the repo, and open pull requests.

---



## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 💬 Feedback

Have suggestions or found a bug? Open an issue or contact me directly!

---

### 🎉 Happy Downloading! 🎉

