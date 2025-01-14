REM Python'un yüklü olup olmadığını kontrol et
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python sistemde yüklü değil. Lütfen Python'u yükleyin.
    pause
    exit /b
)

REM Gerekli kütüphanelerin kurulu olup olmadığını kontrol et
echo Gerekli kütüphaneler kontrol ediliyor...
python -m pip show PyQt6 >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo PyQt6 kütüphanesi eksik. Yükleniyor...
    python -m pip install PyQt6
)

python -m pip show yt_dlp >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo yt_dlp kütüphanesi eksik. Yükleniyor...
    python -m pip install yt_dlp
)

REM Gerekli tüm kütüphaneler yüklendi, uygulama başlatılıyor
echo Uygulama başlatılıyor...
start "" pythonw tools\main.py

REM CMD ekranını kapat
exit
