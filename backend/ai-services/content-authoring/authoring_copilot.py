import os
import json
from groq import Groq
from taxonomy_extractor import SkillTaxonomyExtractor

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
taxonomy = SkillTaxonomyExtractor()

def generate_lesson(prompt: str, subject: str, grade: str) -> dict:
    system_prompt = f"""
You are an expert curriculum designer. Create a detailed lesson on: {prompt}
Subject: {subject}
Grade level: {grade}

Output JSON with:
- title: str
- learning_objectives: list[str]
- key_concepts: list[str]
- content: list[{{"heading": str, "body": str}}]
- examples: list[{{"question": str, "solution": str, "explanation": str}}]
- practice: list[{{"difficulty": str, "question": str, "answer": str}}]
- assessment: list[dict]
- extensions: list[str]
"""
    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role": "user", "content": system_prompt}],
        temperature=0.7,
        response_format={"type": "json_object"}
    )
    lesson = json.loads(response.choices[0].message.content)
    # Extract skills from content
    full_text = json.dumps(lesson)
    skills = taxonomy.extract_skills(full_text)
    lesson["skills"] = skills
    return lesson