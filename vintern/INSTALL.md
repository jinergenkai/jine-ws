# Vintern OCR API - Simple Installation

## Quick Start

### CPU Version (Lightweight - ~2.5GB)

**Linux/Mac:**
```bash
chmod +x install_cpu.sh
./install_cpu.sh
```

**Windows:**
```bash
install_cpu.bat
```

### GPU Version (CUDA 11.8 - ~9GB)

**Linux/Mac:**
```bash
chmod +x install_gpu.sh
./install_gpu.sh
```

**Windows:**
```bash
install_gpu.bat
```

## Run the API

**CPU:**
```bash
# Linux/Mac
source venv/bin/activate
DEVICE=cpu python api.py

# Windows
venv\Scripts\activate.bat
set DEVICE=cpu
python api.py
```

**GPU:**
```bash
# Linux/Mac
source venv/bin/activate
DEVICE=cuda python api.py

# Windows
venv\Scripts\activate.bat
set DEVICE=cuda
python api.py
```

API will run at: `http://localhost:11200`

## Test

```bash
curl http://localhost:11200/health
```

## Usage

```bash
curl -X POST http://localhost:11200/extract \
  -F "file=@image.jpg" \
  -F "max_num=12" \
  -F "max_new_tokens=4096"
```

## Configuration

Set environment variables before running:

```bash
# Device (cpu or cuda)
export DEVICE=cpu

# Max file size (10MB default)
export MAX_FILE_SIZE=10485760

# CORS origins
export ALLOWED_ORIGINS=*

# Model name
export MODEL_NAME=5CD-AI/Vintern-1B-v3_5
```

## Manual Installation

If scripts don't work:

```bash
# 1. Create venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate.bat  # Windows

# 2. Install dependencies
pip install fastapi uvicorn[standard] python-multipart transformers Pillow numpy einops timm

# 3. Install PyTorch
# CPU:
pip install --index-url https://download.pytorch.org/whl/cpu torch torchvision

# GPU (CUDA 11.8):
pip install --index-url https://download.pytorch.org/whl/cu118 torch torchvision

# 4. Run
python api.py
```

## Requirements

- Python 3.10+
- 8GB RAM (CPU) or 16GB RAM (GPU)
- GPU: NVIDIA GPU with CUDA 11.8 support

That's it! No Docker, no complexity.
