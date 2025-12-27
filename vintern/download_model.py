#!/usr/bin/env python
"""
Download Vintern model to local cache
This will speed up first Docker run
"""

from transformers import AutoModel, AutoTokenizer
import os

MODEL_NAME = "5CD-AI/Vintern-1B-v3_5"

print(f"Downloading model: {MODEL_NAME}")
print("This may take 5-10 minutes depending on your internet speed...")
print("")

# Download model
print("Downloading model files...")
model = AutoModel.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True,
    low_cpu_mem_usage=True
)
print("✓ Model downloaded")

# Download tokenizer
print("Downloading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True
)
print("✓ Tokenizer downloaded")

# Show cache location
cache_dir = os.path.expanduser("~/.cache/huggingface")
print(f"\n✓ Model cached at: {cache_dir}")
print(f"✓ Docker will use this cache when you run 'make cpu' or 'make gpu'")
print("\nYou can now run: make cpu")
