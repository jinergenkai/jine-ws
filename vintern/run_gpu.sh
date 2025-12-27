#!/bin/bash
# Force GPU/CUDA mode
# Will fall back to CPU if CUDA is not available

echo "Starting API in GPU mode..."
DEVICE=cuda python api.py
