from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
import os

router = APIRouter()

# Root is 5 levels up from this file's directory: routers -> api -> ui_react -> src -> project_root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent

DOCS_MAPPING = {
    "report": PROJECT_ROOT / "GenAI_Report_AS1568_UC20.md",
    "system_guide": PROJECT_ROOT / "guide.md",
    "readme": PROJECT_ROOT / "README.md",
    "migration_guide": PROJECT_ROOT / "src" / "ui_react" / "guide.md"
}

class DocUpdate(BaseModel):
    content: str

@router.get("/image/{img_path:path}")
async def get_image(img_path: str):
    full_path = PROJECT_ROOT / img_path
    if not full_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(full_path)

@router.get("/{doc_key}")
async def get_doc(doc_key: str):
    if doc_key not in DOCS_MAPPING:
        raise HTTPException(status_code=404, detail="Document not found")
    
    file_path = DOCS_MAPPING[doc_key]
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"File {file_path.name} does not exist on disk")
    
    with open(file_path, "r", encoding="utf-8") as f:
        return {"content": f.read(), "filename": file_path.name}

@router.post("/{doc_key}")
async def update_doc(doc_key: str, update: DocUpdate):
    if doc_key not in DOCS_MAPPING:
        raise HTTPException(status_code=404, detail="Document not found")
    
    file_path = DOCS_MAPPING[doc_key]
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(update.content)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
