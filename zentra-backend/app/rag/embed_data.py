import json
import time
from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
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
    print("Local Embedding Pipeline (Reverted for Local Run)")
    print("=" * 60)

    documents = load_processed_data()
    if not documents: return

    # Reverting to Local Embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Initialize ChromaDB
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    try:
        chroma_client.delete_collection("health_knowledge")
    except: pass
    
    collection = chroma_client.create_collection(name="health_knowledge")
    
    batch_size = 100
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
            # Local embedding (Uses your computer's power)
            batch_embeddings = embeddings.embed_documents(texts)
            collection.add(
                embeddings=batch_embeddings,
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            print(f"Progress: {i + len(batch)}/{total_docs}")
        except Exception as e:
            print(f"Error in batch: {e}")
            continue

    print("=" * 60)
    print(f"SUCCESS! Embedded {collection.count()} documents.")
    print("=" * 60)

if __name__ == "__main__":
    embed_and_store()
