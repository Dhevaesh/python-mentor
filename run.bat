@echo off
title Python Mentor — Code Testing & Learning Tool
cd /d "%~dp0"

echo ======================================================================
echo                Python Mentor: Learning & Practice Tool
echo ======================================================================
echo.

:: 1. Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not added to system PATH!
    echo Please install Python 3.9+ from https://www.python.org and check "Add to PATH".
    echo.
    pause
    exit /b 1
)

:: 2. Auto-check & install dependencies if missing
echo [*] Verifying environment dependencies...
python -c "import streamlit, PIL" >nul 2>&1
if %errorlevel% neq 0 (
    echo [*] Installing required packages (streamlit, pillow)...
    python -m pip install -r requirements.txt
    echo [*] Dependencies installed successfully.
)

:: 3. Launch Application
echo [*] Launching Python Mentor on http://localhost:8501 ...
echo.
python -m streamlit run app.py
pause
