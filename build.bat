
@echo off
setlocal

REM Path of scripts and assets
set SCRIPT_NAME=main.py
set ASSETS_FOLDER=Assets
set DATA_FOLDER=Data

REM Check if PyInstaller is installed, and install it if needed
python -c "import PyInstaller" 2>nul
if %errorlevel% neq 0 (
    echo PyInstaller is not installed. Installing...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo Error: Failed to install PyInstaller.
        pause
        exit /b %errorlevel%
    )
)

REM Run PyInstaller
pyinstaller --onefile --noconsole %SCRIPT_NAME%

REM Check if PyInstaller succeeded
if %errorlevel% neq 0 (
    echo Error: PyInstaller failed.
    pause
    exit /b %errorlevel%
)

REM Create the 'game' folder if it doesn't exist
if not exist Game mkdir Game

REM Copy the executable to the 'game' folder
copy dist\%SCRIPT_NAME:.py=%* Game\

REM Copy the assets to the 'game' folder
xcopy /s %ASSETS_FOLDER%\* Game\%ASSETS_FOLDER%\

REM Copy the 'Data' folder and its contents to the 'game' folder
xcopy /s %DATA_FOLDER%\* Game\%DATA_FOLDER%\

echo Build successful! Executable and assets are in the 'Game' folder.
pause
exit /b 0
