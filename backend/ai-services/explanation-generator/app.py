from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from generator import generate_explanation
import logging

app = FastAPI(title="Explanation Generator")

class ExplainRequest(BaseModel):
    factors: list[str]  # e.g., ["attendance dropped 10%", "test scores decreased"]
    language: str = "en"

class ExplainResponse(BaseModel):
    explanation: str

@app.post("/explain", response_model=ExplainResponse)
async def explain(req: ExplainRequest):
    try:
        explanation = generate_explanation(req.factors, req.language)
        return {"explanation": explanation}
    except Exception as e:
        logging.error(e)
        raise HTTPException(500, detail=str(e))