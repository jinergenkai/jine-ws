# Deployment Guide - Vintern OCR API

## Quick Start

### 🖥️ CPU Version (No GPU required)

```bash
# Build and run
docker-compose --profile cpu up -d --build

# Check status
docker-compose ps

# View logs
docker-compose logs -f vintern-ocr-cpu

# Stop
docker-compose --profile cpu down
```

API available at: `http://localhost:11200`

### 🚀 GPU Version (NVIDIA GPU required)

**Prerequisites:**
- NVIDIA GPU with CUDA support
- [NVIDIA Docker runtime](https://github.com/NVIDIA/nvidia-docker) installed

```bash
# Build and run
docker-compose --profile gpu up -d --build

# Check status
docker-compose ps

# View logs
docker-compose logs -f vintern-ocr-gpu

# Stop
docker-compose --profile gpu down
```

API available at: `http://localhost:11200`

## Configuration

### Environment Variables

Create `.env` file from `.env.example`:

```bash
cp .env.example .env
```

Edit `.env`:

```env
DEVICE=cuda
MODEL_NAME=5CD-AI/Vintern-1B-v3_5
MAX_FILE_SIZE=10485760
ALLOWED_ORIGINS=http://your-frontend.com
```

### Resource Limits

Edit `docker-compose.yml` to adjust:

**CPU version:**
```yaml
deploy:
  resources:
    limits:
      cpus: '4'      # Max CPU cores
      memory: 8G     # Max RAM
    reservations:
      memory: 4G     # Reserved RAM
```

**GPU version:**
```yaml
deploy:
  resources:
    limits:
      cpus: '4'
      memory: 16G
    reservations:
      memory: 8G
```

## Integration with Other Services

### Docker Network

Create a shared network for internal communication:

```bash
# Create network
docker network create internal-services

# Update docker-compose.yml
networks:
  default:
    external:
      name: internal-services
```

### Example: Connect with Another Service

```yaml
# your-other-service/docker-compose.yml
version: '3.8'

services:
  your-app:
    image: your-app:latest
    networks:
      - internal-services
    environment:
      - OCR_API_URL=http://vintern-ocr-gpu:8000

networks:
  internal-services:
    external: true
```

### Health Check

```bash
# Check if service is healthy
curl http://localhost:11200/health

# Response
{
  "status": "healthy",
  "model": "5CD-AI/Vintern-1B-v3_5",
  "device": "cuda",
  "cuda_available": true,
  "gpu_name": "NVIDIA GeForce RTX 3090"
}
```

## Production Deployment

### 1. Use GPU Version

GPU is 10-50x faster than CPU for inference.

### 2. Set CORS Properly

```env
# Don't use * in production!
ALLOWED_ORIGINS=https://app.yourdomain.com,https://admin.yourdomain.com
```

### 3. Add Reverse Proxy (NGINX)

```nginx
# nginx.conf
upstream vintern_ocr {
    server localhost:8001;
}

server {
    listen 80;
    server_name ocr.yourdomain.com;

    client_max_body_size 20M;

    location / {
        proxy_pass http://vintern_ocr;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 300s;
    }
}
```

### 4. Enable HTTPS

Use Let's Encrypt with certbot:

```bash
certbot --nginx -d ocr.yourdomain.com
```

### 5. Monitoring

Add Prometheus metrics (optional):

```bash
pip install prometheus-fastapi-instrumentator
```

Update `api.py`:

```python
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

### 6. Logging

Mount log directory:

```yaml
volumes:
  - ./logs:/app/logs
```

## Troubleshooting

### GPU Not Detected

```bash
# Check NVIDIA Docker runtime
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi

# If fails, install nvidia-docker2
sudo apt-get install nvidia-docker2
sudo systemctl restart docker
```

### Out of Memory

Reduce batch processing or limit workers:

```yaml
environment:
  - MAX_FILE_SIZE=5242880  # Reduce to 5MB
```

### Model Download Slow

Pre-download model:

```bash
# Download model to local cache
python -c "from transformers import AutoModel; AutoModel.from_pretrained('5CD-AI/Vintern-1B-v3_5', trust_remote_code=True)"

# Mount cache in docker-compose.yml
volumes:
  - ~/.cache/huggingface:/root/.cache/huggingface
```

## API Usage Examples

### Python

```python
import requests

url = "http://localhost:11200/extract"
files = {'file': open('document.jpg', 'rb')}
data = {
    'max_num': 12,
    'max_new_tokens': 4096,
    'question': 'Extract all text from this image'
}

response = requests.post(url, files=files, data=data)
result = response.json()
print(result['text'])
```

### cURL

```bash
curl -X POST http://localhost:11200/extract \
  -F "file=@document.jpg" \
  -F "max_num=12" \
  -F "max_new_tokens=4096"
```

### JavaScript/Node.js

```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

const form = new FormData();
form.append('file', fs.createReadStream('document.jpg'));
form.append('max_num', '12');
form.append('max_new_tokens', '4096');

axios.post('http://localhost:11200/extract', form, {
  headers: form.getHeaders()
}).then(response => {
  console.log(response.data.text);
});
```

## Performance Tips

1. **Use GPU**: 10-50x faster than CPU
2. **Adjust max_num**: Lower values = faster, less detail
3. **Pre-download model**: Mount cache volume
4. **Limit concurrent requests**: Use single worker
5. **Set resource limits**: Prevent OOM kills

## Support

For issues or questions:
- Check logs: `docker-compose logs -f`
- Verify health: `curl http://localhost:11200/health`
- Review configuration: `.env` file
