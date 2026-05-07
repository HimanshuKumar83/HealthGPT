"""
Embed processed fitness data using LangChain + Google Gemini embeddings
Uses the officially supported 'models/embedding-001' model
"""
import json
from pathlib import Path
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from langchain_core.documents import Document
from app.core.config import settings


def load_processed_data():
    """Load all processed JSON files and convert to LangChain Documents"""
    exercises_file = Path("data/processed/exercises_processed.json")
    pdfs_file = Path("data/processed/pdfs_processed.json")
    
    documents = []
    
    # Load exercises
    if exercises_file.exists():
        print(f"Loading exercises from {exercises_file}...")
        with open(exercises_file, 'r', encoding='utf-8') as f:
            exercises = json.load(f)
        
        for item in exercises:
            # Create LangChain Document
            doc = Document(
                page_content=item['text'],
                metadata=item['metadata']
            )
            documents.append(doc)
        
        print(f"Loaded {len(exercises)} exercises")
    else:
        print(f" {exercises_file} not found, skipping exercises")
    
    # Load PDFs
    if pdfs_file.exists():
        print(f"Loading PDF chunks from {pdfs_file}...")
        with open(pdfs_file, 'r', encoding='utf-8') as f:
            pdf_chunks = json.load(f)
        
        for item in pdf_chunks:
            # Create LangChain Document
            doc = Document(
                page_content=item['text'],
                metadata=item['metadata']
            )
            documents.append(doc)
        
        print(f"Loaded {len(pdf_chunks)} PDF chunks")
    else:
        print(f" {pdfs_file} not found, skipping PDFs")
    
    return documents


def embed_and_store():
    """Main function to embed all processed data and store in ChromaDB using LangChain"""
    
    print("=" * 60)
    print("LangChain + Local Embedding Pipeline")
    print("=" * 60)
    
    # Check API key
    if not settings.GEMINI_API_KEY:
        print(" Error: GEMINI_API_KEY not found!")
        print("   Add it to your .env file")
        return
    
    # Load processed data
    print("Loading processed data...")
    documents = load_processed_data()
    
    if not documents:
        print(" No documents found to embed!")
        print("   Please run:")
        print("   - python scripts/process_exercises.py")
        print("   - python scripts/process_pdfs.py")
        return
    
    print(f"Total documents to embed: {len(documents)}")
    
    # Initialize local HuggingFace embeddings
    print("Initializing local embeddings (all-MiniLM-L6-v2)...")
    from langchain_huggingface import HuggingFaceEmbeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    # Initialize ChromaDB
    print("Initializing ChromaDB...")
    import chromadb
    
    chroma_client = chromadb.PersistentClient(path="./data/chroma_db")
           # Always start fresh when switching models
    try:
        chroma_client.delete_collection("fitness_knowledge")
        print(" Deleted old collection to start fresh with new embeddings")
    except:  # noqa: E722
        pass

    collection = chroma_client.create_collection(
        name="fitness_knowledge",
        metadata={"description": "Fitness exercises and guidelines"}
    )
    print(" Created new collection: fitness_knowledge")
    start_index = 0
    
    # Process in batches - local embeddings are fast
    batch_size = 100
    total_docs = len(documents)
    total_batches = (total_docs + batch_size - 1) // batch_size
    
    print(f"Processing {total_docs} documents in {total_batches} batches of {batch_size}")
    
    import time
    start_time = time.time()
    
    for i in range(0, total_docs, batch_size):
        batch_num = (i // batch_size) + 1
        batch = documents[i:i+batch_size]
        
        print(f"Batch {batch_num}/{total_batches} ({len(batch)} documents)...")
        
        try:
            # Extract texts and metadatas
            texts = [doc.page_content for doc in batch]
            metadatas = [doc.metadata for doc in batch]
            ids = [f"doc_{i+j}" for j in range(len(batch))]
            
            # Clean metadatas for ChromaDB
            cleaned_metadatas = []
            for metadata in metadatas:
                cleaned = {}
                for key, value in metadata.items():
                    if value is None:
                        continue
                    elif isinstance(value, list):
                        cleaned[key] = ", ".join(str(v) for v in value)
                    else:
                        cleaned[key] = str(value)
                cleaned_metadatas.append(cleaned)
            
            # Embed the batch
            batch_embeddings = embeddings.embed_documents(texts)
            
            # Add to ChromaDB
            collection.add(
                embeddings=batch_embeddings,
                documents=texts,
                metadatas=cleaned_metadatas,
                ids=ids
            )
            
            print(f" Batch {batch_num} complete!")
            
            # Breathing room for the CPU to prevent hanging
            time.sleep(1)
        
        except Exception as e:
            print(f" Error in batch {batch_num}: {e}")
            continue
    
    import time
    end_time = time.time()
    duration = end_time - start_time
    
    # Verify
    count = collection.count()
    
    print("\n" + "=" * 60)
    print("EMBEDDING COMPLETE!")
    print("=" * 60)
    print("📍 Location: ./data/chroma_db")
    print(f"Documents: {count}")
    print("Duration: {:.1f} seconds".format(duration))
    print("Model: sentence-transformers/all-MiniLM-L6-v2 (Local)")
    print("Framework: LangChain")
    print("\n💡 You can now use the RAG system in your FastAPI app!")


if __name__ == "__main__":
    embed_and_store()

