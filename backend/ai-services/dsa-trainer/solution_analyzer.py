# ai-services/dsa-trainer/solution_analyzer.py

import os
import json
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

async def analyze_solution(problem: dict, code: str, language: str = "python"):
    """
    Analyze a submitted solution using Groq LLM.
    Returns structured JSON feedback.
    """

    prompt = f"""
You are an expert FAANG DSA interviewer.

Analyze the student's solution to the following problem.

PROBLEM:
{json.dumps(problem, indent=2)}

STUDENT CODE ({language}):

{code}

Perform the analysis below.

1. Correctness
2. Time Complexity
3. Space Complexity
4. Edge Cases missed
5. Code Quality
6. Optimality of approach
7. Improved Solution
8. Learning feedback for the student

Return STRICTLY in JSON format:

{{
 "correctness": "",
 "time_complexity": "",
 "space_complexity": "",
 "edge_cases": [],
 "code_quality": "",
 "optimality": "",
 "improved_solution": "",
 "learning_feedback": ""
}}

Do not include anything outside JSON.
"""

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            temperature=0.2,
            max_tokens=1200,
            messages=[
                {
                    "role": "system",
                    "content": "You are an elite data structures and algorithms interviewer."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        content = response.choices[0].message.content

        # Safely parse JSON
        try:
            result = json.loads(content)
        except json.JSONDecodeError:
            result = {
                "error": "LLM returned invalid JSON",
                "raw_output": content
            }

        return result

    except Exception as e:
        return {"error": str(e)}