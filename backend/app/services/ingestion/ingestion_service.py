"""
Document Ingestion Service.
Handles file upload, text extraction, and document classification.
"""

import os
import io
import logging
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from app.models import Document, Patient
from app.config import settings

logger = logging.getLogger(__name__)

UPLOAD_DIR = settings.upload_dir
os.makedirs(UPLOAD_DIR, exist_ok=True)


def extract_text_from_file(content: bytes, filename: str) -> str:
    """Extract plain text from uploaded file bytes."""
    ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else "txt"

    if ext == "txt":
        try:
            return content.decode("utf-8")
        except UnicodeDecodeError:
            return content.decode("latin-1", errors="replace")

    if ext == "pdf":
        try:
            import PyPDF2
            reader = PyPDF2.PdfReader(io.BytesIO(content))
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as e:
            logger.warning("PDF extraction failed for %s: %s", filename, e)
            return ""

    if ext == "docx":
        try:
            import docx
            doc = docx.Document(io.BytesIO(content))
            return "\n".join(p.text for p in doc.paragraphs)
        except Exception as e:
            logger.warning("DOCX extraction failed for %s: %s", filename, e)
            return ""

    # Fallback — try plain text
    try:
        return content.decode("utf-8", errors="replace")
    except Exception:
        return ""


def ingest_document(
    db: Session,
    patient_id: str,
    filename: str,
    content: bytes,
    document_type: Optional[str] = None,
) -> Document:
    """
    Ingest a document for a patient.
    Saves the file, extracts text, and creates a Document record.
    """
    # Save file
    safe_name = filename.replace(" ", "_")
    file_path = os.path.join(UPLOAD_DIR, f"{patient_id}_{safe_name}")
    with open(file_path, "wb") as f:
        f.write(content)

    raw_text = extract_text_from_file(content, filename)

    doc = Document(
        patient_id=patient_id,
        filename=filename,
        document_type=document_type or "other",
        raw_text=raw_text,
        file_path=file_path,
        processed=False,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    logger.info("Ingested document %s for patient %s", doc.id, patient_id)
    return doc
