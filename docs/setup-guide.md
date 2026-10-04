# THREAD — Clinical Continuity Engine

## Setup Guide

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm

---

### 1. Clone the repository

```bash
git clone https://github.com/[your-repo].git
cd [your-repo]
```

---

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and set your watsonx.ai credentials (optional — app runs in demo mode without them):

```
WATSONX_API_KEY=your_api_key
WATSONX_PROJECT_ID=your_project_id
```

Start the backend:

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`.
Interactive docs: `http://localhost:8000/docs`

---

### 3. Frontend Setup

```bash
cd frontend
npm install
```

Create environment file:

```bash
# Create frontend/.env (copy from .env.local.example)
# Content: VITE_API_URL=http://localhost:8000
```

Start the frontend:

```bash
npm run dev
```

The UI will be available at `http://localhost:5173`.

---

### 4. Load Demo Patient

Once both services are running:

1. Open `http://localhost:5173`
2. Click **"Load Demo Patient"** on the dashboard
3. The synthetic demo dataset will be seeded automatically

Or via API:

```bash
curl -X POST http://localhost:8000/demo/seed
```

---

### 5. Quick Start (Both Services)

From the project root:

```bash
python start.py
```

---

### Environment Variables

| Variable | Description | Default |
|---|---|---|
| `WATSONX_API_KEY` | IBM watsonx.ai API key | None (demo mode) |
| `WATSONX_PROJECT_ID` | IBM watsonx.ai project ID | None |
| `WATSONX_URL` | watsonx.ai endpoint URL | `https://us-south.ml.cloud.ibm.com` |
| `WATSONX_MODEL_ID` | Model ID | `ibm/granite-13b-instruct-v2` |
| `DATABASE_URL` | SQLAlchemy DB URL | `sqlite:///./thread.db` |
| `DEMO_MODE` | Use demo responses (no LLM) | `true` |

---

### Demo Mode

When `DEMO_MODE=true` (default) or when no watsonx.ai credentials are provided, the application:

- Uses pre-written realistic clinical outputs for all generated documents
- Fully loads and displays the synthetic patient dataset
- Demonstrates all P0 features end-to-end without LLM calls

To enable real watsonx.ai generation, set `DEMO_MODE=false` and provide valid credentials.

---

### Project Structure

```
thread/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py            # Settings
│   │   ├── database.py          # SQLAlchemy engine
│   │   ├── models/              # ORM models
│   │   ├── routers/             # API routes
│   │   ├── services/
│   │   │   ├── llm/             # LLM abstraction (watsonx.ai)
│   │   │   ├── ingestion/       # Document ingestion
│   │   │   ├── clinical_memory/ # Processing pipeline
│   │   │   └── outputs/         # Clinical output generation
│   │   └── data/
│   │       └── demo_data.py     # Synthetic dataset
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx    # Patient list / demo load
│   │   │   └── PatientPage.tsx  # Main clinical dashboard
│   │   ├── components/
│   │   │   ├── ui/              # Shared UI components
│   │   │   ├── dashboard/       # Patient header, clinical snapshot
│   │   │   ├── timeline/        # Clinical timeline
│   │   │   ├── memory/          # Changes, loops, conflicts
│   │   │   └── outputs/         # Generated clinical outputs
│   │   ├── services/
│   │   │   └── api.ts           # API client
│   │   └── types/
│   │       └── index.ts         # TypeScript types
│   └── package.json
├── docs/
├── start.py                     # Combined startup script
└── README.md
```
