#!/bin/bash
# Force CPU mode even if CUDA is available
# Useful for testing or when you want to save GPU resources

echo "Starting API in CPU mode..."
DEVICE=cpu python api.py
