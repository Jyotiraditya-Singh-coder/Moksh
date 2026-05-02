from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging
from authoring_copilot import generate_lesson
from media_studio import text_to_speech, generate_image
from taxonomy_extractor import SkillTaxonomyExtractor

app = FastAPI(title="Content Authoring")

taxonomy = SkillTaxonomyExtractor()

class LessonRequest(BaseModel):
    prompt: str
    subject: str
    grade: str

class LessonResponse(BaseModel):
    lesson: dict
    audio_url: Optional[str] = None

class SkillExtractRequest(BaseModel):
    text: str

class AddSkillRequest(BaseModel):
    skill_id: str
    description: str

@app.post("/generate-lesson", response_model=LessonResponse)
async def create_lesson(req: LessonRequest):
    try:
        lesson = generate_lesson(req.prompt, req.subject, req.grade)
        summary = lesson.get("content", [{}])[0].get("body", "")
        audio_b64 = text_to_speech(summary)
        return {"lesson": lesson, "audio_url": f"data:audio/mp3;base64,{audio_b64}"}
    except Exception as e:
        logging.error(e)
        raise HTTPException(500, detail=str(e))

@app.post("/extract-skills")
async def extract_skills(req: SkillExtractRequest):
    try:
        skills = taxonomy.extract_skills(req.text)
        return {"skills": skills}
    except Exception as e:
        logging.error(e)
        raise HTTPException(500, detail=str(e))

@app.post("/add-skill")
async def add_skill(req: AddSkillRequest):
    try:
        taxonomy.add_custom_skill(req.skill_id, req.description)
        return {"message": "Skill added"}
    except Exception as e:
        logging.error(e)
        raise HTTPException(500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}