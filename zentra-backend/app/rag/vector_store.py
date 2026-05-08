import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from app.core.config import settings

# 1. Use Gemini Embeddings (Fast, API-based, zero RAM usage)
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=settings.GEMINI_API_KEY
)

# 2. Initialize ChromaDB
CHROMA_PATH = "chroma_db"
vector_store = Chroma(
    collection_name="health_knowledge",
    embedding_function=embeddings,
    persist_directory=CHROMA_PATH
)

retriever = vector_store.as_retriever(search_kwargs={"k": 5})
