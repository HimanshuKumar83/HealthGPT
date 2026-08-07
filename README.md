# HealthGPT (Zentra) - Premium AI-Powered RAG Health Assistant & Lifestyle Dashboard

HealthGPT is a premium healthcare web application combining **RAG-based Generative AI assistant capabilities** and **automated machine learning risk models** to deliver data-driven clinical information, wellness dashboards, and obesity prediction alerts. It embeds World Health Organization (WHO) medical manuals directly into a local semantic index to guarantee citation-grade, context-aware information.


## Core Features

- 🏥 **Evidence-Based Healthcare Chatbot**: Dynamic context retrieval (Top-K=3) from WHO textbooks.
- ⚡ **Real-Time Word-By-Word Streaming**: Uses Server-Sent Events (SSE) for sub-second latency.
- ⚖️ **Obesity Risk Classifier**: Random Forest Classifier evaluating 16 lifestyle parameters.
- 📊 **Wellness Dashboard**: Responsive visualizations showing BMI categories and lifestyle factors.
- 🔒 **Enterprise-Grade Auth**: JWT-based stateless authentication with password hashing.
- 📜 **Source Citations**: Injects source file identifiers directly into conversational structures.
- 🛑 **Integrated Safety Disclaimer**: Hardcoded constraints preventing medical diagnostics.

---

## Folder Structure

```
├── docs/                    # Step-by-step local setup, architecture, and project logic documents
├── presentation/            # 5-slide outline structures, speaking transcripts, and demo scripts
├── report/                  # Capstone project report (academic formatting)
├── deployment/              # Dockerfile, docker-compose, Render blueprints, and Vercel json routing
├── testing/                 # API, prompt engine, UI, security, and edge test cases
├── zentra-backend/          # Backend APIs and RAG modules
│   ├── app/
│   │   ├── api/             # Routers (Auth, Chat, Predict)
│   │   ├── core/            # Security configurations
│   │   ├── db/              # SQLAlchemy database structures
│   │   ├── ml/              # RandomForest model and scaler
│   │   └── rag/             # RAG chain pipelines and vector stores
│   └── data/                # WHO guidelines and source PDFs
└── zentra-ui/               # Single Page Application
    ├── src/
    │   ├── components/      # UI components
    │   ├── pages/           # Pages (Dashboard, Results)
    │   └── store/           # Zustand state management
```

---

## Step-by-Step Local Setup Guide

Follow this guide to get the project running locally on your laptop.

### 1. Open and Split Terminal (VS Code Shortcut)
- Press `Ctrl + Shift + ` ` (Backtick) to open the terminal panel.
- Press `Ctrl + Shift + 5` to split the terminal into two side-by-side terminal instances:
  - **Left Terminal**: For the FastAPI Backend.
  - **Right Terminal**: For the React Frontend.

### 2. Configure Environment Variables (`.env`)

#### In the Backend Folder (`zentra-backend/.env`)
Navigate to `zentra-backend/` in the left terminal and create a `.env` file containing:
```env
ENVIRONMENT=development
APP_HOST=127.0.0.1
APP_PORT=8000

SECRET_KEY=9a7bcf308291df13192080a2b534cf661908d132a
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=600

DATABASE_URL=sqlite+aiosqlite:///./local_mydb.db
EMBEDDING_TYPE=huggingface
CHROMA_PATH=data/chroma_db
CHROMA_COLLECTION=fitness_knowledge
RAG_TOP_K=3

GEMINI_API_KEY=your_gemini_api_key_here
```
*Note: Make sure to replace `your_gemini_api_key_here` with a valid API key from Google AI Studio (https://aistudio.google.com/).*

#### In the Frontend Folder (`zentra-ui/.env`)
Navigate to `zentra-ui/` in the right terminal and create a `.env` file containing:
```env
VITE_API_URL=http://localhost:8000
```

---

### 3. Launch the Services

#### Start Backend (Left Terminal)
```bash
cd zentra-backend
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
python app/ml/train_dummy_models.py
python app/rag/embed_data.py
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

#### Start Frontend (Right Terminal)
```bash
cd zentra-ui
npm install
npm run dev
```

---

### 4. Interactive Walkthrough Flow
1. **Register & Log In**: Open `http://localhost:5173`, click **Get Started**, register a new account, and sign in.
2. **Onboarding Form**: Complete the health and lifestyle onboarding questionnaire to create your user profile.
3. **View Obesity Level**: Navigate to the Results tab to view your obesity risk level and personalized recommendations.
4. **Chat with Assistant**: Switch to the Chat Assistant tab and query the bot (e.g., *"What is a healthy diet according to WHO guidelines?"*). Watch the response stream back in real-time with citations.

---

## License & Disclaimer
Distributed under the MIT License. See `LICENSE` for details. HealthGPT is an academic assignment and is for informational purposes only. It does not provide medical diagnoses or replace clinical consultations.
