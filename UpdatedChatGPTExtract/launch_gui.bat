@echo off
REM Launch ChatGPT Thread Extractor GUI

python extractor_gui.py

if %errorlevel% neq 0 (
    echo.
    echo Error: Python not found or script failed to run
    echo Make sure Python 3.6+ is installed and in your PATH
    echo.
    pause
)
