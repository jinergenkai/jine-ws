@echo off
REM Force CPU mode even if CUDA is available
REM Useful for testing or when you want to save GPU resources

echo Starting API in CPU mode...
set DEVICE=cpu
python api.py
