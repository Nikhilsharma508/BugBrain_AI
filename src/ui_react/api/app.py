import sys
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add project root to python path to ensure imports work from anywhere
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

# Change working directory to project root so that relative paths
# (e.g. VECTOR_STORE_PATH="Data/vector_store") resolve correctly,
# matching the behavior when running Streamlit from project root.
os.chdir(project_root)

from src.ui_react.api.routers import triage, dashboard, docs

app = FastAPI(
    title="AI Bug Triage API",
    description="Backend API for the React-based Bug Triage Dashboard",
    version="1.0.0"
)

# Configure CORS for local development with Vite
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(triage.router, prefix="/api/triage", tags=["triage"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(docs.router, prefix="/api/docs", tags=["docs"])

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "Bug Triage API is running."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.ui_react.api.app:app", host="0.0.0.0", port=8000, reload=True)
