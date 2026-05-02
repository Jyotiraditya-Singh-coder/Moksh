from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from generator import generate_question
import logging

app = FastAPI()

class Profile(BaseModel):
    weakTopics: list[str]
    strongTopics: list[str]
    preferredLanguage: str = "en"

class QuestionResponse(BaseModel):
    question: str
    difficulty: str
    topic: str
    solution: str
    alternateApproach: str
    explanation: str
    learningTip: str

@app.post("/generate", response_model=QuestionResponse)
async def generate(profile: Profile):
    try:
        q = generate_question(profile.dict())
        return q
    except Exception as e:
        logging.error(e)
        raise HTTPException(500, detail=str(e))