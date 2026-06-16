import os
import requests
from pathlib import Path

CHROMA_DOWNLOAD_URL = os.getenv("CHROMA_DOWNLOAD_URL", "")
CHROMA_PATH = os.getenv("CHROMA_PATH", "data/chroma_db")

def download_chroma():
    if not CHROMA_DOWNLOAD_URL:
        print("⚠️ CHROMA_DOWNLOAD_URL not set. Skipping pre-embedded database download.")
        return

    db_dir = Path(CHROMA_PATH)
    db_dir.mkdir(parents=True, exist_ok=True)
    filepath = db_dir / "chroma.sqlite3"

    if filepath.exists():
        print(f"✅ {filepath} already exists")
        return

    try:
        print(f"📥 Downloading pre-embedded ChromaDB from {CHROMA_DOWNLOAD_URL}...")
        response = requests.get(CHROMA_DOWNLOAD_URL, stream=True, timeout=60)
        response.raise_for_status()

        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"✅ Downloaded and saved ChromaDB to {filepath}")
    except Exception as e:
        print(f"❌ Failed to download ChromaDB: {e}")

if __name__ == "__main__":
    download_chroma()
