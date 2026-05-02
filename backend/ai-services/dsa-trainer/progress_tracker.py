import pymongo
import os
from datetime import datetime

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/")
client = pymongo.MongoClient(MONGO_URI)
db = client["edunex"]
collection = db["dsa_progress"]

async def update_progress(student_id: str, problem_id: str, topic: str, difficulty: str, correct: bool, time_spent: float):
    """
    Store student's attempt in MongoDB.
    """
    record = {
        "student_id": student_id,
        "problem_id": problem_id,
        "topic": topic,
        "difficulty": difficulty,
        "correct": correct,
        "time_spent": time_spent,
        "timestamp": datetime.utcnow()
    }
    collection.insert_one(record)

async def get_student_progress(student_id: str):
    """
    Retrieve all attempts for a student.
    """
    cursor = collection.find({"student_id": student_id}).sort("timestamp", -1)
    return list(cursor)

async def get_weak_topics(student_id: str, min_attempts: int = 3):
    """
    Identify topics where the student has low success rate.
    """
    pipeline = [
        {"$match": {"student_id": student_id}},
        {"$group": {
            "_id": "$topic",
            "total_attempts": {"$sum": 1},
            "correct_attempts": {"$sum": {"$cond": ["$correct", 1, 0]}}
        }},
        {"$match": {"total_attempts": {"$gte": min_attempts}}},
        {"$addFields": {"success_rate": {"$divide": ["$correct_attempts", "$total_attempts"]}}},
        {"$match": {"success_rate": {"$lt": 0.6}}},
        {"$sort": {"success_rate": 1}}
    ]
    cursor = collection.aggregate(pipeline)
    return [doc["_id"] for doc in cursor]