# Pre-download Model

Pre-download the model to avoid waiting during first Docker run.

## Method 1: Download to Local Cache (Recommended)

### Windows:
```bash
download_model.bat
```

### Linux/Mac:
```bash
chmod +x download_model.sh
./download_model.sh
```

### Or use Python directly:
```bash
python download_model.py
```

This downloads the model (~3-4GB) to:
- **Windows**: `C:\Users\YourName\.cache\huggingface`
- **Linux/Mac**: `~/.cache/huggingface`

Docker will automatically use this cache when you run `make cpu` or `make gpu`.

## Method 2: Download Inside Docker Image

Create a custom Dockerfile that includes the model:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
RUN pip install transformers torch

# Pre-download model
RUN python -c "from transformers import AutoModel, AutoTokenizer; \
    AutoModel.from_pretrained('5CD-AI/Vintern-1B-v3_5', trust_remote_code=True); \
    AutoTokenizer.from_pretrained('5CD-AI/Vintern-1B-v3_5', trust_remote_code=True)"

# Copy your app
COPY api.py .

CMD ["python", "api.py"]
```

Build:
```bash
docker build -t vintern-ocr-preloaded .
```

## Method 3: Docker Volume Pre-population

Download model into a Docker volume:

```bash
# Create volume
docker volume create vintern-model-cache

# Download model into volume
docker run --rm \
  -v vintern-model-cache:/root/.cache/huggingface \
  python:3.10-slim \
  bash -c "pip install transformers && \
    python -c \"from transformers import AutoModel; \
    AutoModel.from_pretrained('5CD-AI/Vintern-1B-v3_5', trust_remote_code=True)\""

# Update docker-compose.yml to use this volume
# volumes:
#   - vintern-model-cache:/root/.cache/huggingface
```

## Verify Download

Check if model is cached:

### Windows:
```bash
dir %USERPROFILE%\.cache\huggingface\hub\models--5CD-AI--Vintern*
```

### Linux/Mac:
```bash
ls -lh ~/.cache/huggingface/hub/models--5CD-AI--Vintern*
```

## After Download

Run Docker normally:
```bash
# Windows
$env:HOME = $env:USERPROFILE
make cpu

# Linux/Mac
make cpu
```

The container will start in ~5 seconds instead of 5-10 minutes!
