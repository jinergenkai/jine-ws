@echo off
REM Simple CPU installation for Vintern OCR API

echo Installing Vintern OCR API (CPU version)...

REM Create virtual environment
python -m venv venv
call venv\Scripts\activate.bat

REM Upgrade pip
pip install --upgrade pip

REM Install dependencies (without torch)
pip install fastapi uvicorn[standard] python-multipart transformers Pillow numpy einops timm

REM Install PyTorch CPU version
pip install --index-url https://download.pytorch.org/whl/cpu torch torchvision

echo.
echo Installation complete!
echo To run the API:
echo   venv\Scripts\activate.bat
echo   set DEVICE=cpu
echo   python api.py
