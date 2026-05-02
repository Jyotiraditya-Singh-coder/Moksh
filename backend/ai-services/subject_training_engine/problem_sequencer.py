# ai-services/subject_training_engine/problem_sequencer.py
import os
import json
from groq import Groq
from knowledge_base import compute_student_weakness_profile, search_similar_approaches

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def generate_personalized_sequence(student_id: str, subject: str, available_hours: float) -> dict:
    """
    Generate a custom problem sequence based on the student's weakness profile.
    Returns a list of recommended problems with topics and estimated time.
    """
    profile = compute_student_weakness_profile(student_id)
    weak_concepts = profile.get("weak_concepts", [])
    strong_concepts = profile.get("strong_concepts", [])

    if not weak_concepts:
        # If no weaknesses identified, generate general practice
        weak_concepts = ["general"]

    # Retrieve similar successful approaches for each weak concept to guide sequencing
    examples = []
    for concept in weak_concepts[:3]:  # limit to top 3
        similar = search_similar_approaches(concept, top_k=2, topic_filter=subject)
        examples.extend(similar)

    prompt = f"""
You are an expert tutor designing a personalized problem sequence for a student.

Student's weak conceptual areas: {', '.join(weak_concepts)}
Student's strong conceptual areas: {', '.join(strong_concepts)}
Subject: {subject}
Available study time: {available_hours} hours

Here are some examples of successful approaches for similar concepts:
{json.dumps(examples, indent=2) if examples else 'None'}

Design a sequence of 3-5 problems that progressively build the student's skills in their weak areas.
For each problem, specify:
- topic (the main concept it targets)
- estimated time to solve (in minutes)
- a brief description of the problem
- which weak concept it addresses

Return a JSON object with keys:
- sequence (list of problems, each with: topic, estimated_minutes, description, targeted_concept)
- total_time (sum of estimated minutes)
- explanation (why this sequence is effective for this student)
"""

    try:
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            response_format={"type": "json_object"}
        )
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        # Fallback sequence
        return {
            "sequence": [
                {
                    "topic": weak_concepts[0] if weak_concepts else "general",
                    "estimated_minutes": 30,
                    "description": f"Practice problem on {weak_concepts[0] if weak_concepts else 'key concepts'}.",
                    "targeted_concept": weak_concepts[0] if weak_concepts else "general"
                }
            ],
            "total_time": 30,
            "explanation": "Fallback sequence due to error."
        }