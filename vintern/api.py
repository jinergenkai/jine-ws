import io
import numpy as np
import torch
import torchvision.transforms as T
from PIL import Image
from torchvision.transforms.functional import InterpolationMode
from transformers import AutoModel, AutoTokenizer
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import logging
import traceback
import os
import argparse
import time
from contextlib import asynccontextmanager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration from environment
MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 10 * 1024 * 1024))  # 10MB default
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '*').split(',')
MODEL_NAME = os.getenv('MODEL_NAME', '5CD-AI/Vintern-1B-v3_5')

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("API starting up...")
    yield
    # Shutdown
    logger.info("API shutting down...")
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

app = FastAPI(
    title="Vintern OCR API",
    version="1.0.0",
    description="Production-ready OCR API for extracting text from images",
    lifespan=lifespan
)

# CORS middleware for internal service integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)

def build_transform(input_size):
    MEAN, STD = IMAGENET_MEAN, IMAGENET_STD
    transform = T.Compose([
        T.Lambda(lambda img: img.convert('RGB') if img.mode != 'RGB' else img),
        T.Resize((input_size, input_size), interpolation=InterpolationMode.BICUBIC),
        T.ToTensor(),
        T.Normalize(mean=MEAN, std=STD)
    ])
    return transform

def find_closest_aspect_ratio(aspect_ratio, target_ratios, width, height, image_size):
    best_ratio_diff = float('inf')
    best_ratio = (1, 1)
    area = width * height
    for ratio in target_ratios:
        target_aspect_ratio = ratio[0] / ratio[1]
        ratio_diff = abs(aspect_ratio - target_aspect_ratio)
        if ratio_diff < best_ratio_diff:
            best_ratio_diff = ratio_diff
            best_ratio = ratio
        elif ratio_diff == best_ratio_diff:
            if area > 0.5 * image_size * image_size * ratio[0] * ratio[1]:
                best_ratio = ratio
    return best_ratio

