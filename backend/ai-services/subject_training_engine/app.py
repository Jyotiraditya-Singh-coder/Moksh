from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Tuple
import logging
from problem_generator import generate_problem
from solution_analyzer import analyze_solution
from math_validator import validate_math, validate_numerical, compare_algorithms_output
from algorithm_analyzer import analyze_algorithm
from knowledge_base import update_knowledge_base, search_similar_approaches, rebuild_index
from student_weakness import get_weakness_profile
from problem_sequencer import generate_personalized_sequence

app = FastAPI(title="Subject Training Engine")

# Request/Response Models
class GenerateProblemRequest(BaseModel):
    subject: str
    topic: str
    difficulty: str
    weakness_profile: List[str]
    previous_mistakes: Optional[List[str]] = None

class GenerateProblemResponse(BaseModel):
    problem_statement: str
    hints: List[str]
    solution_explanation: str
    alternative_approach: Optional[str] = None
    time_complexity: Optional[str] = None

class AnalyzeSolutionRequest(BaseModel):
    student_id: str
    problem_id: str
    solution_text: str
    code: Optional[str] = None
    topic: Optional[str] = None
    difficulty: Optional[str] = None
    correct: bool = False

class AnalyzeSolutionResponse(BaseModel):
    reasoning_strategy: str
    algorithm_pattern: Optional[str] = None
    mathematical_pattern: Optional[str] = None
    common_mistakes: List[str]
    time_complexity: Optional[str] = None
    suggested_improvement: Optional[str] = None
    concept_tags: List[str] = []

class ValidateMathRequest(BaseModel):
    expression: str
    steps: List[str]

class ValidateMathResponse(BaseModel):
    is_correct: bool
    simplified_expression: Optional[str] = None
    error_step: Optional[int] = None
    feedback: str

class ValidateNumericalRequest(BaseModel):
    expression: str
    expected_range: Optional[Tuple[float, float]] = None
    tolerance: str = "1e-15"

class ValidateNumericalResponse(BaseModel):
    is_valid: bool
    value: Optional[str] = None
    high_precision_value: Optional[str] = None
    interval_check: Optional[dict] = None
    error: Optional[str] = None

class CompareAlgorithmsRequest(BaseModel):
    algorithm1_expr: str
    algorithm2_expr: str
    precision: int = 100

class CompareAlgorithmsResponse(BaseModel):
    algorithm1_result: Optional[str] = None
    algorithm2_result: Optional[str] = None
    difference: Optional[str] = None
    are_equivalent: Optional[bool] = None
    error: Optional[str] = None

class AnalyzeAlgorithmRequest(BaseModel):
    code: str
    problem_description: str

class AnalyzeAlgorithmResponse(BaseModel):
    time_complexity: str
    space_complexity: str
    algorithm_type: str
    optimization_suggestions: List[str]

class SearchApproachesRequest(BaseModel):
    query: str
    top_k: int = 5
    topic_filter: Optional[str] = None

class SearchApproachesResponse(BaseModel):
    results: List[dict]

class WeaknessProfileRequest(BaseModel):
    student_id: str

class WeaknessProfileResponse(BaseModel):
    weak_concepts: List[str]
    strong_concepts: List[str]
    concept_stats: Dict[str, Any]

class PersonalizedSequenceRequest(BaseModel):
    student_id: str
    subject: str
    available_hours: float

class PersonalizedSequenceResponse(BaseModel):
    sequence: List[dict]
    total_time: float
    explanation: str

class RebuildIndexRequest(BaseModel):
    pass

# Endpoints
@app.post("/generate-problem", response_model=GenerateProblemResponse)
async def generate_problem_endpoint(req: GenerateProblemRequest):
    try:
        problem = generate_problem(req.dict())
        return problem
    except Exception as e:
        logging.error(f"Problem generation error: {e}")
        raise HTTPException(500, detail=str(e))

@app.post("/analyze-solution", response_model=AnalyzeSolutionResponse)
async def analyze_solution_endpoint(req: AnalyzeSolutionRequest):
    try:
        analysis = analyze_solution(req.dict())
        update_knowledge_base(
            student_id=req.student_id,
            problem_id=req.problem_id,
            analysis=analysis,
            topic=req.topic,
            difficulty=req.difficulty,
            correct=req.correct
        )
        return analysis
    except Exception as e:
        logging.error(f"Solution analysis error: {e}")
        raise HTTPException(500, detail=str(e))

@app.post("/validate-math", response_model=ValidateMathResponse)
async def validate_math_endpoint(req: ValidateMathRequest):
    try:
        result = validate_math(req.expression, req.steps)
        return result
    except Exception as e:
        logging.error(f"Math validation error: {e}")
        raise HTTPException(500, detail=str(e))

@app.post("/validate-numerical", response_model=ValidateNumericalResponse)
async def validate_numerical_endpoint(req: ValidateNumericalRequest):
    try:
        result = validate_numerical(req.expression, req.expected_range, req.tolerance)
        return result
    except Exception as e:
        logging.error(f"Numerical validation error: {e}")
        raise HTTPException(500, detail=str(e))

@app.post("/compare-algorithms", response_model=CompareAlgorithmsResponse)
async def compare_algorithms_endpoint(req: CompareAlgorithmsRequest):
    try:
        result = compare_algorithms_output(req.algorithm1_expr, req.algorithm2_expr, req.precision)
        return result
    except Exception as e:
        logging.error(f"Algorithm comparison error: {e}")
        raise HTTPException(500, detail=str(e))

@app.post("/analyze-algorithm", response_model=AnalyzeAlgorithmResponse)
async def analyze_algorithm_endpoint(req: AnalyzeAlgorithmRequest):
    try:
        analysis = analyze_algorithm(req.code, req.problem_description)
        return analysis
    except Exception as e:
        logging.error(f"Algorithm analysis error: {e}")
        raise HTTPException(500, detail=str(e))

@app.post("/search-approaches", response_model=SearchApproachesResponse)
async def search_approaches_endpoint(req: SearchApproachesRequest):
    try:
        results = search_similar_approaches(req.query, req.top_k, req.topic_filter)
        return {"results": results}
    except Exception as e:
        logging.error(f"Search error: {e}")
        raise HTTPException(500, detail=str(e))

@app.post("/weakness-profile", response_model=WeaknessProfileResponse)
async def weakness_profile_endpoint(req: WeaknessProfileRequest):
    try:
        profile = get_weakness_profile(req.student_id)
        return profile
    except Exception as e:
        logging.error(f"Weakness profile error: {e}")
        raise HTTPException(500, detail=str(e))

@app.post("/personalized-sequence", response_model=PersonalizedSequenceResponse)
async def personalized_sequence_endpoint(req: PersonalizedSequenceRequest):
    try:
        sequence = generate_personalized_sequence(req.student_id, req.subject, req.available_hours)
        return sequence
    except Exception as e:
        logging.error(f"Sequence generation error: {e}")
        raise HTTPException(500, detail=str(e))

@app.post("/rebuild-knowledge-base")
async def rebuild_knowledge_base(req: RebuildIndexRequest):
    try:
        rebuild_index()
        return {"message": "Knowledge base rebuilt"}
    except Exception as e:
        logging.error(e)
        raise HTTPException(500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}