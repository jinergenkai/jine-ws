#!/bin/bash
# Simple CPU installation for Vintern OCR API

echo "Installing Vintern OCR API (CPU version)..."

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies (without torch)
pip install fastapi uvicorn[standard] python-multipart transformers Pillow numpy einops timm

# Install PyTorch CPU version
pip install --index-url https://download.pytorch.org/whl/cpu torch torchvision

echo ""
echo "Installation complete!"
echo "To run the API:"
echo "  source venv/bin/activate"
echo "  DEVICE=cpu python api.py"
