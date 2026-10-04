"""
THREAD — Clinical Continuity Engine
FastAPI Application Entry Point
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
# Import models to ensure they are registered with Base before create_all
import app.models.models  # noqa: F401
from app.routers import patients, documents, memory, outputs, timeline, demo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    Base.metadata.create_all(bind=engine)
    logger.info("THREAD Clinical Continuity Engine — started")
    yield
    logger.info("THREAD — shutdown")


app = FastAPI(
    title="THREAD — Clinical Continuity Engine",
    description=(
        "THREAD reconstructs the patient's clinical journey and prevents important "
        "information from being lost between episodes of care."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(patients.router)
app.include_router(documents.router)
app.include_router(memory.router)
app.include_router(outputs.router)
app.include_router(timeline.router)
app.include_router(demo.router)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "THREAD Clinical Continuity Engine"}
