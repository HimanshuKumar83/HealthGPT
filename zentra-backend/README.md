# HealthGPT AI Platform

A full-stack AI health assistant built with a FastAPI backend and a React + TypeScript frontend. The platform supports authentication, user profile management, health prediction, and AI chat with RAG-powered responses.

Contact: himanshukumarsingh454@gmail.com

---

## Overview

HealthGPT combines:
- a secure backend for authentication, profile handling, and prediction APIs
- a modern web frontend for onboarding, dashboards, results, and account management
- AI-powered chat and retrieval-based health knowledge support

This project is designed to provide a smooth experience for users who want health insights, wellness tracking, and AI-guided support in one place.

---

## Features

### Backend
- JWT-based authentication and authorization
- User profile creation and updates
- ML-based health prediction workflow
- Chat and RAG-based AI assistant support
- PostgreSQL database integration
- Redis support for caching and session-related needs
- Alembic migrations for database management

### Frontend
- React + TypeScript single-page application
- Vite-based fast development and build workflow
- Tailwind CSS-based modern UI
- Authentication pages and protected routes
- Onboarding, dashboard, results, account, and profile screens
- Responsive layout for desktop and mobile screens

---

## Tech Stack

### Backend
- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- PostgreSQL
- Alembic
- Redis
- Pydantic
- scikit-learn
- pandas / numpy
- Chroma / LangChain / Gemini / OpenAI integrations

### Frontend
- React
- TypeScript
- Vite
- Tailwind CSS
- React Router
- Zustand
- Axios
- Framer Motion
- Lucide Icons

---

## Project Structure

```bash
HealthGPT2/
├── zentra-backend/           # FastAPI backend
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── ml/
│   │   ├── rag/
│   │   └── services/
│   ├── migrations/
│   ├── requirements.txt
│   └── render.yaml
│
└── zentra-ui/               # React frontend
    ├── src/
    ├── public/
    ├── package.json
    └── vite.config.ts
```

---

## Backend Setup

### Prerequisites
- Python 3.10+
- PostgreSQL
- Redis (optional but recommended)

### Install dependencies
```bash
cd zentra-backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Environment variables
Create a `.env` file in the backend folder with values such as:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/your_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
GEMINI_API_KEY=your-gemini-key
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
```

### Run backend
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

---

## Frontend Setup

### Prerequisites
- Node.js 18+
- npm

### Install dependencies
```bash
cd zentra-ui
npm install
```

### Run frontend
```bash
npm run dev
```

### Frontend environment variable
Create a `.env.local` file inside the frontend folder:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

---

## Deployment

### Backend
- Recommended: Render
- Use the backend folder as the deployment root
- Set the runtime environment to Python
- Provide the required environment variables for database, secret key, and API keys

### Frontend
- Recommended: Vercel
- Build command: `npm run build`
- Output directory: `dist`
- Set `VITE_API_BASE_URL` to your deployed backend URL

---

## Contact

For questions, collaboration, or deployment support:
- Email: himanshukumarsingh454@gmail.com

**7. Access API Documentation**
- **Scalar Docs**: http://127.0.0.1:8000/scalar
- **OpenAPI Schema**: http://127.0.0.1:8000/openapi.json

---

## 🔌 API Endpoints

### 🔐 Authentication Routes (`/auth`)

| Method | Endpoint | Description | Auth | Body |
|--------|----------|-------------|------|------|
| POST | `/auth/signup` | Register new user | No | `{ email, password }` |
| POST | `/auth/login` | Get JWT token | No | `{ email, password }` |
| POST | `/auth/request-password-reset` | Request reset token | No | `{ email }` |
| POST | `/auth/reset-password` | Reset password | No | `{ token, new_password }` |
| GET | `/auth/me` | Get current user | Yes | - |

### 👤 User Profile Routes (`/profile`)

| Method | Endpoint | Description | Auth | Body |
|--------|----------|-------------|------|------|
| POST | `/profile/create` | Create user profile | Yes | Full profile data |
| PUT | `/profile/update` | Update profile | Yes | Partial profile data |
| GET | `/profile/me` | Get user profile | Yes | - |

**Profile Fields**: `gender`, `age`, `height_m`, `weight_kg`, `family_overweight_history`, `high_calorie_food`, `vegetable_intake_freq`, `main_meals_per_day`, `snack_frequency`, `smokes`, `water_intake_liters`, `calorie_tracking`, `physical_activity_hours`, `screentime_hours`, `alcohol_consumption`, `travel_mode`

### 🤖 Prediction Routes (`/predict`)

| Method | Endpoint | Description | Auth | Body |
|--------|----------|-------------|------|------|
| POST | `/predict/` | Get ML prediction | Yes | Same as profile fields |

**Response Format**:
```json
{
  "prediction": "Category_Name",
  "confidence": 0.87,
  "bmi": 27.55,
  "saved_to_history": true
}
```

### 📚 Documentation Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/scalar` | Interactive API docs |
| GET | `/openapi.json` | OpenAPI schema |

---

## 🤖 ML Pipeline Architecture

### Inference Flow

```
Input Data (15 features)
    ↓
Label Encoding (categorical variables)
    ↓
Robust Scaling (numerical features)
    ↓
Random Forest Classifier (100 estimators)
    ↓
Prediction Output (7 categories)
```

