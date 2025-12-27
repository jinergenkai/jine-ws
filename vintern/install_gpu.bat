@echo off
REM Simple GPU installation for Vintern OCR API

echo Installing Vintern OCR API (GPU version with CUDA 11.8)...

REM Create virtual environment
python -m venv venv
call venv\Scripts\activate.bat

REM Upgrade pip
pip install --upgrade pip

REM Install dependencies (without torch)
pip install fastapi uvicorn[standard] python-multipart transformers Pillow numpy einops timm

REM Install PyTorch with CUDA 11.8
pip install --index-url https://download.pytorch.org/whl/cu118 torch torchvision

echo.
echo Installation complete!
echo To run the API:
echo   venv\Scripts\activate.bat
echo   set DEVICE=cuda
echo   python api.py
