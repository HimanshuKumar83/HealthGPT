import os
import requests
from pathlib import Path

# Set this in Railway environment variables
MODEL_DOWNLOAD_URL = os.getenv("MODEL_DOWNLOAD_URL", "")

BASE_DIR = Path(__file__).parent

MODEL_FILES = [
    "label_encoders.pkl",
    "target_label_encoder.pkl",
    "robust_scaler.pkl",
    "feature_columns.pkl",
    "random_forest_model.pkl"
]

def download_models():
    """Download ML models from a URL if they don't exist locally"""
    if not MODEL_DOWNLOAD_URL:
        print("⚠️  MODEL_DOWNLOAD_URL not set. Skipping model download.")
        return
    
    for filename in MODEL_FILES:
        filepath = BASE_DIR / filename
        
        if filepath.exists():
            print(f"✅ {filename} already exists")
            continue
        
        try:
            print(f"📥 Downloading {filename}...")
            url = f"{MODEL_DOWNLOAD_URL}/{filename}"
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Downloaded {filename}")
        except Exception as e:
            print(f"❌ Failed to download {filename}: {e}")

if __name__ == "__main__":
    download_models()