def dynamic_preprocess(image, min_num=1, max_num=12, image_size=448, use_thumbnail=False):
    orig_width, orig_height = image.size
    aspect_ratio = orig_width / orig_height

    target_ratios = set(
        (i, j) for n in range(min_num, max_num + 1) for i in range(1, n + 1) for j in range(1, n + 1) if
        i * j <= max_num and i * j >= min_num)
    target_ratios = sorted(target_ratios, key=lambda x: x[0] * x[1])

    target_aspect_ratio = find_closest_aspect_ratio(
        aspect_ratio, target_ratios, orig_width, orig_height, image_size)

    target_width = image_size * target_aspect_ratio[0]
    target_height = image_size * target_aspect_ratio[1]
    blocks = target_aspect_ratio[0] * target_aspect_ratio[1]

    resized_img = image.resize((target_width, target_height))
    processed_images = []
    for i in range(blocks):
        box = (
            (i % (target_width // image_size)) * image_size,
            (i // (target_width // image_size)) * image_size,
            ((i % (target_width // image_size)) + 1) * image_size,
            ((i // (target_width // image_size)) + 1) * image_size
        )
        split_img = resized_img.crop(box)
        processed_images.append(split_img)
    assert len(processed_images) == blocks
    if use_thumbnail and len(processed_images) != 1:
        thumbnail_img = image.resize((image_size, image_size))
        processed_images.append(thumbnail_img)
    return processed_images

def process_image(image: Image.Image, input_size=448, max_num=12):
    transform = build_transform(input_size=input_size)
    images = dynamic_preprocess(image, image_size=input_size, use_thumbnail=True, max_num=max_num)
    pixel_values = [transform(image) for image in images]
    pixel_values = torch.stack(pixel_values)
    return pixel_values

# Device configuration
# Priority: Command line args > Environment variable > Auto-detect
def get_device():
    # Check environment variable
    force_device = os.getenv('DEVICE', None)

    if force_device:
        force_device = force_device.lower()
        if force_device == 'cpu':
            print("DEVICE=cpu set in environment - forcing CPU mode")
            return torch.device('cpu')
        elif force_device == 'cuda':
            if torch.cuda.is_available():
                print("DEVICE=cuda set in environment - using GPU")
                return torch.device('cuda')
            else:
                print("WARNING: DEVICE=cuda set but CUDA not available, falling back to CPU")
                return torch.device('cpu')

    # Auto-detect
    if torch.cuda.is_available():
        return torch.device('cuda')
    else:
        return torch.device('cpu')

device = get_device()
print(f"Using device: {device}")
if device.type == 'cuda':
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"CUDA Version: {torch.version.cuda}")

logger.info(f"Loading model: {MODEL_NAME}")
if device.type == 'cuda':
    model = AutoModel.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.bfloat16,
        low_cpu_mem_usage=True,
        trust_remote_code=True,
        use_flash_attn=False,
    ).eval().cuda()
else:
    logger.info("Loading model on CPU (this will be slower)...")
    model = AutoModel.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float32,
        low_cpu_mem_usage=True,
        trust_remote_code=True,
        use_flash_attn=False,
    ).eval()

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True, use_fast=False)
logger.info(f"Model loaded successfully! Max file size: {MAX_FILE_SIZE / 1024 / 1024:.1f}MB")

class OCRResponse(BaseModel):
    text: str
    question: str
    inference_time: float
    total_time: float

@app.get("/")
async def root():
    return {"message": "Vintern OCR API is running", "version": "1.0.0"}

@app.post("/extract", response_model=OCRResponse)
async def extract_text(
    file: UploadFile = File(...),
    question: Optional[str] = Form(None),
    max_num: int = Form(3),
    max_new_tokens: int = Form(2048)
):
    """
    Extract text from an uploaded image.

    Parameters:
    - file: Image file to process
    - question: Custom question (default: Trích xuất đầy đủ toàn bộ ra dữ liệu)
    - max_num: Maximum number of image blocks (default: 6)
    - max_new_tokens: Maximum length of output text (default: 4096)
    """
    start_time = time.time()

    if file.content_type and not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        logger.info(f"Receiving file: {file.filename}")
        contents = await file.read()

        # Validate file size
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Max size: {MAX_FILE_SIZE / 1024 / 1024:.1f}MB"
            )

        logger.info(f"File size: {len(contents)} bytes ({len(contents) / 1024:.1f}KB)")

        image = Image.open(io.BytesIO(contents)).convert('RGB')
        logger.info(f"Image size: {image.size}")

        dtype = torch.bfloat16 if device.type == 'cuda' else torch.float32
        logger.info(f"Processing image with dtype: {dtype}, device: {device}")
        pixel_values = process_image(image, max_num=max_num).to(dtype).to(device)
        logger.info(f"Pixel values shape: {pixel_values.shape}")

        if question is None:
            question = '<image>\nTrích xuất đầy đủ toàn bộ ra dữ liệu'
        else:
            question = f'<image>\n{question}'

        logger.info(f"Question: {question}")

        generation_config = dict(
            max_new_tokens=max_new_tokens,
            do_sample=False,
            num_beams=3,
            repetition_penalty=2.0,
        )

        logger.info("Starting inference...")
        inference_start = time.time()
        response, history = model.chat(
            tokenizer,
            pixel_values,
            question,
            generation_config,
            history=None,
            return_history=True
        )
        inference_time = time.time() - inference_start
        total_time = time.time() - start_time

        logger.info(f"Inference complete. Response length: {len(response)} chars")
        logger.info(f"Timing - Inference: {inference_time:.2f}s, Total: {total_time:.2f}s")

        return OCRResponse(
            text=response,
            question=question,
            inference_time=round(inference_time, 2),
            total_time=round(total_time, 2)
        )

    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model": "5CD-AI/Vintern-1B-v3_5",
        "device": str(device),
        "cuda_available": torch.cuda.is_available(),
        "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
