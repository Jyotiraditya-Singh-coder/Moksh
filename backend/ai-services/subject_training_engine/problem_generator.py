# ai-services/subject_training_engine/problem_generator.py
import os
import json
from groq import Groq
from knowledge_base import search_similar_approaches

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def generate_problem(params: dict) -> dict:
    subject = params['subject']
    topic = params['topic']
    difficulty = params['difficulty']
    weakness_profile = params.get('weakness_profile', [])
    previous_mistakes = params.get('previous_mistakes', [])

    # Retrieve similar approaches from knowledge base
    similar = search_similar_approaches(topic, top_k=3, topic_filter=topic)
    similar_text = ""
    if similar:
        similar_text = "Here are some successful approaches students used for similar problems:\n"
        for s in similar:
            strat = s['analysis'].get('reasoning_strategy', 'unknown')
            alg = s['analysis'].get('algorithm_pattern', '')
            math = s['analysis'].get('mathematical_pattern', '')
            similar_text += f"- {strat} {alg} {math}\n"

    prompt = f"""
You are an expert tutor in {subject}. Generate a {difficulty} difficulty problem on the topic: {topic}.

Student profile:
- Weak topics: {', '.join(weakness_profile) if weakness_profile else 'None'}
- Previous mistakes: {', '.join(previous_mistakes) if previous_mistakes else 'None'}

{similar_text}

The problem should target the student's weak areas. Provide:
1. Problem statement
2. A list of hints (2-3)
3. Detailed solution explanation
4. An alternative approach (if applicable)
5. Time complexity (if it's an algorithm problem)

Format your response as a JSON object with keys:
- problem_statement
- hints (list of strings)
- solution_explanation
- alternative_approach (string or null)
- time_complexity (string or null)
"""

    try:
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        result = json.loads(response.choices[0].message.content)
        required_keys = ["problem_statement", "hints", "solution_explanation", "alternative_approach", "time_complexity"]
        for key in required_keys:
            if key not in result:
                result[key] = None
        return result
    except Exception as e:
        # Fallback
        return {
            "problem_statement": f"Solve a {difficulty} {topic} problem.",
            "hints": ["Think step by step.", "Recall the definition."],
            "solution_explanation": "Here is a detailed solution.",
            "alternative_approach": None,
            "time_complexity": None
        }