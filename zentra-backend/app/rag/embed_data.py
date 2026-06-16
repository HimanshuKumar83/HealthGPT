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
    import os
    from app.rag.vector_store import embeddings, CHROMA_PATH, COLLECTION_NAME

    print("=" * 60)
    print("Embedding Pipeline starting...")
    print("=" * 60)

    # 1. Allow skipping database embedding entirely (e.g. if downloading pre-built DB)
    if os.getenv("SKIP_BUILD_EMBED", "false").lower() == "true":
        print("⏭️  SKIP_BUILD_EMBED is true. Skipping embedding pipeline.")
        return

    # 2. Check if database already exists and has documents to avoid unnecessary API usage/time
    try:
        chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
        collection = chroma_client.get_collection(COLLECTION_NAME)
        doc_count = collection.count()
        if doc_count > 0:
            print(f"✅ ChromaDB collection '{COLLECTION_NAME}' already populated with {doc_count} documents. Skipping embedding pipeline.")
            return
    except Exception as e:
        print(f"No existing collection found or error checking database: {e}. Proceeding with embedding.")

    documents = load_processed_data()
    if not documents: 
        print("⚠️  No documents found to embed.")
        return

    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    try:
        chroma_client.delete_collection(COLLECTION_NAME)
        print(f"Cleared existing collection '{COLLECTION_NAME}'")
    except: pass
    
    collection = chroma_client.create_collection(name=COLLECTION_NAME)
    
    batch_size = 100
    total_docs = len(documents)
    
    print(f"Embedding {total_docs} docs into '{COLLECTION_NAME}' in batches of {batch_size} using {embeddings.__class__.__name__}...")
    
    for i in range(0, total_docs, batch_size):
        batch = documents[i:i+batch_size]
        texts = [doc.page_content for doc in batch]
        metadatas = []
        for doc in batch:
            clean_meta = {k: str(v) for k, v in doc.metadata.items() if v is not None}
            metadatas.append(clean_meta)
        
        ids = [f"doc_{j}" for j in range(i, i + len(batch))]
        
        try:
            # Embedding documents
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
