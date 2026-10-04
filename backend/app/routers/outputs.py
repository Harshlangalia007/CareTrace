"""
Outputs API router.
Generates clinical outputs: Next Clinician Brief, Ward Round, Referral, Discharge.
"""

from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from app.database import get_db
from app.models import GeneratedOutput, Patient
from app.services.clinical_memory.memory_service import build_patient_context
from app.services.llm.llm_service import llm_service

router = APIRouter(prefix="/outputs", tags=["outputs"])


class GenerateRequest(BaseModel):
    specialty: Optional[str] = None  # for referral


class OutputResponse(BaseModel):
    id: str
    patient_id: str
    output_type: str
    content: str
    evidence_refs: List[str]
    generated_at: datetime
    model_used: Optional[str]
    is_demo: bool

    class Config:
        from_attributes = True


def _get_patient_or_404(patient_id: str, db: Session) -> Patient:
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


def _save_output(db: Session, patient_id: str, output_type: str, content: str, is_demo: bool) -> GeneratedOutput:
    output = GeneratedOutput(
        patient_id=patient_id,
        output_type=output_type,
        content=content,
        model_used=llm_service._client.__class__.__name__ if llm_service._client else "demo",
        is_demo=is_demo,
    )
    db.add(output)
    db.commit()
    db.refresh(output)
    return output


@router.post("/{patient_id}/next-clinician-brief", response_model=OutputResponse)
def generate_next_clinician_brief(patient_id: str, db: Session = Depends(get_db)):
    _get_patient_or_404(patient_id, db)
    context = build_patient_context(db, patient_id)
    content = llm_service.generate_clinician_brief(context)
    output = _save_output(db, patient_id, "next_clinician_brief", content, llm_service.demo_mode)
    return output


@router.post("/{patient_id}/ward-round", response_model=OutputResponse)
def generate_ward_round(patient_id: str, db: Session = Depends(get_db)):
    _get_patient_or_404(patient_id, db)
    context = build_patient_context(db, patient_id)
    content = llm_service.generate_ward_round(context)
    output = _save_output(db, patient_id, "ward_round", content, llm_service.demo_mode)
    return output


@router.post("/{patient_id}/referral", response_model=OutputResponse)
def generate_referral(patient_id: str, request: GenerateRequest = None, db: Session = Depends(get_db)):
    _get_patient_or_404(patient_id, db)
    context = build_patient_context(db, patient_id)
    specialty = (request.specialty if request else None) or ""
    content = llm_service.generate_referral(context, specialty)
    output = _save_output(db, patient_id, "referral", content, llm_service.demo_mode)
    return output


@router.post("/{patient_id}/discharge", response_model=OutputResponse)
def generate_discharge(patient_id: str, db: Session = Depends(get_db)):
    _get_patient_or_404(patient_id, db)
    context = build_patient_context(db, patient_id)
    content = llm_service.generate_discharge(context)
    output = _save_output(db, patient_id, "discharge", content, llm_service.demo_mode)
    return output


@router.get("/{patient_id}/history", response_model=List[OutputResponse])
def get_output_history(patient_id: str, db: Session = Depends(get_db)):
    _get_patient_or_404(patient_id, db)
    outputs = (
        db.query(GeneratedOutput)
        .filter(GeneratedOutput.patient_id == patient_id)
        .order_by(GeneratedOutput.generated_at.desc())
        .all()
    )
    return outputs


@router.get("/{patient_id}/latest/{output_type}", response_model=OutputResponse)
def get_latest_output(patient_id: str, output_type: str, db: Session = Depends(get_db)):
    output = (
        db.query(GeneratedOutput)
        .filter(
            GeneratedOutput.patient_id == patient_id,
            GeneratedOutput.output_type == output_type
        )
        .order_by(GeneratedOutput.generated_at.desc())
        .first()
    )
    if not output:
        raise HTTPException(status_code=404, detail="Output not found")
    return output
