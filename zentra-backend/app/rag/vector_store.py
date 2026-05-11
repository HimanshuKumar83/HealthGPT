import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from app.core.config import settings

# Reverting to Local Embeddings for local development
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Initialize ChromaDB
CHROMA_PATH = "chroma_db"
vector_store = Chroma(
    collection_name="health_knowledge",
    embedding_function=embeddings,
    persist_directory=CHROMA_PATH
)

retriever = vector_store.as_retriever(search_kwargs={"k": 5})
