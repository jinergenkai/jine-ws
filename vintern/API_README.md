# Vintern OCR API

A FastAPI-based web service for extracting text from images using the Vintern-1B-v3_5 model.

## Installation

```bash
pip install -r requirements.txt
```

## Running the API

```bash
python api.py
```

Or using uvicorn directly:

```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### GET `/`
Root endpoint - returns API information

### POST `/extract`
Extract text from an uploaded image

**Parameters:**
- `file` (required): Image file to process
- `question` (optional): Custom question about the image
- `max_num` (optional): Maximum number of image blocks (default: 6)

**Response:**
```json
{
  "text": "Extracted text content",
  "question": "The question that was asked"
}
```

### GET `/health`
Health check endpoint

## Usage Examples

### Using Python requests

```python
import requests

with open('image.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/extract', files=files)
    result = response.json()
    print(result['text'])
```

### Using curl

```bash
curl -X POST "http://localhost:8000/extract" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test-image.jpg"
```

### With custom question

```bash
curl -X POST "http://localhost:8000/extract" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test-image.jpg" \
  -F "question=Describe this image in detail"
```

### Using the client example

```python
python client_example.py
```

## API Documentation

Once the server is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Requirements

- CUDA-capable GPU
- Python 3.8+
- All dependencies listed in `requirements.txt`

## Notes

- The model will be downloaded automatically on first run
- Images are automatically converted to RGB format
- Default question is in Vietnamese: "Trích xuất thông tin chính trong ảnh và trả về dạng markdown."

