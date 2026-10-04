"""
Patients API router.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models import Patient, Document, Encounter, ClinicalEvent

router = APIRouter(prefix="/patients", tags=["patients"])


class PatientCreate(BaseModel):
    identifier: str
    age: Optional[int] = None
    sex: Optional[str] = None
    major_conditions: Optional[List[str]] = []
    current_admission: Optional[str] = None


class PatientResponse(BaseModel):
    id: str
    identifier: str
    age: Optional[int]
    sex: Optional[str]
    major_conditions: List[str]
    current_admission: Optional[str]
    document_count: int = 0
    encounter_count: int = 0

    class Config:
        from_attributes = True


@router.get("/", response_model=List[PatientResponse])
def list_patients(db: Session = Depends(get_db)):
    patients = db.query(Patient).all()
    result = []
    for p in patients:
        doc_count = db.query(Document).filter(Document.patient_id == p.id).count()
        enc_count = db.query(Encounter).filter(Encounter.patient_id == p.id).count()
        result.append(PatientResponse(
            id=p.id, identifier=p.identifier, age=p.age, sex=p.sex,
            major_conditions=p.major_conditions or [],
            current_admission=p.current_admission,
            document_count=doc_count,
            encounter_count=enc_count,
        ))
    return result


@router.post("/", response_model=PatientResponse, status_code=201)
def create_patient(data: PatientCreate, db: Session = Depends(get_db)):
    existing = db.query(Patient).filter(Patient.identifier == data.identifier).first()
    if existing:
        raise HTTPException(status_code=400, detail="Patient identifier already exists")
    patient = Patient(**data.model_dump())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return PatientResponse(
        id=patient.id, identifier=patient.identifier, age=patient.age,
        sex=patient.sex, major_conditions=patient.major_conditions or [],
        current_admission=patient.current_admission,
        document_count=0, encounter_count=0
    )


@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: str, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    doc_count = db.query(Document).filter(Document.patient_id == patient_id).count()
    enc_count = db.query(Encounter).filter(Encounter.patient_id == patient_id).count()
    return PatientResponse(
        id=patient.id, identifier=patient.identifier, age=patient.age,
        sex=patient.sex, major_conditions=patient.major_conditions or [],
        current_admission=patient.current_admission,
        document_count=doc_count, encounter_count=enc_count,
    )


@router.delete("/{patient_id}", status_code=204)
def delete_patient(patient_id: str, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    db.delete(patient)
    db.commit()
