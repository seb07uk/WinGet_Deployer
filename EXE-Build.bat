@echo off
title polsoft.ITS™ WinGet Deployer — Build Process
setlocal ENABLEDELAYEDEXPANSION

:: ANSI colors (Windows 10+)
for /f "delims=" %%a in ('echo prompt $E^| cmd') do set "ESC=%%a"

cls
echo %ESC%[96m
echo                   888                    .d888 888        8888888 88888888888 .d8888b.
echo                   888                   d88P"  888          888       888    d88P  Y88b
echo                   888                   888    888          888       888    Y88b.
echo 88888b.   .d88b.  888 .d8888b   .d88b.  888888 888888       888       888     "Y888b.
echo 888 "88b d88""88b 888 88K      d88""88b 888    888          888       888        "Y88b.
echo 888  888 888  888 888 "Y8888b. 888  888 888    888          888       888          "888
echo 888 d88P Y88..88P 888      X88 Y88..88P 888    Y88b.  d8b   888       888    Y88b  d88P
echo 88888P"   "Y88P"  888  88888P'  "Y88P"  888     "Y888 Y8P 8888888     888     "Y8888P"
echo 888                            888                            888
echo 888                            888                            888
echo 888                            888                            888
echo                                888      .d88b.  88888b.   .d88888  .d88b.  88888b.
echo                                888     d88""88b 888 "88b d88" 888 d88""88b 888 "88b
echo                                888     888  888 888  888 888  888 888  888 888  888
echo                                888     Y88..88P 888  888 Y88b 888 Y88..88P 888  888
echo                                88888888 "Y88P"  888  888  "Y88888  "Y88P"  888  888
echo %ESC%[0m
echo.

echo %ESC%[93mChecking Python/pip environment...%ESC%[0m

pip --version >nul 2>&1
if errorlevel 1 (
    echo %ESC%[91mError: pip is not available in PATH.%ESC%[0m
    echo Install Python with the "Add to PATH" option enabled.
    pause
    exit /b 1
)

echo %ESC%[92mOK — pip detected.%ESC%[0m
echo.

echo %ESC%[93mChecking and installing PyInstaller...%ESC%[0m
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo %ESC%[91mPyInstaller installation failed!%ESC%[0m
        pause
        exit /b 1
    )
) else (
    echo %ESC%[92mPyInstaller is already installed.%ESC%[0m
)

echo.
echo %ESC%[96mStarting build process...%ESC%[0m
echo.

pyinstaller ^
 --noconsole ^
 --onefile ^
 --icon="icon.ico" ^
 --version-file="version.txt" ^
 --name "WinGetDeployer" ^
 main.py

if errorlevel 1 (
    echo %ESC%[91mBuild failed!%ESC%[0m
    pause
    exit /b 1
)

echo.
echo %ESC%[92mBuild completed successfully!%ESC%[0m
echo Your EXE file is located in: %ESC%[96m.\dist\WinGetDeployer.exe%ESC%[0m
echo.

pause