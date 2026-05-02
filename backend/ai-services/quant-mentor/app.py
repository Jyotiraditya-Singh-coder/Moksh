from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import logging
from mentor import generate_quant_guide
from knowledge_graph import QuantKnowledgeGraph

app = FastAPI(title="Quant Trading Mentor")

kg = QuantKnowledgeGraph()

class GuideRequest(BaseModel):
    degree: str = "Computer Science"
    year: int = 1
    known_topics: List[str] = []
    target_firm: Optional[str] = None

class GuideResponse(BaseModel):
    core_skills: dict
    timeline: dict
    interview_questions: dict
    recommended_topics: List[str]
    explanation: str

class TopicInfoRequest(BaseModel):
    topic: str

class TopicInfoResponse(BaseModel):
    topic: str
    category: str
    difficulty: int
    description: str
    prerequisites: List[str]
    related: List[str]

class AddTopicRequest(BaseModel):
    topic_id: str
    category: str
    difficulty: int
    description: str
    prerequisites: List[str] = []

@app.post("/guide", response_model=GuideResponse)
async def get_quant_guide(req: GuideRequest):
    try:
        background = req.dict()
        guide = generate_quant_guide(background)
        return guide
    except Exception as e:
        logging.error(f"Guide generation error: {e}")
        raise HTTPException(500, detail=str(e))

@app.post("/topic-info", response_model=TopicInfoResponse)
async def get_topic_info(req: TopicInfoRequest):
    try:
        topic = req.topic
        info = kg.get_topic_info(topic)
        if not info:
            raise HTTPException(404, detail="Topic not found")
        prerequisites = kg.get_prerequisites(topic)
        related = kg.get_related(topic, depth=1)
        return {
            "topic": topic,
            "category": info.get("category", ""),
            "difficulty": info.get("difficulty", 1),
            "description": info.get("description", ""),
            "prerequisites": prerequisites,
            "related": related
        }
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Topic info error: {e}")
        raise HTTPException(500, detail=str(e))

@app.post("/add-topic")
async def add_topic(req: AddTopicRequest):
    try:
        kg.graph.add_node(req.topic_id,
                          category=req.category,
                          difficulty=req.difficulty,
                          description=req.description)
        for prereq in req.prerequisites:
            kg.graph.add_edge(prereq, req.topic_id)
        return {"message": "Topic added successfully"}
    except Exception as e:
        logging.error(e)
        raise HTTPException(500, detail=str(e))

@app.get("/topics")
async def list_topics():
    topics = kg.get_all_topics()
    return {"topics": [{"id": t[0], **t[1]} for t in topics]}

@app.get("/health")
async def health():
    return {"status": "ok"}