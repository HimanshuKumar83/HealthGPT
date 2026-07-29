import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from app.rag.vector_store import retriever
from app.core.config import settings

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=settings.GEMINI_API_KEY,
    temperature=0.7,
    streaming=True
)

AGENT_SYSTEM_PROMPT = """You are 'HealthGPT', a premium AI Health Assistant. 

CORE OPERATING INSTRUCTIONS:
1. Use the provided health knowledge base context first for specific medical guidelines or documents.
2. IF the knowledge base does not have information on a specific disease or query:
   - Do NOT simply say "I don't know."
   - Instead, use your internal medical knowledge to provide helpful, evidence-based advice regarding **medical fitness, diet, and general wellness**.
   - Explicitly mention that you are providing general health information because specific local documents were not found.
3. Use Markdown formatting: bold, bullet points, and headers for readability.
4. Be empathetic and professional.
5. ALWAYS end with a medical disclaimer: "This is for informational purposes only. Please consult a doctor for clinical diagnosis." """

MAX_HISTORY_MESSAGES = 8


def _format_docs(docs) -> str:
    if not docs:
        return "No matching knowledge base documents were found."

    formatted = []
    for index, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source") or doc.metadata.get("file_path") or "knowledge base"
        formatted.append(f"[Document {index} | Source: {source}]\n{doc.page_content}")
    return "\n\n".join(formatted)


async def _build_messages(message: str, history: list = None, user_profile=None):
    docs = await retriever.ainvoke(message)
    context = _format_docs(docs)
    profile_context = ""

    if user_profile:
        profile_context = f"\n\nUSER HEALTH PROFILE:\n{user_profile}"

    messages = [
        SystemMessage(
            content=(
                f"{AGENT_SYSTEM_PROMPT}\n\n"
                f"HEALTH KNOWLEDGE BASE CONTEXT:\n{context}"
                f"{profile_context}"
            )
        )
    ]

    if history:
        for msg in history[-MAX_HISTORY_MESSAGES:]:
            content = msg["content"]
            messages.append(
                HumanMessage(content=content)
                if msg["role"] == "user"
                else AIMessage(content=content)
            )

    messages.append(HumanMessage(content=message))
    return messages


print("RAG chat initialized with direct retrieval and streaming support")


async def chat(
    session_id: str, message: str, history: list = None, user_profile=None
) -> str:
    """Standard non-streaming chat."""
    messages = await _build_messages(message, history, user_profile)
    result = await llm.ainvoke(messages)
    return result.content


async def stream_chat(
    session_id: str,
    message: str,
    history: list = None,
    user_profile: any = None,
):
    """Modern Generator for word-by-word streaming."""
    messages = await _build_messages(message, history, user_profile)

    async for chunk in llm.astream(messages):
        content = chunk.content
        if content:
            if isinstance(content, str):
                yield content
            elif isinstance(content, list):
                for part in content:
                    if isinstance(part, dict) and part.get("type") == "text":
                        yield part.get("text", "")
                    elif isinstance(part, str):
                        yield part
