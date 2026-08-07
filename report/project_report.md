# HealthGPT (Zentra) Project Report

---
**Course:** Final Year Software Engineering & AI Capstone  
**Project Title:** HealthGPT: Intelligent RAG Healthcare Assistant & Wellness Dashboard  
**Academic Year:** 2026  
**Candidate Name:** Himanshu Kumar  
**Supervisor:** Department of Computer Science & Engineering  
---

## Certificate of Authenticity
This is to certify that the project work entitled **"HealthGPT: Intelligent RAG Healthcare Assistant & Wellness Dashboard"** is a record of work carried out by **Himanshu Kumar** under the supervision of the Department of Computer Science & Engineering. This work is authentic and has not been submitted elsewhere for any other degree or diploma.

---

## Acknowledgement
I express my gratitude to my academic advisor and the department faculty for their guidance throughout this project. I also thank my peers for their support, and the open-source community for providing the tools and frameworks that made this work possible.

---

## Abstract
Modern healthcare systems face challenges with information accessibility and early risk detection. **HealthGPT** addresses these challenges by combining **Retrieval-Augmented Generation (RAG)** and **machine learning risk prediction**. The platform provides an empathetic health assistant backed by World Health Organization (WHO) guidelines, alongside a wellness dashboard featuring an obesity classification model. Built with a React frontend and a FastAPI backend, the system implements secure JWT authentication and local vector search to deliver a fast, reliable, and user-friendly experience.

---

## Table of Contents
1. **Introduction & Objectives**
2. **Problem Statement & Scope**
3. **Literature Review & Existing Systems**
4. **Proposed System & Architecture**
5. **Database Design & Schema**
6. **Authentication & Security**
7. **Machine Learning Pipeline**
8. **Retrieval-Augmented Generation (RAG)**
9. **Prompt Engineering & Safety**
10. **System Testing & Validation**
11. **Deployment Strategy**
12. **Results & System Analysis**
13. **Challenges & Limitations**
14. **Future Scope & Conclusion**
15. **References**

---

## 1. Introduction & Objectives
The goal of HealthGPT is to make evidence-based health information more accessible to users. The project objectives are:
- Develop a secure wellness portal for logging lifestyle metrics.
- Implement an automated machine learning classifier to assess obesity risk.
- Integrate a RAG-based assistant to provide health information backed by official guidelines.
- Build a responsive dashboard using a decoupled API architecture.

---

## 2. Problem Statement & Scope
Accessing reliable medical information online can be challenging due to the risk of misinformation and generic advice. HealthGPT addresses this by indexing trusted medical documents, such as WHO guidelines, to provide accurate, context-aware information, while using an ML model to offer personalized lifestyle risk assessments.

---

## 3. Literature Review & Existing Systems
Existing health portals often rely on simple keyword searches or generic chatbot responses that lack clinical backing or user context. HealthGPT improves on these methods by using semantic vector searches to retrieve relevant document passages and combining them with the user's health profile for more personalized responses.

---

## 4. Proposed System & Architecture
HealthGPT uses a decoupled architecture to separate the user interface from data processing and model inference:
- **Frontend SPA**: React, Vite, and Tailwind CSS for a fast, responsive interface.
- **Backend API**: FastAPI serving endpoints for user profiles, predictions, and chat.
- **Vector DB**: ChromaDB storing embedded WHO manuals.
- **Relational Storage**: PostgreSQL managing user data, profiles, and chat sessions.

---

## 5. Database Design & Schema
The relational database (PostgreSQL) is structured around five core tables to manage user data:
- `users`: Stores credentials, verification status, and timestamps.
- `user_profiles`: Stores basic metrics (height, weight, BMI).
- `user_health_profiles`: Stores detailed lifestyle inputs for the ML model.
- `chat_sessions` & `chat_messages`: Manage conversational history.
- `prediction_history`: Logs ML model inference inputs and results.

---

## 6. Authentication & Security
The system uses OAuth2 with JWT for stateless session authentication. Passwords are encrypted using `bcrypt`, and user endpoints are protected by token validation middleware.

---

## 7. Machine Learning Pipeline
Obesity risk is assessed using a Random Forest Classifier trained on 16 lifestyle parameters. Numerical features are normalized using a Robust Scaler, and categorical features are mapped via custom label encoders before running inference to classify the user into one of seven risk levels.

---

## 8. Retrieval-Augmented Generation (RAG)
The RAG pipeline extracts text from WHO manuals, splits them into manageable chunks, and indexes them in ChromaDB using Google's embedding model. When a user asks a question, the retriever fetches the most relevant chunks to build the prompt context.

---

## 9. Prompt Engineering & Safety
To ensure safety, system prompts include strict guidelines:
- Injected contexts include document source metadata for transparency.
- The assistant is instructed to provide wellness information rather than diagnoses.
- A mandatory medical disclaimer is appended to every response.

---

## 10. System Testing & Validation
Testing includes API validation (FastAPI endpoints), ML inference checks, authentication security tests, and edge-case evaluations (such as handling empty profiles or invalid inputs).

---

## 11. Deployment Strategy
The platform is designed for cloud deployment:
- The React frontend is configured for Vercel.
- The FastAPI backend is set up for Render using Docker containers.
- Persistent storage is managed via Render's managed PostgreSQL and Redis services.

---

## 12. Results & System Analysis
The system successfully delivers real-time response streaming with low latency, accurate risk classification, and clear source citations.

---

## 13. Challenges & Limitations
Challenges included matching varied medical terminology in searches and handling sparse health profiles. The model is also limited to lifestyle-based obesity classification and does not replace professional clinical diagnosis.

---

## 14. Future Scope & Conclusion
Future updates will focus on supporting multimodal inputs, such as image-based food logging, and integrating with external healthcare APIs. In conclusion, HealthGPT demonstrates how combining machine learning and RAG can make reliable health information more accessible.

---

## 15. References
1. World Health Organization. (2020). *Guidelines on Physical Activity and Sedentary Behaviour*.
2. Blei, D. M., Ng, A. Y., & Jordan, M. I. (2003). Latent Dirichlet Allocation. *Journal of Machine Learning Research*.
3. Vaswani, A., et al. (2017). Attention Is All You Need. *Advances in Neural Information Processing Systems*.
