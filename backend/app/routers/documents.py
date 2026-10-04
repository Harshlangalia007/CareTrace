"""
Documents API router.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from app.database import get_db
from app.models import Document, Patient
from app.services.ingestion.ingestion_service import ingest_document
from app.services.clinical_memory.memory_service import (
    process_document, run_change_detection, run_conflict_detection
)

router = APIRouter(prefix="/documents", tags=["documents"])


class DocumentResponse(BaseModel):
    id: str
    patient_id: str
    filename: str
    document_type: str
    document_date: Optional[datetime]
    title: Optional[str]
    source_author: Optional[str]
    source_institution: Optional[str]
    processed: bool

    class Config:
        from_attributes = True


@router.get("/patient/{patient_id}", response_model=List[DocumentResponse])
def list_patient_documents(patient_id: str, db: Session = Depends(get_db)):
    docs = (
        db.query(Document)
        .filter(Document.patient_id == patient_id)
        .order_by(Document.document_date)
        .all()
    )
    return docs


@router.post("/upload/{patient_id}", response_model=DocumentResponse, status_code=201)
async def upload_document(
    patient_id: str,
    file: UploadFile = File(...),
    document_type: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    content = await file.read()
    doc = ingest_document(db, patient_id, file.filename, content, document_type)

    # Process immediately
    try:
        process_document(db, doc.id)
        run_change_detection(db, patient_id)
        run_conflict_detection(db, patient_id)
    except Exception as e:
        # Non-fatal — document is ingested, processing failed
        pass

    db.refresh(doc)
    return doc


@router.post("/process/{document_id}", response_model=DocumentResponse)
def reprocess_document(document_id: str, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    doc = process_document(db, document_id)
    run_change_detection(db, doc.patient_id)
    run_conflict_detection(db, doc.patient_id)
    return doc


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: str, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@router.get("/{document_id}/text")
def get_document_text(document_id: str, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"id": doc.id, "title": doc.title, "raw_text": doc.raw_text}
