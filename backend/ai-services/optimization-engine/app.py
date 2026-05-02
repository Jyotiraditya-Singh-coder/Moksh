from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from optimizer import optimize_study_plan
import logging

app = FastAPI()

class OptimizeRequest(BaseModel):
    weakTopics: list[str]  # list of topic names (gain will be assigned)
    strongTopics: list[str]
    availableHours: float
    difficultyPreference: str
    dropoutRisk: float
    careerGoal: str

class OptimizeResponse(BaseModel):
    recommendedStudyHours: float
    optimizedTopicSequence: list[str]
    dailyPlan: list[dict]

@app.post("/optimize", response_model=OptimizeResponse)
async def optimize(req: OptimizeRequest):
    try:
        # Convert topics to list of (name, gain) - gain could be derived from weak/strong
        weak_with_gain = [(t, 0.8) for t in req.weakTopics]  # placeholder gain
        strong_with_gain = [(t, 0.3) for t in req.strongTopics]
        plan = optimize_study_plan(weak_with_gain, strong_with_gain,
                                    req.availableHours, req.difficultyPreference,
                                    req.dropoutRisk, req.careerGoal)
        return plan
    except Exception as e:
        logging.error(e)
        raise HTTPException(500, detail=str(e))