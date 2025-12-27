# Vintern OCR API

Simple OCR API using Vintern-1B-v3_5 model.

## Quick Start

### Using Makefile (Recommended)

```bash
make cpu    # Run CPU version
make gpu    # Run GPU version
make stop   # Stop service
make logs   # View logs
make health # Check health
make clean  # Clean everything
```

### Using docker-compose

```bash
# CPU
docker-compose --profile cpu up -d --build

# GPU
docker-compose --profile gpu up -d --build
```

API: `http://localhost:11200`

## Usage

```bash
# Health check
curl http://localhost:11200/health

# Extract text
curl -X POST http://localhost:11200/extract \
  -F "file=@image.jpg" \
  -F "max_num=12" \
  -F "max_new_tokens=4096"
```

## Commands

| Command | Description |
|---------|-------------|
| `make cpu` | Start CPU version |
| `make gpu` | Start GPU version |
| `make stop` | Stop all services |
| `make logs` | View logs |
| `make health` | Check API health |
| `make test` | Test with sample image |
| `make clean` | Remove all containers & images |

## Without Docker

See `INSTALL.md` for Python installation.
