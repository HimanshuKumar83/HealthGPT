import logging
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import create_retriever_tool
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from app.rag.vector_store import retriever
from app.core.config import settings

# 1. Initialize LLM with streaming enabled
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=settings.GEMINI_API_KEY,
    temperature=0.7,
    streaming=True
)

# 2. Create the Retriever Tool
retriever_tool = create_retriever_tool(
    retriever=retriever,
    name="health_knowledge_base",
    description="Search the comprehensive health knowledge base including WHO guidelines, medical standards, disease treatments (Malaria, TB, HIV, etc.), nutrition, and fitness advice. Always use this tool for ANY health-related query.",
)

AGENT_SYSTEM_PROMPT = """You are 'HealthGPT', a premium AI Health Assistant. 

CORE OPERATING INSTRUCTIONS:
1. ALWAYS use the 'health_knowledge_base' tool first to search for specific medical guidelines or documents.
2. IF the knowledge base does not have information on a specific disease or query:
   - Do NOT simply say "I don't know."
   - Instead, use your internal medical knowledge to provide helpful, evidence-based advice regarding **medical fitness, diet, and general wellness**.
   - Explicitly mention that you are providing general health information because specific local documents were not found.
3. Use Markdown formatting: bold, bullet points, and headers for readability.
4. Be empathetic and professional.
5. ALWAYS end with a medical disclaimer: "This is for informational purposes only. Please consult a doctor for clinical diagnosis." """

# 3. Create the Modern ReAct Agent (LangGraph)
# Removed state_modifier to ensure compatibility with older LangGraph versions
agent = create_react_agent(
    llm,
    tools=[retriever_tool]
)

print("Modern RAG agent initialized with full streaming support")


async def chat(
    session_id: str, message: str, history: list = None, user_profile=None
) -> str:
    """Standard non-streaming chat."""
    messages = [SystemMessage(content=AGENT_SYSTEM_PROMPT)]
    
    if history:
        for msg in history:
            messages.append(HumanMessage(content=msg["content"]) if msg["role"] == "user" else AIMessage(content=msg["content"]))
    
    messages.append(HumanMessage(content=message))
    
    result = await agent.ainvoke({"messages": messages})
    return result["messages"][-1].content


async def stream_chat(
    session_id: str,
    message: str,
    history: list = None,
    user_profile: any = None,
):
    """Modern Generator for word-by-word streaming."""
    # Prepend the system prompt manually to the message list
    messages = [SystemMessage(content=AGENT_SYSTEM_PROMPT)]
    
    if history:
        for msg in history:
            role, content = msg["role"], msg["content"]
            messages.append(HumanMessage(content=content) if role == "user" else AIMessage(content=content))

    messages.append(HumanMessage(content=message))

    # Use astream_events v2 - the official way to stream LangGraph agents
    async for event in agent.astream_events({"messages": messages}, version="v2"):
        kind = event["event"]
        
        # This catches the tokens directly from the LLM inside the agent
        if kind == "on_chat_model_stream":
            content = event["data"].get("chunk", {}).content
            if content:
                if isinstance(content, str):
                    yield content
                elif isinstance(content, list):
                    for part in content:
                        if isinstance(part, dict) and part.get("type") == "text":
                            yield part.get("text", "")
                        elif isinstance(part, str):
                            yield part
