# ai-services/dsa-trainer/app.py

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging
import uuid
from dsa_topics import get_all_topics, get_topic_info
from problem_generator import generate_problem
from solution_analyzer import analyze_solution
from progress_tracker import update_progress, get_weak_topics
from trending_topics import get_trending_topics, update_custom_trends

app = FastAPI(title="DSA Trainer Service")

# -----------------------------------------------------------------------------
# Pydantic Models
# -----------------------------------------------------------------------------
class ProblemRequest(BaseModel):
    topic: str
    difficulty: str = "medium"
    student_id: Optional[str] = None

class ProblemResponse(BaseModel):
    problem_id: str
    problem_statement: str
    input_format: str
    output_format: str
    constraints: str
    sample_inputs: List[str]
    sample_outputs: List[str]
    hints: List[str]
    expected_time_complexity: str
    expected_space_complexity: str
    topic: str
    difficulty: str

class SolutionRequest(BaseModel):
    problem_id: str
    student_id: str
    code: str
    language: str = "python"
    time_spent: float

class SolutionResponse(BaseModel):
    is_correct: bool
    time_complexity: str
    space_complexity: str
    missed_edge_cases: List[str]
    code_quality_suggestions: List[str]
    alternative_approaches: List[str]
    verdict: str
    explanation: str

class WeakTopicsResponse(BaseModel):
    weak_topics: List[str]

# Models for trending topics
class TrendingTopicsRequest(BaseModel):
    source: str = "hybrid"  # "hybrid", "groq", "custom", "fallback"

class TrendingTopicsResponse(BaseModel):
    topics: List[Dict[str, Any]]
    source: str
    count: int

class UpdateTrendsRequest(BaseModel):
    topics: List[Dict[str, Any]]

# -----------------------------------------------------------------------------
# Existing endpoints
# -----------------------------------------------------------------------------
@app.get("/topics")
async def list_topics():
    """Return all available DSA topics."""
    return {"topics": get_all_topics()}

@app.get("/topic/{topic_id}")
async def topic_info(topic_id: str):
    """Get information about a specific topic."""
    info = get_topic_info(topic_id)
    if not info:
        raise HTTPException(404, "Topic not found")
    return info

@app.post("/generate", response_model=ProblemResponse)
async def generate_new_problem(req: ProblemRequest):
    """Generate a DSA problem based on topic and difficulty."""
    try:
        # Optionally get student's weak topics if student_id provided
        weak_topics = []
        if req.student_id:
            weak_topics = await get_weak_topics(req.student_id)
        
        problem = await generate_problem(req.topic, req.difficulty, weak_topics)
        problem_id = str(uuid.uuid4())
        # In production, store problem in DB with this ID
        return ProblemResponse(problem_id=problem_id, **problem)
    except Exception as e:
        logging.error(f"Problem generation error: {e}")
        raise HTTPException(500, detail=str(e))

@app.post("/analyze", response_model=SolutionResponse)
async def analyze_submission(req: SolutionRequest, background_tasks: BackgroundTasks):
    """Analyze a submitted solution and update progress."""
    try:
        # In production, fetch the problem from DB using req.problem_id.
        # For now, we construct a minimal problem dict (topic/difficulty may be stored separately)
        problem = {
            "problem_statement": "Placeholder",  # would be retrieved from DB
            "topic": "arrays",                    # placeholder
            "difficulty": "medium"                 # placeholder
        }
        analysis = await analyze_solution(problem, req.code, req.language)
        
        background_tasks.add_task(
            update_progress,
            req.student_id,
            req.problem_id,
            problem.get("topic", "unknown"),
            problem.get("difficulty", "unknown"),
            analysis.get("is_correct", False),
            req.time_spent
        )
        return SolutionResponse(**analysis)
    except Exception as e:
        logging.error(f"Solution analysis error: {e}")
        raise HTTPException(500, detail=str(e))

@app.get("/weak-topics/{student_id}", response_model=WeakTopicsResponse)
async def weak_topics(student_id: str):
    """Get topics where the student struggles."""
    topics = await get_weak_topics(student_id)
    return {"weak_topics": topics}

# -----------------------------------------------------------------------------
# Trending topics endpoints
# -----------------------------------------------------------------------------
@app.post("/trending-topics", response_model=TrendingTopicsResponse)
async def get_trending(req: TrendingTopicsRequest):
    """
    Get current hot DSA topics.
    Source can be:
    - "hybrid": scrape then synthesize with Groq (default)
    - "groq": only Groq (fallback)
    - "custom": use manually set custom trends
    - "fallback": use hardcoded fallback
    """
    try:
        topics = await get_trending_topics(req.source)
        return TrendingTopicsResponse(
            topics=topics,
            source=req.source,
            count=len(topics)
        )
    except Exception as e:
        logging.error(f"Trending topics error: {e}")
        raise HTTPException(500, detail=str(e))

@app.post("/trending-topics/update", status_code=200)
async def update_trends(req: UpdateTrendsRequest):
    """
    Update the custom trends data (fine-tuning).
    This allows overriding the generated trends with your own data.
    """
    try:
        result = update_custom_trends(req.topics)
        return result
    except Exception as e:
        logging.error(f"Update trends error: {e}")
        raise HTTPException(500, detail=str(e))


@app.get("/health")
async def health():
    return {"status": "ok"}