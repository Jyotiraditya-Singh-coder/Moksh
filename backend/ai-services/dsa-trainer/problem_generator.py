import os
import json
from groq import Groq
from dsa_topics import get_topic_info

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

async def generate_problem(topic: str, difficulty: str, student_weaknesses: list = None):
    """
    Generate a DSA problem using Groq API.
    """
    topic_info = get_topic_info(topic)
    topic_name = topic_info.get("name", topic)
    
    prompt = f"""
You are an expert DSA tutor. Generate a {difficulty} difficulty problem on the topic "{topic_name}".

Student's weak areas: {', '.join(student_weaknesses) if student_weaknesses else 'None'}

The problem should be original and suitable for coding practice. Include:
1. Problem statement
2. Input format
3. Output format
4. Constraints
5. Sample input/output (2 examples)
6. Hints (2-3)
7. Time complexity expectation
8. Space complexity expectation

Return the response as a JSON object with the following keys:
- problem_statement
- input_format
- output_format
- constraints
- sample_inputs (list of strings)
- sample_outputs (list of strings)
- hints (list of strings)
- expected_time_complexity
- expected_space_complexity
- topic
- difficulty
"""

    try:
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": "You are a helpful DSA tutor that outputs JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        problem = json.loads(content)
        return problem
    except Exception as e:
        # Fallback
        return {
            "problem_statement": f"Write a program to solve a {difficulty} {topic_name} problem.",
            "input_format": "First line contains an integer n...",
            "output_format": "Print the result...",
            "constraints": "1 ≤ n ≤ 10^5",
            "sample_inputs": ["5\n2 3 1 5 4"],
            "sample_outputs": ["3"],
            "hints": ["Think about using two pointers.", "Consider sorting first."],
            "expected_time_complexity": "O(n log n)",
            "expected_space_complexity": "O(1)",
            "topic": topic,
            "difficulty": difficulty
        }