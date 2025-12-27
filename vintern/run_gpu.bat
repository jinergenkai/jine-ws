@echo off
REM Force GPU/CUDA mode
REM Will fall back to CPU if CUDA is not available

echo Starting API in GPU mode...
set DEVICE=cuda
python api.py
