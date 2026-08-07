# System Logic & Workflow Documentation - HealthGPT

## 1. Introduction & Objectives

HealthGPT (Zentra) provides personalized clinical guidance, risk prediction, and health monitoring. It aims to deliver accurate, citation-backed medical information and automate obesity risk predictions using a clean, modern interface.

## 2. Core Functional Logic

### 2.1 Chat Processing & RAG Pipeline

```mermaid
sequenceDiagram
    autonumber
    Client->>FastAPI: POST /chat/sessions/{id}/stream (User Message)
    FastAPI->>PostgreSQL: Fetch User Profile & Chat History
    FastAPI->>ChromaDB: Query Vector DB with User Message
    ChromaDB-->>FastAPI: Return Top-3 Context Chunks
    FastAPI->>Gemini API: Submit Prompt (System Prompt + History + Context + Query)
    Gemini API-->>FastAPI: Stream Response Chunks (SSE)
    FastAPI-->>Client: Stream Event Chunks (JSON chunks)
    Gemini API-->>FastAPI: Complete Stream
    FastAPI->>PostgreSQL: Save Completed Response
```

### 2.2 Obesity Risk Prediction Pipeline

The obesity classification pipeline uses a Random Forest model with the following features:

#### Demographics & Measurements
- `Gender` (Categorical)
- `Age` (Numerical)
- `Height` (Numerical, meters)
- `Weight` (Numerical, kg)
- `BMI` (Derived: $\text{BMI} = \frac{\text{Weight}}{\text{Height}^2}$)

#### Family History & Diet
- `family_history_with_overweight` (Binary)
- `FAVC` (Frequent consumption of high-calorie food - Binary)
- `FCVC` (Frequency of consumption of vegetables - Numerical)
- `NCP` (Number of main meals - Numerical)
- `CAEC` (Consumption of food between meals - Categorical)

#### Lifestyle & Habits
- `SMOKE` (Binary)
- `CH2O` (Daily water intake - Numerical)
- `SCC` (Calories consumption monitoring - Binary)
- `FAF` (Physical activity frequency - Numerical)
- `TUE` (Time using technology devices - Numerical)
- `CALC` (Consumption of alcohol - Categorical)
- `MTRANS` (Transportation used - Categorical)

#### Preprocessing & Inference Flow
1. **Inputs**: Extracted from `UserHealthProfile` database tables.
2. **BMI Calculation**: Computed dynamically:
   $$\text{BMI} = \frac{\text{Weight}}{\text{Height}^2}$$
3. **Encoding**: Categorical columns are converted using saved label encoders:
   ```python
   for col, encoder in label_encoders.items():
       df[col] = encoder.transform(df[col])
   ```
4. **Encoding Multi-category features**: Snacking, Alcohol, and Transport modes are expanded using dummy variables and matched to `feature_columns.pkl`.
5. **Scaling**: Numerical features are scaled via `robust_scaler.pkl`:
   $$\hat{x} = \frac{x - Q_2(x)}{Q_3(x) - Q_1(x)}$$
6. **Inference**: The processed vector is classified by the Random Forest model.
7. **Mapping Output**: The predicted index is mapped to categories:
   - `Insufficient_Weight`
   - `Normal_Weight`
   - `Overweight_Level_I`
   - `Overweight_Level_II`
   - `Obesity_Type_I`
   - `Obesity_Type_II`
   - `Obesity_Type_III`

---

## 3. Database Schema Design

```mermaid
erDiagram
    USERS ||--o| USER_PROFILES : has
    USERS ||--o| USER_HEALTH_PROFILES : contains
    USERS ||--o{ CHAT_SESSIONS : creates
    USERS ||--o{ PREDICTION_HISTORY : triggers
    CHAT_SESSIONS ||--o{ CHAT_MESSAGES : contains

    USERS {
        uuid id PK
        string email
        string hashed_password
        boolean is_verified
        datetime created_at
    }

    USER_PROFILES {
        uuid id PK
        uuid user_id FK
        float bmi
        float weight_kg
        float height_m
    }

    USER_HEALTH_PROFILES {
        uuid id PK
        uuid user_id FK
        int age
        string gender
        string family_overweight_history
        float physical_activity_hours
        float water_intake_liters
    }

    CHAT_SESSIONS {
        uuid id PK
        uuid user_id FK
        string title
        datetime created_at
    }

    CHAT_MESSAGES {
        uuid id PK
        uuid session_id FK
        string role
        string content
        string sources
        datetime created_at
    }

    PREDICTION_HISTORY {
        uuid id PK
        uuid user_id FK
        string input_data
        string prediction
        datetime created_at
    }
```
