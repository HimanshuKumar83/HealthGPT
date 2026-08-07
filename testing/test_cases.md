# QA Test Suites - HealthGPT

This document details the test suites used to validate the API, UI, RAG prompt engine, authentication, security, and edge-case behaviors of the HealthGPT platform.

## 1. Authentication & Security Test Cases

### TC-AUTH-01: Secure Password Hashing
- **Objective**: Verify that user passwords are encrypted before storage.
- **Method**: Register a test account and inspect the `hashed_password` column in the database.
- **Expected Result**: Passwords must be saved as secure bcrypt hashes. Plaintext passwords must not be logged or stored.

### TC-AUTH-02: JWT Expiration and Middleware Protection
- **Objective**: Validate that endpoints reject expired tokens or requests without authorization headers.
- **Method**: Send a request to `/profile` with no token, and another request using a token expired for over 600 minutes.
- **Expected Result**: Both requests must return a `401 Unauthorized` status.

---

## 2. API & Endpoint Test Cases

### TC-API-01: Health Profile Creation & Update
- **Objective**: Verify that user health profile updates are processed and stored correctly.
- **Method**: Send a `PUT /profile` request with updated weight, height, and activity metrics.
- **Expected Result**: Returns a `200 OK` status and updates the corresponding record in PostgreSQL.

### TC-API-02: Streamed RAG Chat Endpoint
- **Objective**: Validate Server-Sent Event (SSE) streaming for real-time chat.
- **Method**: Send a `POST /chat/sessions/{id}/stream` request containing a test query.
- **Expected Result**: The server must return a `text/event-stream` response and stream data chunks, ending with a `[DONE]` signal.

---

## 3. RAG Prompt Engineering & Safety Test Cases

### TC-RAG-01: Dynamic Disclaimer Injection
- **Objective**: Confirm that all chat responses include the required medical disclaimer.
- **Method**: Ask the chatbot: "Explain the symptoms of malaria."
- **Expected Result**: The generated response must contain the warning: *"This is for informational purposes only. Please consult a doctor for clinical diagnosis."*

### TC-RAG-02: Retrieval Context Fallback
- **Objective**: Verify how the chatbot handles queries that fall outside the indexed WHO manuals.
- **Method**: Ask the assistant a query not covered in the local vector database, such as "How do I fix a broken car engine?"
- **Expected Result**: The chatbot must handle the query gracefully, advising that it is designed to assist with health and wellness queries.

---

## 4. Machine Learning & Edge Case Test Cases

### TC-ML-01: Missing Health Profile Exception
- **Objective**: Verify prediction behavior when a user health profile is missing.
- **Method**: Register a new user, skip onboarding, and send a request to `/predict`.
- **Expected Result**: The server must return a `400 Bad Request` status with the message: *"Health profile not found. Please create your profile first."*

### TC-ML-02: Scaler Handling of Outlier Inputs
- **Objective**: Verify that the Robust Scaler handles extreme profile inputs (e.g. extremely high weight values) without crashing.
- **Method**: Set the health profile weight to `300 kg` and trigger `/predict`.
- **Expected Result**: The model must scale the input metrics and return an classification (such as `Obesity_Type_III`) without throwing a value error.
