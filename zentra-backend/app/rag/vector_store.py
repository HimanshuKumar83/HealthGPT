import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from app.core.config import settings

# Determine which embeddings to use
EMBEDDING_TYPE = os.getenv("EMBEDDING_TYPE", "huggingface" if settings.ENVIRONMENT == "development" else "google")

if EMBEDDING_TYPE == "google":
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=settings.GEMINI_API_KEY
    )
    CHROMA_PATH = os.getenv("CHROMA_PATH", "chroma_db")
    COLLECTION_NAME = os.getenv("CHROMA_COLLECTION", "health_knowledge")
    print("Initializing ChromaDB with Google Generative AI Embeddings")
else:
    from langchain_huggingface import HuggingFaceEmbeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    CHROMA_PATH = os.getenv("CHROMA_PATH", "data/chroma_db")
    COLLECTION_NAME = os.getenv("CHROMA_COLLECTION", "fitness_knowledge")
    print(f"Initializing ChromaDB with Local HuggingFace Embeddings at {CHROMA_PATH} (Collection: {COLLECTION_NAME})")

# Initialize ChromaDB
vector_store = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings,
    persist_directory=CHROMA_PATH
)

retriever = vector_store.as_retriever(search_kwargs={"k": 5})
