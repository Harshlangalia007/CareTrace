"""
Timeline API router.
Returns chronological clinical events for the timeline UI component.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from app.database import get_db
from app.models import ClinicalEvent, Encounter, Document, Evidence

router = APIRouter(prefix="/timeline", tags=["timeline"])


class TimelineEventResponse(BaseModel):
    id: str
    event_type: str
    event_date: Optional[datetime]
    title: str
    description: Optional[str]
    clinical_significance: Optional[str]
    is_confirmed: bool
    source_document_id: Optional[str]
    source_document_title: Optional[str]
    evidence: List[dict] = []

    class Config:
        from_attributes = True


@router.get("/{patient_id}", response_model=List[TimelineEventResponse])
def get_timeline(patient_id: str, db: Session = Depends(get_db)):
    events = (
        db.query(ClinicalEvent)
        .filter(ClinicalEvent.patient_id == patient_id)
        .order_by(ClinicalEvent.event_date)
        .all()
    )

    result = []
    for evt in events:
        doc_title = None
        if evt.source_document_id:
            doc = db.query(Document).filter(Document.id == evt.source_document_id).first()
            doc_title = doc.title if doc else None

        evidence_items = db.query(Evidence).filter(Evidence.clinical_event_id == evt.id).all()
        evidence_data = [
            {"id": e.id, "text": e.extracted_text, "document_id": e.document_id}
            for e in evidence_items
        ]

        result.append(TimelineEventResponse(
            id=evt.id,
            event_type=evt.event_type,
            event_date=evt.event_date,
            title=evt.title,
            description=evt.description,
            clinical_significance=evt.clinical_significance,
            is_confirmed=evt.is_confirmed,
            source_document_id=evt.source_document_id,
            source_document_title=doc_title,
            evidence=evidence_data,
        ))

    return result
