#!/usr/bin/env python3
"""
THREAD startup helper — starts both backend and frontend.
Run: python start.py
"""
import subprocess
import sys
import os

BACKEND_DIR = os.path.join(os.path.dirname(__file__), "backend")
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")

print("=" * 60)
print("THREAD — Clinical Continuity Engine")
print("=" * 60)
print()
print("Starting backend (FastAPI) on http://localhost:8000 ...")
print("Starting frontend (Vite) on http://localhost:5173 ...")
print()
print("API Docs: http://localhost:8000/docs")
print()
print("Press Ctrl+C to stop.")
print()

backend = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
    cwd=BACKEND_DIR,
)

frontend = subprocess.Popen(
    ["npm", "run", "dev"],
    cwd=FRONTEND_DIR,
    shell=True,
)

try:
    backend.wait()
except KeyboardInterrupt:
    print("\nShutting down...")
    backend.terminate()
    frontend.terminate()
