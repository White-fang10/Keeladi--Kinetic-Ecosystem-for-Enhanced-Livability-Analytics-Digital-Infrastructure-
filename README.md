# KEELADI - Smart Civic Operations Platform

KEELADI is a modern Smart Civic Operations Platform designed to digitize and optimize municipal waste management, task assignments, and fleet tracking. It utilizes a Modular Monolith architecture powered by FastAPI and integrates Google Gemini AI for predictive analytics and automated complaint triaging.

## 🚀 Features

- **Role-Based Access Control (RBAC)**: Secure JWT authentication with 8 distinct operational roles (Citizen, Sanitation Worker, Supervisor, Engineers, etc.).
- **Smart Complaint Triaging**: AI-driven (Gemini 1.5 Flash) categorization and severity scoring for citizen issues.
- **Geo-Verified Workflows**: GPS-backed task verification enforcing workers to upload Before/After images within a strict ~100m radius of the issue using the Haversine formula.
- **Fleet Management**: Real-time vehicle registration and operational status updates for waste collection trucks.
- **Predictive Analytics**: Gemini-powered forecasting to estimate weekly waste generation and optimize truck allocation per ward.

## 🛠 Tech Stack

- **Backend Framework**: Python 3.10+, FastAPI, Pydantic
- **ORM & Database**: SQLAlchemy, SQLite (MVP Setup)
- **AI Integration**: Google Generative AI (`gemini-1.5-flash`)
- **Testing**: Pytest, HTTPX
- **Security**: Passlib (Bcrypt), python-jose (JWT)

## 💻 Local Development Setup

### 1. Environment Setup

Clone the repository and navigate to the backend folder:

```bash
cd backend
python -m venv venv
```

Activate the virtual environment:
- **Windows**: `.\venv\Scripts\activate`
- **Unix/macOS**: `source venv/bin/activate`

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configuration

Copy the example environment file and insert your active API keys:

```bash
cp .env.example .env
```
Ensure your `.env` has a valid `GEMINI_API_KEY` for the AI features to function.

### 4. Running the Server

Start the Uvicorn development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.
You can view the interactive Swagger documentation at `http://127.0.0.1:8000/docs`.

### 5. Running Tests

Execute the full isolated test suite using Pytest:

```bash
pytest
```
