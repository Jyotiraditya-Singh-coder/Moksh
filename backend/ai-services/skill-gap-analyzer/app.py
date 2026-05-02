from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import logging
from analyzer import (
    analyze,
    add_job_role,
    get_all_job_roles,
    rebuild_index_from_metadata
)

app = FastAPI(title="Skill Gap Analyzer")

# Request/Response models
class AnalyzeRequest(BaseModel):
    resumeText: str
    targetRole: str

class AnalyzeResponse(BaseModel):
    missingSkills: List[str]
    roadmap: List[dict]

class AddJobRoleRequest(BaseModel):
    job_title: str
    skills: List[str]

class JobRoleResponse(BaseModel):
    title: str
    skills: List[str]

# Existing endpoint
@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_endpoint(req: AnalyzeRequest):
    try:
        result = analyze(req.resumeText, req.targetRole)
        return result
    except Exception as e:
        logging.error(f"Analysis error: {e}")
        raise HTTPException(500, detail=str(e))

# NEW: Add a job role (fine‑tuning)
@app.post("/add-job-role", response_model=JobRoleResponse)
async def add_job_role_endpoint(req: AddJobRoleRequest):
    try:
        add_job_role(req.job_title, req.skills)
        return {"title": req.job_title, "skills": req.skills}
    except Exception as e:
        logging.error(f"Add job role error: {e}")
        raise HTTPException(500, detail=str(e))

# NEW: List all job roles
@app.get("/job-roles", response_model=List[JobRoleResponse])
async def list_job_roles():
    try:
        return get_all_job_roles()
    except Exception as e:
        logging.error(f"List job roles error: {e}")
        raise HTTPException(500, detail=str(e))

# NEW: Rebuild FAISS index (e.g., after many additions)
@app.post("/rebuild-index")
async def rebuild_index():
    try:
        rebuild_index_from_metadata()
        return {"message": "Index rebuilt successfully"}
    except Exception as e:
        logging.error(f"Rebuild index error: {e}")
        raise HTTPException(500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}