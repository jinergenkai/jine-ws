@echo off
REM Pre-download model for Docker

echo Pre-downloading Vintern model...
echo.

REM Activate venv if exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo Using virtual environment
) else (
    echo Using system Python
)

REM Install transformers if not installed
pip show transformers >nul 2>&1 || pip install transformers

REM Download model
python download_model.py

echo.
echo Done! Now run: make cpu
pause