### Model Specifications

- **Algorithm**: Random Forest Classifier
- **Estimators**: 100 trees
- **Accuracy**: 95%+ on test set
- **Training Data**: 2000+ samples
- **Features**: 15 input variables
- **Output Classes**: 7 categories

### Serialized Artifacts

| File | Size | Purpose |
|------|------|---------|
| `random_forest_model.pkl` | 7.9 MB | Trained classifier |
| `label_encoders.pkl` | 1.4 KB | Categorical encoders |
| `robust_scaler.pkl` | 1.0 KB | Feature scaler |
| `target_label_encoder.pkl` | 608 B | Target encoder |
| `feature_columns.pkl` | 517 B | Feature names |

---

## 🗄️ Database Schema

```
┌─────────────────┐
│      User       │
├─────────────────┤
│ id (PK)         │
│ email (UNIQUE)  │
│ hashed_password │
└────────┬────────┘
         │
         ├──────────────────────────────────┐
         │                                  │
         ▼                                  ▼
┌──────────────────────┐      ┌──────────────────────────┐
│ UserHealthProfile    │      │   PredictionHistory      │
├──────────────────────┤      ├──────────────────────────┤
│ id (PK)              │      │ id (PK)                  │
│ user_id (FK, UNIQUE) │      │ user_id (FK)             │
│ gender               │      │ input_data (JSON)        │
│ age                  │      │ prediction               │
│ height_m             │      │ created_at               │
│ weight_kg            │      └──────────────────────────┘
│ bmi (computed)       │
│ [15+ health fields]  │
│ updated_at           │
└──────────────────────┘
```

---

## 📖 Usage Examples

### 1. User Registration & Authentication

```bash
# Register
curl -X POST "http://127.0.0.1:8000/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "SecurePass123!"}'

# Login
curl -X POST "http://127.0.0.1:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "SecurePass123!"}'
```

### 2. Profile Management

```bash
# Create Profile
curl -X POST "http://127.0.0.1:8000/profile/create" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "gender": "Male",
    "age": 28,
    "height_m": 1.75,
    "weight_kg": 82,
    "family_overweight_history": "yes",
    "high_calorie_food": "yes",
    "vegetable_intake_freq": 2,
    "main_meals_per_day": 3,
    "snack_frequency": "Sometimes",
    "smokes": "no",
    "water_intake_liters": 2.5,
    "calorie_tracking": "no",
    "physical_activity_hours": 1.5,
    "screentime_hours": 6,
    "alcohol_consumption": "Sometimes",
    "travel_mode": "Car"
  }'

# Update Profile
curl -X PUT "http://127.0.0.1:8000/profile/update" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"weight_kg": 78, "physical_activity_hours": 3}'
```

### ML Prediction

```bash
curl -X POST "http://127.0.0.1:8000/predict/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "gender": "Female",
    "age": 32,
    "height_m": 1.62,
    "weight_kg": 68,
    "family_overweight_history": "no",
    "high_calorie_food": "no",
    "vegetable_intake_freq": 3,
    "main_meals_per_day": 3,
    "snack_frequency": "no",
    "smokes": "no",
    "water_intake_liters": 2,
    "calorie_tracking": "yes",
    "physical_activity_hours": 2,
    "screentime_hours": 3,
    "alcohol_consumption": "no",
    "travel_mode": "Walking"
  }'
```

---

## 🔮 Roadmap

### Planned Features

**AI & Chat Capabilities**
- [ ] LLM Integration (GPT-4, Claude, Gemini)
- [ ] Conversational AI Assistant
- [ ] Context-aware chat responses
- [ ] Multi-turn conversation handling
- [ ] Chat history persistence

**Analytics & Insights**
- [ ] Prediction history retrieval API
- [ ] Analytics dashboard backend
- [ ] Data visualization endpoints
- [ ] Trend analysis algorithms
- [ ] Personalized recommendations engine

**Infrastructure**
- [ ] Redis caching layer
- [ ] Rate limiting middleware
- [ ] WebSocket support for real-time chat
- [ ] Batch prediction endpoints
- [ ] Export functionality (CSV/PDF)

**Integrations**
- [ ] Third-party API connectors
- [ ] Webhook support
- [ ] OAuth2 providers (Google, GitHub)
- [ ] Mobile app backend support

**DevOps**
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Prometheus monitoring
- [ ] Grafana dashboards
- [ ] Automated testing suite

---

## 🧪 Development

### Testing

```bash
pip install pytest pytest-asyncio httpx
pytest
pytest --cov=app --cov-report=html
```

### Database Migrations

```bash
alembic revision --autogenerate -m "Description"
alembic upgrade head
alembic downgrade -1
```

### Code Quality

```bash
black app/
flake8 app/
mypy app/
```

---

## 📄 License

© 2024 Fahad Khan. All rights reserved.

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/name`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/name`)
5. Open Pull Request

**Code Standards**: PEP 8, type hints, docstrings, tests required

---

## 📞 Contact

- **Email**: himanshukumarsingh454@gmail.com
- **GitHub Issues**: [Create an issue](https://github.com/yourusername/zentra/issues)
- **Documentation**: http://127.0.0.1:8000/scalar

---

<div align="center">

**Built with FastAPI, PostgreSQL, and Machine Learning**

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat-square&logo=postgresql&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)

</div>

