"""
Demo seed router — loads the synthetic demo dataset.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import (
    Patient, Document, Encounter, ClinicalEvent, Condition,
    Medication, MedicationChange, Investigation, OpenLoop,
    Conflict, DetectedChange
)
from app.data.demo_data import (
    get_demo_patient, get_demo_documents, get_demo_encounters,
    get_demo_clinical_events, get_demo_conditions, get_demo_medications,
    get_demo_medication_changes, get_demo_open_loops, get_demo_conflicts,
    get_demo_detected_changes, get_demo_investigations, DEMO_PATIENT_ID
)

router = APIRouter(prefix="/demo", tags=["demo"])


@router.post("/seed")
def seed_demo_data(db: Session = Depends(get_db)):
    """Load the synthetic demo dataset. Idempotent — clears existing demo data first."""

    # Clear existing demo data
    existing = db.query(Patient).filter(Patient.id == DEMO_PATIENT_ID).first()
    if existing:
        db.delete(existing)
        db.commit()

    # Patient
    patient_data = get_demo_patient()
    patient = Patient(**patient_data)
    db.add(patient)
    db.flush()

    # Documents
    for d in get_demo_documents():
        doc = Document(**d)
        db.add(doc)
    db.flush()

    # Encounters
    for e in get_demo_encounters():
        enc = Encounter(**e)
        db.add(enc)
    db.flush()

    # Conditions
    for c in get_demo_conditions():
        cond = Condition(**c)
        db.add(cond)
    db.flush()

    # Medications
    for m in get_demo_medications():
        med = Medication(**m)
        db.add(med)
    db.flush()

    # Medication changes
    for mc in get_demo_medication_changes():
        change = MedicationChange(**mc)
        db.add(change)
    db.flush()

    # Investigations
    for inv in get_demo_investigations():
        investigation = Investigation(**inv)
        db.add(investigation)
    db.flush()

    # Clinical events
    for evt in get_demo_clinical_events():
        event = ClinicalEvent(**evt)
        db.add(event)
    db.flush()

    # Open loops
    for ol in get_demo_open_loops():
        loop = OpenLoop(**ol)
        db.add(loop)
    db.flush()

    # Conflicts
    for cf in get_demo_conflicts():
        conflict = Conflict(**cf)
        db.add(conflict)
    db.flush()

    # Detected changes
    for ch in get_demo_detected_changes():
        detected = DetectedChange(**ch)
        db.add(detected)

    db.commit()

    doc_count = db.query(Document).filter(Document.patient_id == DEMO_PATIENT_ID).count()
    enc_count = db.query(Encounter).filter(Encounter.patient_id == DEMO_PATIENT_ID).count()
    event_count = db.query(ClinicalEvent).filter(ClinicalEvent.patient_id == DEMO_PATIENT_ID).count()
    loop_count = db.query(OpenLoop).filter(OpenLoop.patient_id == DEMO_PATIENT_ID).count()
    conflict_count = db.query(Conflict).filter(Conflict.patient_id == DEMO_PATIENT_ID).count()

    return {
        "status": "seeded",
        "patient_id": DEMO_PATIENT_ID,
        "documents": doc_count,
        "encounters": enc_count,
        "clinical_events": event_count,
        "open_loops": loop_count,
        "conflicts": conflict_count,
    }


@router.get("/status")
def demo_status(db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == DEMO_PATIENT_ID).first()
    return {
        "demo_loaded": patient is not None,
        "patient_id": DEMO_PATIENT_ID if patient else None,
    }
