"""
Clinical Memory API router.
Returns the structured clinical memory for a patient.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from app.database import get_db
from app.models import (
    ClinicalEvent, Condition, Medication, Investigation, InvestigationResult,
    OpenLoop, Conflict, DetectedChange, Evidence, Document
)

router = APIRouter(prefix="/memory", tags=["clinical-memory"])


# ─────────────────────────────────────────────
# Response schemas
# ─────────────────────────────────────────────

class ConditionResponse(BaseModel):
    id: str
    name: str
    status: str
    onset_date: Optional[datetime]
    resolved_date: Optional[datetime]
    notes: Optional[str]
    source_document_id: Optional[str]

    class Config:
        from_attributes = True


class MedicationResponse(BaseModel):
    id: str
    name: str
    dose: Optional[str]
    route: Optional[str]
    frequency: Optional[str]
    status: str
    start_date: Optional[datetime]
    stop_date: Optional[datetime]
    stop_reason: Optional[str]
    source_document_id: Optional[str]

    class Config:
        from_attributes = True


class InvestigationResponse(BaseModel):
    id: str
    name: str
    investigation_type: Optional[str]
    requested_date: Optional[datetime]
    result_date: Optional[datetime]
    status: str
    source_document_id: Optional[str]

    class Config:
        from_attributes = True


class OpenLoopResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    loop_type: Optional[str]
    status: str
    requested_date: Optional[datetime]
    source_document_id: Optional[str]
    evidence_text: Optional[str]
    latest_matching_record: Optional[str]
    action_required: Optional[str]

    class Config:
        from_attributes = True


class ConflictResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    conflict_type: Optional[str]
    severity: str
    source_a_document_id: Optional[str]
    source_b_document_id: Optional[str]
    source_a_text: Optional[str]
    source_b_text: Optional[str]
    action_required: Optional[str]
    resolved: bool

    class Config:
        from_attributes = True


class DetectedChangeResponse(BaseModel):
    id: str
    change_type: str
    title: str
    entity_name: Optional[str]
    previous_state: Optional[str]
    current_state: Optional[str]
    change_date: Optional[datetime]
    reason: Optional[str]
    source_document_id: Optional[str]
    evidence_text: Optional[str]

    class Config:
        from_attributes = True


class ClinicalEventResponse(BaseModel):
    id: str
    event_type: str
    event_date: Optional[datetime]
    title: str
    description: Optional[str]
    clinical_significance: Optional[str]
    is_confirmed: bool
    confidence: float
    source_document_id: Optional[str]

    class Config:
        from_attributes = True


class EvidenceResponse(BaseModel):
    id: str
    document_id: str
    extracted_text: str
    section: Optional[str]
    confidence: float

    class Config:
        from_attributes = True


# ─────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────

@router.get("/{patient_id}/conditions", response_model=List[ConditionResponse])
def get_conditions(patient_id: str, db: Session = Depends(get_db)):
    return db.query(Condition).filter(Condition.patient_id == patient_id).all()


@router.get("/{patient_id}/medications", response_model=List[MedicationResponse])
def get_medications(patient_id: str, db: Session = Depends(get_db)):
    return db.query(Medication).filter(Medication.patient_id == patient_id).all()


@router.get("/{patient_id}/investigations", response_model=List[InvestigationResponse])
def get_investigations(patient_id: str, db: Session = Depends(get_db)):
    return db.query(Investigation).filter(Investigation.patient_id == patient_id).all()


@router.get("/{patient_id}/open-loops", response_model=List[OpenLoopResponse])
def get_open_loops(patient_id: str, db: Session = Depends(get_db)):
    return db.query(OpenLoop).filter(OpenLoop.patient_id == patient_id).all()


@router.get("/{patient_id}/conflicts", response_model=List[ConflictResponse])
def get_conflicts(patient_id: str, db: Session = Depends(get_db)):
    return db.query(Conflict).filter(Conflict.patient_id == patient_id).all()


@router.get("/{patient_id}/changes", response_model=List[DetectedChangeResponse])
def get_changes(patient_id: str, db: Session = Depends(get_db)):
    return db.query(DetectedChange).filter(DetectedChange.patient_id == patient_id).all()


@router.get("/{patient_id}/events", response_model=List[ClinicalEventResponse])
def get_events(patient_id: str, db: Session = Depends(get_db)):
    return (
        db.query(ClinicalEvent)
        .filter(ClinicalEvent.patient_id == patient_id)
        .order_by(ClinicalEvent.event_date)
        .all()
    )


@router.get("/{patient_id}/evidence/{event_id}", response_model=List[EvidenceResponse])
def get_evidence_for_event(patient_id: str, event_id: str, db: Session = Depends(get_db)):
    return db.query(Evidence).filter(Evidence.clinical_event_id == event_id).all()


@router.get("/{patient_id}/summary")
def get_clinical_summary(patient_id: str, db: Session = Depends(get_db)):
    """Full clinical memory summary for the patient."""
    conditions = db.query(Condition).filter(Condition.patient_id == patient_id).all()
    meds = db.query(Medication).filter(Medication.patient_id == patient_id).all()
    investigations = db.query(Investigation).filter(Investigation.patient_id == patient_id).all()
    open_loops = db.query(OpenLoop).filter(OpenLoop.patient_id == patient_id).all()
    conflicts = db.query(Conflict).filter(Conflict.patient_id == patient_id).all()
    changes = db.query(DetectedChange).filter(DetectedChange.patient_id == patient_id).all()
    events = (
        db.query(ClinicalEvent)
        .filter(ClinicalEvent.patient_id == patient_id)
        .order_by(ClinicalEvent.event_date)
        .all()
    )

    return {
        "patient_id": patient_id,
        "conditions": [{"id": c.id, "name": c.name, "status": c.status} for c in conditions],
        "active_medications": [
            {"id": m.id, "name": m.name, "dose": m.dose, "status": m.status}
            for m in meds if m.status == "active"
        ],
        "stopped_medications": [
            {"id": m.id, "name": m.name, "dose": m.dose, "stop_reason": m.stop_reason}
            for m in meds if m.status == "stopped"
        ],
        "pending_investigations": [
            {"id": i.id, "name": i.name, "status": i.status}
            for i in investigations if i.status == "pending"
        ],
        "open_loops_count": len(open_loops),
        "conflicts_count": len(conflicts),
        "recent_changes": [
            {"title": ch.title, "type": ch.change_type}
            for ch in changes[:5]
        ],
        "timeline_events": len(events),
    }
