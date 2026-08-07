# Local Setup Guide - HealthGPT

Follow this step-by-step guide to set up and run HealthGPT (Zentra) locally on any laptop.

---

## Step 1: Clone the Repository & Open Terminal
Open your project directory (`HealthGPT`) in your favorite editor (e.g., VS Code). 

*Shortcut to split/open terminal panel in VS Code:*
- Press `Ctrl + Shift + ` ` (Backtick) to open the terminal panel.
- Press `Ctrl + Shift + 5` to split the terminal panel into two side-by-side terminal instances (one for the Backend, one for the Frontend).

---

## Step 2: Configure Environment Variables

### 1. Backend `.env` File
In your first terminal, navigate to the backend directory and create a `.env` file:
```bash
cd zentra-backend
```
Create a file named `.env` and add the following keys. Make sure to replace `your_gemini_api_key_here` with a valid key from Google AI Studio (https://aistudio.google.com/):

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

### 2. Frontend `.env` File
Switch to the second terminal, navigate to the frontend directory:
```bash
cd zentra-ui
```
Create a file named `.env` and add the backend API URL:
```env
VITE_API_URL=http://localhost:8000
```

---

## Step 3: Run the Backend & Populate Vector DB
In the **first terminal** (`zentra-backend` folder):

1. **Create and Activate Python Virtual Environment**:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
2. **Install Backend Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Download ML Models & Pre-populate Vector Database**:
   ```bash
   python app/ml/train_dummy_models.py
   python app/rag/embed_data.py
   ```
4. **Start the FastAPI Server**:
   ```bash
   uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```

---

## Step 4: Run the Frontend
In the **second terminal** (`zentra-ui` folder):

1. **Install Frontend Dependencies**:
   ```bash
   npm install
   ```
2. **Start the Development Server**:
   ```bash
   npm run dev
   ```
3. **Open the App**: Click the local URL printed in the terminal (usually `http://localhost:5173`).

---

## Step 5: Verification & Initial Walkthrough Flow
1. **Register & Sign In**: Open the web app, click **Get Started** or **Login**, and register a new account.
2. **Complete Onboarding (Health Profile)**: After registering, complete the health onboarding questionnaire. Enter your metrics (height, weight, age, exercise habits, diet parameters). Saving this creates your persistent health profile.
3. **Review ML Risk Level**: Navigate to the Results tab in the dashboard to see your predicted obesity classification level displayed on the speedometer gauge.
4. **Start Chatting**: Open the Health Assistant chat tab and enter queries (e.g., *"What is a balanced diet according to WHO guidelines?"*). The assistant will stream replies back with source citations.
