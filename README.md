<div align="center">

<img src="assets/keeladi-banner.gif" width="100%" alt="KEELADI Smart Civic Operations Platform"/>

<br>

# 🏛️ KEELADI

### **Smart Civic Operations Platform**

**Turning civic complaints into verified action.**

<br>

<a href="#features">
<img src="https://img.shields.io/badge/AI-GEMINI-4285F4?style=for-the-badge&logo=google&logoColor=white" />
</a>
<a href="#tech-stack">
<img src="https://img.shields.io/badge/FASTAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white" />
</a>
<a href="#tech-stack">
<img src="https://img.shields.io/badge/PYTHON-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
</a>
<a href="#testing">
<img src="https://img.shields.io/badge/TESTED-PYTEST-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white" />
</a>

<br><br>

![Status](https://img.shields.io/badge/STATUS-ACTIVE-00C853?style=flat-square)
![Architecture](https://img.shields.io/badge/ARCHITECTURE-MODULAR_MONOLITH-6C5CE7?style=flat-square)
![Database](https://img.shields.io/badge/DATABASE-SQLITE-003B57?style=flat-square\&logo=sqlite\&logoColor=white)
![License](https://img.shields.io/badge/LICENSE-OPEN_SOURCE-lightgrey?style=flat-square)

<br>

**Report → Understand → Assign → Verify → Analyze → Improve**

</div>

---

# 🌐 What is KEELADI?

> **KEELADI is not just a complaint management system.
> It is an operational intelligence layer for civic infrastructure.**

KEELADI is an AI-powered **Smart Civic Operations Platform** designed to modernize municipal waste management and field operations.

It connects:

```text
Citizen
   │
   ▼
Complaint
   │
   ▼
AI Intelligence
   │
   ▼
Task Assignment
   │
   ▼
Field Operations
   │
   ▼
GPS Verification
   │
   ▼
Evidence
   │
   ▼
Resolution
   │
   ▼
Analytics
   │
   ▼
Prediction
```

The platform brings together **citizen complaints, AI classification, field workers, supervisors, fleet management, geospatial verification, and predictive analytics** into one operational workflow.

---

# ⚡ The Problem

Traditional civic complaint systems often follow this model:

```text
Complaint
   ↓
Database
   ↓
"Resolved"
```

The problem?

There is often little operational intelligence between those steps.

KEELADI introduces a complete feedback loop:

```text
┌───────────────┐
│    REPORT     │
└───────┬───────┘
        ↓
┌───────────────┐
│   UNDERSTAND  │
│    Gemini AI  │
└───────┬───────┘
        ↓
┌───────────────┐
│   PRIORITIZE  │
└───────┬───────┘
        ↓
┌───────────────┐
│     ASSIGN    │
└───────┬───────┘
        ↓
┌───────────────┐
│    EXECUTE    │
└───────┬───────┘
        ↓
┌───────────────┐
│     VERIFY    │
│ GPS + Evidence│
└───────┬───────┘
        ↓
┌───────────────┐
│    ANALYZE    │
└───────┬───────┘
        ↓
┌───────────────┐
│    PREDICT    │
└───────┬───────┘
        │
        └───────────────↺
```

---

# 🚀 Features

## 🤖 AI Complaint Intelligence

KEELADI uses **Google Gemini** to automatically process incoming civic complaints.

The AI layer can identify:

* Complaint category
* Severity
* Priority
* Operational context
* Recommended action

### Example

```text
Citizen:

"There has been garbage piling up near the
school entrance for the last three days."

                 ↓

              GEMINI AI

                 ↓

Category:       Waste Accumulation
Severity:       HIGH
Priority:       URGENT
Department:     Sanitation
Action:         Immediate Collection
```

---

# 📍 Geo-Verified Field Operations

KEELADI introduces geographic verification into the task lifecycle.

A worker cannot simply mark a task as completed from anywhere.

The system verifies:

```text
Worker GPS
     +
Issue Coordinates
     ↓
Haversine Distance
     ↓
Within Allowed Radius?
     ↓
      YES
       │
       ▼
Before Image
       ↓
Work Execution
       ↓
After Image
       ↓
Task Completion
```

The workflow uses a configurable geographic radius, with the MVP enforcing approximately **100 meters** around the reported issue.

---

# 📸 Evidence-Based Completion

Instead of trusting:

```text
status = "completed"
```

KEELADI works toward:

```text
status = "completed"

        +

GPS verified

        +

Before image

        +

After image
```

This creates a stronger operational audit trail.

---

# 🚛 Fleet Management

Municipal waste collection vehicles can be managed through the platform.

### Fleet capabilities

* Vehicle registration
* Vehicle identification
* Operational status
* Availability tracking
* Ward-level allocation
* Collection planning

Example:

```text
┌──────────────────────────────────────┐
│           FLEET STATUS               │
├──────────────────────────────────────┤
│                                      │
│  🚛 KL-01-AB-1234     AVAILABLE      │
│  🚛 KL-01-AB-1235     ON ROUTE       │
│  🚛 KL-01-AB-1236     MAINTENANCE    │
│  🚛 KL-01-AB-1237     AVAILABLE      │
│                                      │
└──────────────────────────────────────┘
```

---

# 📊 Predictive Waste Analytics

KEELADI uses AI-assisted forecasting to support future operational decisions.

Instead of asking:

> "How much waste did Ward 12 generate?"

the system can move toward:

> "How much waste should Ward 12 generate next week?"

This can support:

* Weekly waste forecasting
* Ward-level planning
* Truck allocation
* Resource planning
* Operational trend analysis

---

# 🔐 Role-Based Access Control

KEELADI is designed around multiple municipal roles.

| Role                 | Responsibility                   |
| -------------------- | -------------------------------- |
| 👤 Citizen           | Submit and track complaints      |
| 🧹 Sanitation Worker | Execute field tasks              |
| 👨‍💼 Supervisor     | Assign and monitor tasks         |
| 🏗️ Engineer         | Handle infrastructure operations |
| 🏛️ Administrator    | Manage civic operations          |
| 🚛 Fleet Operator    | Manage vehicle operations        |

Authentication is secured through **JWT-based authentication and role-based authorization**.

---

# 🧠 System Architecture

KEELADI follows a **Modular Monolith architecture**.

Rather than immediately splitting the platform into multiple microservices, the system maintains clearly separated domain modules within a single application.

```text
                         ┌───────────────────┐
                         │     CITIZENS      │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │     FASTAPI       │
                         │    API LAYER      │
                         └─────────┬─────────┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          │                        │                        │
          ▼                        ▼                        ▼
 ┌────────────────┐      ┌────────────────┐      ┌────────────────┐
 │   COMPLAINTS   │      │ TASK MANAGEMENT│      │ FLEET MANAGER  │
 └───────┬────────┘      └───────┬────────┘      └───────┬────────┘
         │                        │                        │
         ▼                        ▼                        ▼
 ┌────────────────┐      ┌────────────────┐      ┌────────────────┐
 │   GEMINI AI    │      │ GEO VERIFIER   │      │  ANALYTICS     │
 └────────────────┘      └────────────────┘      └────────────────┘
         │                        │                        │
         └────────────────────────┼────────────────────────┘
                                  │
                                  ▼
                        ┌────────────────────┐
                        │     SQLALCHEMY     │
                        └─────────┬──────────┘
                                  │
                                  ▼
                        ┌────────────────────┐
                        │       SQLITE       │
                        └────────────────────┘
```

---

# 🏗️ Architecture Philosophy

KEELADI follows four core engineering principles.

### 01 — Modular

Each domain is isolated into a dedicated module.

### 02 — Verifiable

Important field operations should have measurable evidence.

### 03 — Intelligent

AI handles classification and forecasting workloads.

### 04 — Extensible

The MVP architecture is designed so individual modules can later evolve independently.

---

# 🛠️ Tech Stack

<div align="center">

| Layer                 | Technology        |
| --------------------- | ----------------- |
| **Language**          | Python 3.10+      |
| **API Framework**     | FastAPI           |
| **Validation**        | Pydantic          |
| **Server**            | Uvicorn           |
| **ORM**               | SQLAlchemy        |
| **Database**          | SQLite            |
| **AI**                | Google Gemini     |
| **Authentication**    | JWT               |
| **Password Security** | Passlib + Bcrypt  |
| **Testing**           | Pytest + HTTPX    |
| **Geospatial Logic**  | Haversine Formula |

</div>

---

# 📂 Project Structure

```text
KEELADI/
│
├── backend/
│   │
│   ├── app/
│   │   ├── main.py
│   │   │
│   │   ├── models/
│   │   │
│   │   ├── schemas/
│   │   │
│   │   ├── routers/
│   │   │
│   │   ├── services/
│   │   │
│   │   ├── ai/
│   │   │
│   │   └── utils/
│   │
│   ├── tests/
│   │
│   ├── requirements.txt
│   │
│   ├── .env.example
│   │
│   └── ...
│
├── assets/
│   ├── keeladi-banner.gif
│   ├── workflow.gif
│   ├── architecture.png
│   └── dashboard.gif
│
├── README.md
│
└── LICENSE
```

---

# ⚡ Getting Started

## 1. Clone

```bash
git clone <your-repository-url>
cd KEELADI
```

Navigate into the backend:

```bash
cd backend
```

---

## 2. Create Virtual Environment

### Windows

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment

Create your environment file.

### Linux / macOS

```bash
cp .env.example .env
```

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

Add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

> Never commit `.env` or API credentials to GitHub.

---

# ▶️ Run KEELADI

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

The API will start at:

```text
http://127.0.0.1:8000
```

---

# 📚 API Documentation

Once the server is running:

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

---

# 🧪 Testing

Run the complete test suite:

```bash
pytest
```

Verbose mode:

```bash
pytest -v
```

---

# 🔄 Complete Operational Flow

```text
                 ┌──────────────────┐
                 │     CITIZEN      │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │     COMPLAINT    │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │    GEMINI AI     │
                 │   CLASSIFICATION  │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ SEVERITY +       │
                 │ PRIORITY ENGINE  │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ TASK ASSIGNMENT  │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │  FIELD WORKER    │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │  GPS VALIDATION  │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ BEFORE / AFTER   │
                 │    EVIDENCE      │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ VERIFIED TASK    │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │    ANALYTICS     │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │   FORECASTING    │
                 └────────┬─────────┘
                          │
                          └───────────────↺
```

---

# 🎬 Product Demonstration

<div align="center">

### Citizen → AI → Worker → Verification

<img src="assets/workflow.gif" width="90%" alt="KEELADI Workflow"/>

</div>

---

# 🖥️ Command Center

<div align="center">

<img src="assets/dashboard.gif" width="90%" alt="KEELADI Command Center"/>

</div>

Example operational dashboard:

```text
╔════════════════════════════════════════════════════╗
║                  KEELADI COMMAND                   ║
╠════════════════════════════════════════════════════╣
║                                                    ║
║   COMPLAINTS          ACTIVE TASKS       VEHICLES  ║
║      1,284                87                42     ║
║                                                    ║
║   ──────────────────────────────────────────────   ║
║                                                    ║
║   VERIFIED TASKS                    96.8%           ║
║                                                    ║
║   HIGH PRIORITY                     24              ║
║                                                    ║
║   VEHICLES ACTIVE                   31              ║
║                                                    ║
╚════════════════════════════════════════════════════╝
```

> Dashboard numbers above are illustrative UI examples, not live system metrics.

---

# 🧭 Geo Verification

KEELADI uses the **Haversine formula** to calculate the distance between the reported issue and the worker's current GPS coordinates.

Conceptually:

```text
             ISSUE
              📍
             / \
            /   \
           /     \
          /       \
         /         \
        /           \
       📱            

     WORKER GPS

        ↓

Haversine Distance

        ↓

┌──────────────────────┐
│ Within allowed range?│
└──────────┬───────────┘
           │
       ┌───┴───┐
      YES      NO
       │        │
       ▼        ▼
    Continue   Reject
```

This prevents location-sensitive tasks from being completed from an unrelated location.

---

# 🧠 AI Pipeline

```text
               USER COMPLAINT
                      │
                      ▼
              ┌───────────────┐
              │ Text Cleaning │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ Gemini Flash  │
              └───────┬───────┘
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
      Category     Severity     Priority
          │           │           │
          └───────────┼───────────┘
                      ▼
              ┌───────────────┐
              │ Task Creation │
              └───────────────┘
```

---

# 📈 Predictive Intelligence

The analytics layer is designed to evolve from descriptive analytics toward predictive operations.

```text
Historical Data
      │
      ├── Complaints
      ├── Waste Volume
      ├── Ward Activity
      ├── Vehicle Usage
      └── Resolution Times
              │
              ▼
        ┌─────────────┐
        │ AI ANALYSIS │
        └──────┬──────┘
               │
               ▼
       ┌───────────────┐
       │ FORECASTING   │
       └───────┬───────┘
               │
       ┌───────┼────────┐
       ▼       ▼        ▼
     Waste    Fleet    Ward
   Forecast  Planning  Trends
```

---

# 🔐 Security

KEELADI implements:

* JWT authentication
* Password hashing
* Bcrypt
* Role-based authorization
* Protected API endpoints
* Pydantic validation
* Environment-based secret management

### Security Rule

```text
.env
  │
  ├── API Keys
  ├── Secrets
  └── Credentials

        ↓

NEVER COMMIT TO GIT
```

---

# 🧩 Engineering Principles

### `01` — Evidence over assumptions

A completed field task should have measurable evidence wherever the workflow requires it.

### `02` — Automation over repetitive work

AI handles repetitive classification and analytical workloads.

### `03` — Modular by design

Business domains remain separated even inside the monolith.

### `04` — Data-driven operations

Operational data should become useful information.

### `05` — Build for evolution

The MVP architecture leaves room for PostgreSQL, Redis, object storage, background processing, and independent service extraction later.

---

# 🗺️ Roadmap

## Phase 01 — Foundation

* [x] FastAPI backend
* [x] Database models
* [x] JWT authentication
* [x] RBAC
* [x] Complaint management
* [x] Task management

## Phase 02 — Smart Operations

* [x] Gemini integration
* [x] Complaint classification
* [x] Severity scoring
* [x] GPS verification
* [x] Before/After evidence
* [x] Fleet management

## Phase 03 — Intelligence

* [x] Waste forecasting
* [x] Ward analytics
* [ ] Advanced fleet optimization
* [ ] Historical trend engine
* [ ] Operational dashboards

## Phase 04 — Production

* [ ] PostgreSQL
* [ ] Redis
* [ ] Background workers
* [ ] Object storage
* [ ] Containerized deployment
* [ ] Observability
* [ ] Production monitoring

---

# 🔮 Future Vision

KEELADI can evolve beyond waste management into a broader civic operations platform.

```text
                    KEELADI
                       │
       ┌───────────────┼────────────────┐
       │               │                │
       ▼               ▼                ▼
    SANITATION     INFRASTRUCTURE    PUBLIC SERVICES
       │               │                │
       ▼               ▼                ▼
    WASTE           ROADS             LIGHTING
    FLEET           DRAINAGE          WATER
    CLEANING        MAINTENANCE       COMPLAINTS
```

The long-term vision is a platform where municipal operations become:

**Observable → Verifiable → Intelligent → Predictive**

---

# 🤝 Contributing

Contributions and improvements are welcome.

### 1. Fork the repository

```bash
git fork
```

### 2. Create a branch

```bash
git checkout -b feature/your-feature
```

### 3. Make your changes

```bash
git add .
git commit -m "feat: add your feature"
```

### 4. Push

```bash
git push origin feature/your-feature
```

### 5. Open a Pull Request

---

# 📜 License

This project is currently under development.

Add the appropriate license before distributing KEELADI publicly.

---

<div align="center">

<br>

<img src="assets/keeladi-logo.png" width="120" alt="KEELADI Logo"/>

# **KEELADI**

### Civic Intelligence. Verified Action. Better Operations.

<br>

```text
REPORT  →  UNDERSTAND  →  ASSIGN  →  VERIFY  →  ANALYZE
```

<br>

**Built with Python · FastAPI · Gemini AI**

<br>

---

### 🏛️ Building smarter civic infrastructure.

</div>
