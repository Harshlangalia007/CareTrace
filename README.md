# THREAD — Clinical Continuity Engine

> **IBM Bob Hackathon × VGEC**

---

## Team

| Field | Value |
|---|---|
| **Team Name** | CareTrace |
| **Track** | AI |
| **Team Lead** | Harsh Langalia — harshlanagalia10@gmail.com |
| **Members** | Nilabh Oza, Sahil Khankhal, Hetav Shah, Rishabh Jain, Yug Rajpurohit |

---

## Problem Statement

A hospital doctor spends 2 hours per day reading and summarising patient records for ward rounds, referral letters, and discharge summaries. A complex patient with multiple admissions may have 50–200 pages of records across departments. Key clinical events, medication changes, and outstanding investigations are buried in unstructured notes. Referral letters are often written from memory, creating gaps that cause avoidable readmissions and repeated investigations costing the NHS £1B+ annually.

---

## Solution

**THREAD** reconstructs a patient's complete clinical journey from fragmented records, building a structured **Clinical Memory** that prevents important information from being lost between episodes of care. It detects what changed, what is unresolved (open loops), and what conflicts exist across records — then generates evidence-linked handover documents for ward rounds, referrals, and discharge.

---

## Key Features

- **Clinical Timeline** — Chronological reconstruction of all clinical events from uploaded records
- **What Changed?** — Automated detection of medication changes, new diagnoses, worsening/improving markers
- **Open Loops** — Identification of outstanding investigations, referrals, and follow-ups not yet documented
- **Documentation Conflicts** — Detection of conflicting information across records (allergies, medications, diagnoses)
- **Evidence Linking** — Every AI insight is traceable to a specific source document
- **Next Clinician Brief** — "If you only have 60 seconds, read this" — AI-generated handover brief
- **Ward Round / Referral / Discharge** — Evidence-linked clinical output generation via IBM watsonx.ai

---

## Tech Stack

| Category | Technologies |
|---|---|
| **Languages** | Python, TypeScript |
| **Frameworks** | FastAPI, React, Vite |
| **IBM Technologies** | IBM watsonx.ai (Granite), IBM Bob |
| **Databases** | SQLite (SQLAlchemy ORM) |
| **Other** | Pydantic, React Router, date-fns |

---

## Repository Structure

```
thread/
├── backend/             # FastAPI backend
│   ├── app/
│   │   ├── main.py      # Application entry point
│   │   ├── models/      # 17-table relational data model
│   │   ├── routers/     # REST API routes
│   │   ├── services/    # LLM, ingestion, clinical memory, outputs
│   │   └── data/        # Synthetic demo dataset
│   └── requirements.txt
├── frontend/            # React/TypeScript frontend
│   └── src/
│       ├── pages/       # Dashboard, PatientPage
│       ├── components/  # Timeline, memory, outputs, UI
│       ├── services/    # API client
│       └── types/       # TypeScript types
├── docs/
│   └── setup-guide.md
└── start.py             # Combined startup script
```

---

## How to Run

See [`docs/setup-guide.md`](docs/setup-guide.md) for full setup instructions.

```bash
# 1. Install backend dependencies
cd backend && pip install -r requirements.txt

# 2. Install frontend dependencies
cd frontend && npm install

# 3. Start both services
cd .. && python start.py

# 4. Open http://localhost:5173
# 5. Click "Load Demo Patient" to load the synthetic dataset
```

---

## Demo

| Artifact | Link |
|---|---|
| Demo Video | [See demo/demo-video-link.txt](demo/demo-video-link.txt) |
| Live Demo | [See demo/live-demo-url.txt](demo/live-demo-url.txt) |
| Screenshots | [See demo/screenshots/](demo/screenshots/) |
| Presentation | [See presentation/](presentation/) |

---

## Known Limitations

- Authentication is mocked — not production-ready
- Tested on Chrome/Edge desktop
- LLM extraction runs in demo mode by default (pre-written realistic outputs)
- PDF extraction requires PyPDF2 (install separately if needed)
- No real-time updates — manual refresh required after document upload
- FHIR/EHR integration is scaffolded but not implemented (P2)

---

## What We're Most Proud Of

The **Clinical Memory data model** and the **Open Loop + Conflict detection system**. The synthetic demo dataset was designed to contain deliberately fragmented information across 10 documents — a penicillin allergy that conflicts between GP records and a hospital discharge summary, a CT scan recommended but never followed up, and a medication stopped mid-admission that needs a restart decision. The demo makes the value proposition immediately visible: the Clinical Memory reconstructs what a clinician would spend an hour reading.

---

## AI Safety Note

THREAD uses careful clinical language throughout:
- "The record indicates..." — never invented facts
- "Potentially outstanding" — never claims an event didn't happen
- "Conflicting documentation detected" — never resolves conflicts autonomously
- All generated outputs are marked **AI-GENERATED DRAFT — CLINICIAN REVIEW REQUIRED**
