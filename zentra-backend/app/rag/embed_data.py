import json
import time
from pathlib import Path
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from app.core.config import settings
import chromadb

def load_processed_data():
    """Load processed JSON data into LangChain documents."""
    exercises_file = Path("data/processed/exercises_processed.json")
    pdfs_file = Path("data/processed/pdfs_processed.json")
    documents = []
    
    for file in [exercises_file, pdfs_file]:
        if file.exists():
            print(f"Loading {file}...")
            with open(file, 'r', encoding='utf-8') as f:
                items = json.load(f)
                for item in items:
                    documents.append(Document(page_content=item['text'], metadata=item['metadata']))
            print(f"Loaded {len(items)} items.")
    return documents

def embed_and_store():
    print("=" * 60)
    print("Gemini API Embedding Pipeline (Memory Optimized)")
    print("=" * 60)

    if not settings.GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY missing!")
        return

    documents = load_processed_data()
    if not documents: return

    # Initialize Gemini Embeddings (API-based, zero local RAM usage)
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=settings.GEMINI_API_KEY
    )

    # Initialize ChromaDB
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    try:
        chroma_client.delete_collection("health_knowledge")
    except: pass
    
    collection = chroma_client.create_collection(name="health_knowledge")
    
    batch_size = 50 # Smaller batches for stability
    total_docs = len(documents)
    
    print(f"Embedding {total_docs} docs in batches of {batch_size}...")
    
    for i in range(0, total_docs, batch_size):
        batch = documents[i:i+batch_size]
        texts = [doc.page_content for doc in batch]
        metadatas = []
        for doc in batch:
            clean_meta = {k: str(v) for k, v in doc.metadata.items() if v is not None}
            metadatas.append(clean_meta)
        
        ids = [f"doc_{j}" for j in range(i, i + len(batch))]
        
        try:
            # Embed via API (No local RAM used)
            batch_embeddings = embeddings.embed_documents(texts)
            collection.add(
                embeddings=batch_embeddings,
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            print(f"Progress: {i + len(batch)}/{total_docs}")
            time.sleep(0.5) # Avoid API rate limits
        except Exception as e:
            print(f"Error in batch: {e}")
            time.sleep(2) # Wait and retry
            continue

    print("=" * 60)
    print(f"SUCCESS! Embedded {collection.count()} documents.")
    print("=" * 60)

if __name__ == "__main__":
    embed_and_store()
