#!/bin/bash
# Pre-download model for Docker

echo "Pre-downloading Vintern model..."
echo ""

# Activate venv if exists, otherwise use system Python
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "Using virtual environment"
else
    echo "Using system Python"
fi

# Install transformers if not installed
pip show transformers > /dev/null 2>&1 || pip install transformers

# Download model
python download_model.py

echo ""
echo "Done! Now run: make cpu"
