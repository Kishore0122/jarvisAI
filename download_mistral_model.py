#!/usr/bin/env python3
"""
Download Mistral 7B GGUF Model
Downloads a properly quantized Mistral model for better performance
"""

import os
import sys
import requests
import hashlib
from pathlib import Path
from tqdm import tqdm

def download_file(url: str, filename: str, expected_size: int = None):
    """Download a file with progress bar and verification"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(filename, 'wb') as f:
            with tqdm(total=total_size, unit='B', unit_scale=True, desc=filename) as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))
        
        # Verify file size
        actual_size = os.path.getsize(filename)
        if expected_size and actual_size != expected_size:
            print(f"⚠️ Warning: File size mismatch. Expected: {expected_size}, Got: {actual_size}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error downloading {filename}: {e}")
        return False

def main():
    """Download Mistral model"""
    print("🤖 Mistral 7B Model Downloader")
    print("=" * 50)
    
    # Create models directory
    models_dir = Path("models/llm")
    models_dir.mkdir(parents=True, exist_ok=True)
    
    # Model options (choose one)
    models = {
        "mistral-7b-instruct-v0.2.Q4_K_M.gguf": {
            "url": "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
            "size": 4.37 * 1024**3,  # ~4.37 GB
            "description": "Mistral 7B Instruct v0.2 (Q4_K_M quantization)"
        },
        "mistral-7b-instruct-v0.1.Q4_K_M.gguf": {
            "url": "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
            "size": 4.37 * 1024**3,  # ~4.37 GB
            "description": "Mistral 7B Instruct v0.1 (Q4_K_M quantization)"
        }
    }
    
    print("Available models:")
    for i, (model_name, info) in enumerate(models.items(), 1):
        print(f"{i}. {model_name}")
        print(f"   {info['description']}")
        print(f"   Size: {info['size'] / (1024**3):.2f} GB")
        print()
    
    # Let user choose
    try:
        choice = input("Enter model number (1-2) or press Enter for default (1): ").strip()
        if not choice:
            choice = "1"
        
        choice_idx = int(choice) - 1
        if choice_idx < 0 or choice_idx >= len(models):
            print("❌ Invalid choice")
            return
        
        model_name = list(models.keys())[choice_idx]
        model_info = models[model_name]
        
    except (ValueError, IndexError):
        print("❌ Invalid choice, using default")
        model_name = "mistral-7b-instruct-v0.2.Q4_K_M.gguf"
        model_info = models[model_name]
    
    model_path = models_dir / model_name
    
    # Check if model already exists
    if model_path.exists():
        file_size = model_path.stat().st_size
        expected_size = model_info['size']
        
        if abs(file_size - expected_size) < 1024**2:  # Within 1MB
            print(f"✅ Model already exists: {model_name}")
            print(f"   Size: {file_size / (1024**3):.2f} GB")
            return
        else:
            print(f"⚠️ Model exists but size doesn't match. Re-downloading...")
            model_path.unlink()
    
    print(f"📥 Downloading {model_name}...")
    print(f"   URL: {model_info['url']}")
    print(f"   Size: {model_info['size'] / (1024**3):.2f} GB")
    print()
    
    # Download the model
    success = download_file(
        model_info['url'], 
        str(model_path), 
        int(model_info['size'])
    )
    
    if success:
        print(f"✅ Model downloaded successfully: {model_name}")
        print(f"   Location: {model_path}")
        print()
        print("🎉 You can now run your assistant with:")
        print("   python -m core.assistant")
    else:
        print("❌ Failed to download model")
        print("💡 Try downloading manually from:")
        print(f"   {model_info['url']}")

if __name__ == "__main__":
    main() 