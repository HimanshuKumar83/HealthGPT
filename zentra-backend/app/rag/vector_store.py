from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from app.core.config import settings

# Free local embeddings that don't require an API key or quota
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = Chroma(
    collection_name="fitness_knowledge",
    embedding_function=embeddings,
    persist_directory="./data/chroma_db",
)

retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})

print(f"Vector store loaded: {vectorstore._collection.count()} documents")
