# Architecture Presentation Contents & Scripts

This document contains slide content outlines, a 3-minute speaking script, and a demo walkthrough script for presenting the HealthGPT project.

## 1. 5-Slide Presentation Outline

### Slide 1: Project Overview
- **Title**: HealthGPT: Intelligent Healthcare RAG Assistant & Wellness Platform
- **Subtitle**: Personalized Clinical Advice and Obesity Risk Classification
- **Content**:
  - Addresses healthcare accessibility challenges by combining RAG and machine learning.
  - Features a patient-centric React SPA dashboard with a responsive layout.
  - Integrated RAG chatbot backed by official WHO guidelines.
  - Automated obesity classifier model using lifestyle profiles.

---

### Slide 2: System Architecture
- **Title**: Decoupled System Architecture
- **Content**:
  - **Frontend SPA**: React (Vite, TypeScript, Tailwind CSS) for smooth UI interactions.
  - **Backend Server**: FastAPI backend managing database routing and streaming APIs.
  - **Vector DB**: ChromaDB storing embedded WHO manuals for semantic document retrieval.
  - **Relational Storage**: PostgreSQL managing user credentials, profiles, and chat sessions.

---

### Slide 3: RAG & ML Processing Workflow
- **Title**: Hybrid Processing Workflow (RAG & ML)
- **Content**:
  - **RAG Pipeline**: Resolves user queries by retrieving context from local documents, generating responses via Gemini 2.5 Flash, and streaming tokens back via SSE.
  - **ML Pipeline**: Normalizes user profile metrics using a Robust Scaler and runs inference via a Random Forest model to calculate obesity risks.

---

### Slide 4: Technology Stack & Core Features
- **Title**: Technology Stack & Core Integrations
- **Content**:
  - **Core Technologies**: React, FastAPI, PostgreSQL, Redis.
  - **Generative AI**: LangChain, Gemini 2.5 Flash (`models/embedding-001`).
  - **Machine Learning**: RandomForestClassifier, Scikit-learn, joblib.
  - **Security**: JWT stateless authentication and password hashing.

---

### Slide 5: Challenges, Results, and Future Scope
- **Title**: Challenges, Results, and Future Scope
- **Content**:
  - **Key Achievements**: Low-latency RAG response streaming and robust ML predictions.
  - **Project Challenges**: Handling medical terminology matching and processing sparse data.
  - **Future Scope**: Multimodal inputs (e.g. food logging via images) and medical API integrations.

---

## 2. 3-Minute Presentation Speaking Script

*"Good morning, everyone. Today, I am excited to present **HealthGPT**, a health and wellness platform designed to bridge the gap between complex medical manuals and accessible clinical information.*

*Let's start with **Slide 1**. HealthGPT is a patient-centric application designed to address health information accessibility. It features a responsive React dashboard, an automated obesity classifier, and a RAG-powered health assistant.*

*Moving to **Slide 2**, the system uses a decoupled architecture. The frontend is a React single-page application built with Vite and Tailwind CSS. The FastAPI backend serves as the core coordinator, managing secure JWT authentication, PostgreSQL user storage, Redis cache lookups, and ChromaDB vector queries.*

*On **Slide 3**, we look at the RAG and Machine Learning workflows. When a user asks a question, the system queries ChromaDB to retrieve relevant context from WHO documents. This context is combined with the user's profile and chat history, and sent to Gemini 2.5 Flash, which streams responses back to the client in real-time. For risk assessment, the ML pipeline processes 16 lifestyle parameters through a Robust Scaler and uses a Random Forest Classifier to calculate obesity risk levels.*

***Slide 4** outlines our technology stack. We use LangChain for our RAG pipelines, Google Gemini for LLM completions, and Scikit-learn for our local machine learning model. Security is managed via stateless JWT tokens.*

*Finally, on **Slide 5**, we highlight our results and future plans. We achieved low-latency response streaming and accurate risk predictions. Next steps include adding multimodal inputs, such as image-based food logging, and integrating with external medical APIs. Thank you."*

---

## 3. 3-Minute Demo Walkthrough Script

### 0:00 - 0:30 | Introduction & Login
- **Visual**: Show landing page. Highlight the clean, responsive layout. Click "Login".
- **Audio**: *"Welcome to the HealthGPT demo. We start on our landing page, which outlines the platform's key features. Clicking 'Login' takes us to our authentication page, where users can securely access their accounts using JWT-validated credentials."*

### 0:30 - 1:15 | Onboarding & Profile Setup
- **Visual**: Show the onboarding form. Enter details (height, weight, physical activity, alcohol consumption, etc.) and save.
- **Audio**: *"First-time users complete an onboarding questionnaire. This captures demographic details, dietary habits, and activity levels. This information is saved to PostgreSQL to personalize the RAG assistant's responses and run our machine learning models."*

### 1:15 - 2:00 | Obesity Classification Result
- **Visual**: Navigate to the Results page. Show the speedometer gauge indicating the predicted category (e.g. "Normal Weight" or "Obesity Type I") along with dynamic recommendations.
- **Audio**: *"Our results page features a speedometer gauge displaying the user's obesity risk level, calculated by our Random Forest model. It also provides tailored dietary and activity recommendations based on the user's profile."*

### 2:00 - 2:45 | Healthcare RAG Assistant
- **Visual**: Open a chat session and send a query: "What are the key guidelines for a healthy diet?" Show the response streaming in real-time with source citations and a medical disclaimer.
- **Audio**: *"Next is our health assistant. When we ask about dietary guidelines, the system retrieves relevant chunks from WHO documents in ChromaDB, combines them with the user's profile, and streams the response back with clear source citations and safety disclaimers."*

### 2:45 - 3:00 | Session History & Logout
- **Visual**: Show the chat history sidebar, switch sessions, open the profile menu, and click "Logout".
- **Audio**: *"Users can view past conversations in the sidebar or update their profiles at any time. Clicking 'Logout' securely invalidates the session."*
