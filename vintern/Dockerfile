# Multi-stage build for production-ready Vintern OCR API
# Supports both CPU and GPU (CUDA)

ARG DEVICE=cuda
FROM python:3.10-slim as base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install PyTorch based on device type
ARG DEVICE
RUN if [ "$DEVICE" = "cuda" ]; then \
        pip uninstall -y torch torchvision && \
        pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cu118; \
    fi

# Copy application code
COPY api.py .

# Create directory for model cache
RUN mkdir -p /root/.cache/huggingface

# Expose port
EXPOSE 8000

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV DEVICE=${DEVICE}
ENV MAX_FILE_SIZE=10485760
ENV ALLOWED_ORIGINS=*

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
