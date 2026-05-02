# ai-services/skill-navigator/app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import logging
from learner_profiler import LearnerProfiler
from knowledge_tracer import KnowledgeTracer
from path_optimizer import PathOptimizer
from career_aligner import CareerAligner
import numpy as np
import mlflow
import os
import joblib

app = FastAPI(title="Skill Navigator")

# Initialize components
profiler = LearnerProfiler()
kt = KnowledgeTracer()
optimizer = PathOptimizer()
career = CareerAligner()

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# Load knowledge tracer model from MLflow if available
def load_kt_model():
    global kt
    client = mlflow.tracking.MlflowClient()
    versions = client.get_latest_versions("knowledge_tracer", stages=["Production"])
    if versions:
        model_uri = f"models:/knowledge_tracer/Production"
        kt.model = mlflow.pyfunc.load_model(model_uri)
        kt.trained = True
    else:
        # Fallback: use untrained model
        pass
load_kt_model()

# Request/Response Models
class Interaction(BaseModel):
    skill_id: str
    correct: bool
    time_spent: float
    hints_used: int
    concept_tags: List[str] = []
    reasoning_strategy: Optional[str] = None

class ProfileRequest(BaseModel):
    student_id: str
    interactions: List[Interaction]

class ProfileResponse(BaseModel):
    student_id: str
    skill_mastery: Dict[str, float]
    avg_time_per_problem: float
    hint_dependency: float
    concept_strengths: List[str]
    concept_weaknesses: List[str]
    dominant_reasoning_strategy: str
    total_interactions: int

class PathRequest(BaseModel):
    student_id: str
    target_role: Optional[str] = None
    hours_available: Optional[float] = 10

class PathStep(BaseModel):
    skill_id: str
    reason: str
    estimated_hours: float
    resources: List[str]

class PathResponse(BaseModel):
    path: List[PathStep]
    total_estimated_hours: float
    explanation: str

class ReadinessRequest(BaseModel):
    student_id: str
    target_role: str
    skill_mastery: Dict[str, float]

class ReadinessResponse(BaseModel):
    target_role: str
    readiness_score: float
    missing_required: List[str]
    missing_preferred: List[str]
    has_required: List[str]

class TrainKTRequest(BaseModel):
    data_source: str = "mongodb"

class FineTuneKTData(BaseModel):
    features: List[List[float]]
    labels: List[int]

# Endpoints
@app.post("/profile", response_model=ProfileResponse)
async def create_profile(req: ProfileRequest):
    try:
        interactions = [i.dict() for i in req.interactions]
        profile = profiler.create_profile(req.student_id, interactions)
        return profile
    except Exception as e:
        logging.error(f"Profile error: {e}")
        raise HTTPException(500, detail=str(e))

@app.post("/optimal-path", response_model=PathResponse)
async def optimal_path(req: PathRequest):
    try:
        # In a real system, fetch profile from DB; for demo use empty profile
        dummy_profile = {
            "student_id": req.student_id,
            "skill_mastery": {},
            "avg_time_per_problem": 0,
            "hint_dependency": 0,
            "concept_strengths": [],
            "concept_weaknesses": [],
            "dominant_reasoning_strategy": "unknown",
            "total_interactions": 0
        }
        result = optimizer.generate_optimal_path(req.student_id, dummy_profile, req.target_role)
        path_steps = [PathStep(**step) for step in result.get("path", [])]
        return PathResponse(
            path=path_steps,
            total_estimated_hours=result.get("total_estimated_hours", 0),
            explanation=result.get("explanation", "")
        )
    except Exception as e:
        logging.error(f"Path error: {e}")
        raise HTTPException(500, detail=str(e))

@app.post("/career-readiness", response_model=ReadinessResponse)
async def career_readiness(req: ReadinessRequest):
    try:
        result = career.analyze_readiness(req.skill_mastery, req.target_role)
        return result
    except Exception as e:
        logging.error(f"Career readiness error: {e}")
        raise HTTPException(500, detail=str(e))

@app.post("/train-kt")
async def train_kt(req: TrainKTRequest):
    try:
        # Generate synthetic data for demonstration
        np.random.seed(42)
        X = np.random.rand(1000, 5)
        y = (X.sum(axis=1) > 2.5).astype(int)

        kt.train(X, y)

        kt.save("kt_model.pkl")
        with mlflow.start_run() as run:
            mlflow.log_artifact("kt_model.pkl")
            run_id = run.info.run_id
            mlflow.register_model(f"runs:/{run_id}/kt_model.pkl", "knowledge_tracer")

        return {"message": "Knowledge tracer trained successfully"}
    except Exception as e:
        logging.error(e)
        raise HTTPException(500, detail=str(e))

@app.post("/fine-tune-kt")
async def fine_tune_kt(data: FineTuneKTData):
    try:
        X = np.array(data.features)
        y = np.array(data.labels)
        kt.train(X, y)
        kt.save("kt_model.pkl")
        with mlflow.start_run() as run:
            mlflow.log_artifact("kt_model.pkl")
            run_id = run.info.run_id
            mlflow.register_model(f"runs:/{run_id}/kt_model.pkl", "knowledge_tracer")
        return {"message": "Knowledge tracer fine-tuned successfully"}
    except Exception as e:
        logging.error(e)
        raise HTTPException(500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}