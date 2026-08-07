# Prompt Engineering Report - HealthGPT

## 1. Core System Prompt Strategy

The system prompt defines the AI assistant's persona, operating parameters, and limitations:

```
You are 'HealthGPT', a premium AI Health Assistant. 

CORE OPERATING INSTRUCTIONS:
1. Use the provided health knowledge base context first for specific medical guidelines or documents.
2. IF the knowledge base does not have information on a specific disease or query:
   - Do NOT simply say "I don't know."
   - Instead, use your internal medical knowledge to provide helpful, evidence-based advice regarding medical fitness, diet, and general wellness.
   - Explicitly mention that you are providing general health information because specific local documents were not found.
3. Use Markdown formatting: bold, bullet points, and headers for readability.
4. Be empathetic and professional.
5. ALWAYS end with a medical disclaimer: "This is for informational purposes only. Please consult a doctor for clinical diagnosis."
```

## 2. Dynamic Prompt Merging

To ensure context-aware responses, the backend builds dynamic prompts by combining multiple data sources:

```
[System Message]
  - Core Operating Persona
  - ChromaDB Context (Top-3 relevant chunks + citation metadata)
  - User Health Profile (Demographics, lifestyle, and medical parameters)

[Chat History (Max 8 Messages)]
  - User: "I feel tired constantly."
  - Assistant: "Based on WHO Guidelines on Nutrition..."

[Current Query]
  - User: "Could it be iron deficiency?"
```

## 3. Model Parameters & Hallucination Mitigation

| Parameter | Value | Rationale |
| :--- | :--- | :--- |
| **Model** | `gemini-2.5-flash` | Selected for high-speed generation, context window capabilities, and structured citation processing. |
| **Temperature** | `0.7` | Balances natural language flow with clinical consistency. |
| **Max History Length** | `8 messages` | Retains context while preventing context drift or token bloat. |
| **Top-K Retrieval** | `3 chunks` | Ensures high-relevancy context is retrieved without cluttering the prompt window. |

---

## 4. Citation and Safety Guardrails

- **Citations**: Source references (such as `[Document 1 | Source: Healthy diet who.pdf]`) are injected directly into the system prompt's context layer. The model is instructed to cite these sources when referencing guideline documents.
- **Safety Fallback**: If the query falls outside the vector store's data, the model provides general wellness information and fallbacks to its internal database rather than generating inaccurate answers or rejecting the query.
- **Disclaimer Injection**: Every chat completion ends with a mandatory medical disclaimer to ensure user safety.
