@echo off
setlocal
py -3.13 -m pip install -r requirements.txt
py -3.13 -m PyInstaller --noconfirm --clean --onefile --windowed --name fh6_tuner fh6_tuner.py
if errorlevel 1 exit /b 1
echo.
echo Build complete: dist\fh6_tuner.exe
