# ai-services/subject_training_engine/algorithm_analyzer.py
import os
import json
from groq import Groq
from math_validator import compare_algorithms_output  # new import

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def analyze_algorithm(code: str, problem_description: str) -> dict:
    prompt = f"""
You are an algorithm expert. Analyze the following code for the given problem.

Problem: {problem_description}
Code:
{code}

Provide:
- Time complexity (Big O)
- Space complexity (Big O)
- Algorithm type (e.g., brute force, dynamic programming, greedy, divide and conquer, backtracking)
- Optimization suggestions (list)

Return JSON with keys:
- time_complexity
- space_complexity
- algorithm_type
- optimization_suggestions (list of strings)
"""
    try:
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        return {
            "time_complexity": "Unknown",
            "space_complexity": "Unknown",
            "algorithm_type": "Unknown",
            "optimization_suggestions": ["Unable to analyze due to error."]
        }

# New function to compare two algorithms numerically (if they produce numerical output)
def compare_algorithms(expr1: str, expr2: str, precision: int = 100):
    """
    Compare two algorithms by evaluating their expressions with mpmath.
    Returns detailed comparison.
    """
    return compare_algorithms_output(expr1, expr2, precision)