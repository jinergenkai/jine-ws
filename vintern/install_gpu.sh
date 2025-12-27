#!/bin/bash
# Simple GPU installation for Vintern OCR API

echo "Installing Vintern OCR API (GPU version with CUDA 11.8)..."

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies (without torch)
pip install fastapi uvicorn[standard] python-multipart transformers Pillow numpy einops timm

# Install PyTorch with CUDA 11.8
pip install --index-url https://download.pytorch.org/whl/cu118 torch torchvision

echo ""
echo "Installation complete!"
echo "To run the API:"
echo "  source venv/bin/activate"
echo "  DEVICE=cuda python api.py"
