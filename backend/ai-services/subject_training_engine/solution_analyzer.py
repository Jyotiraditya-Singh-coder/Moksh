# ai-services/subject_training_engine/solution_analyzer.py
import os
import json
from groq import Groq
from knowledge_base import get_similar_patterns

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def analyze_solution(data: dict) -> dict:
    """
    Analyze a student's solution and extract reasoning strategy,
    concept tags, mistakes, etc.
    """
    student_id = data['student_id']
    problem_id = data['problem_id']
    solution_text = data['solution_text']
    code = data.get('code')
    topic = data.get('topic', 'unknown')
    difficulty = data.get('difficulty', 'medium')
    correct = data.get('correct', False)  # whether the solution is correct

    # Retrieve similar past approaches to guide analysis
    similar = get_similar_patterns(solution_text, top_k=3)

    prompt = f"""
You are an expert tutor analyzing a student's solution to a {difficulty} {topic} problem.

Student's solution: {solution_text}
{'Code: ' + code if code else ''}
Was the solution correct? {correct}

Similar past patterns: {similar if similar else 'None'}

Analyze the solution and extract:
- Reasoning strategy (e.g., brute force, divide and conquer, induction, greedy, DP)
- Algorithm pattern (if applicable: DP, greedy, backtracking, graph traversal, etc.)
- Mathematical pattern (if applicable: number theory, combinatorics, algebra, calculus)
- Common mistakes observed (list)
- Time complexity (if code provided)
- Suggested improvement (how to optimize or correct)

Additionally, identify **specific conceptual tags** that describe what the student demonstrated or struggled with.
Use tags from this list (or create new ones if needed):
- dp-state-definition, dp-transition, dp-memoization, dp-tabulation
- graph-traversal-choice (bfs vs dfs), graph-cycle-detection, graph-shortest-path
- recursion-base-case, recursion-tree, recursion-optimization
- greedy-choice-property, greedy-vs-dp
- sorting-choice, searching-algorithm
- time-complexity-analysis, space-complexity-analysis
- off-by-one-errors, index-errors, edge-cases
- mathematical-induction, proof-strategy, algebraic-manipulation
- numerical-precision, floating-point-errors
- divide-and-conquer-combine-step, conquer-step

Return a JSON object with keys:
- reasoning_strategy
- algorithm_pattern (string or null)
- mathematical_pattern (string or null)
- common_mistakes (list of strings)
- time_complexity (string or null)
- suggested_improvement (string or null)
- concept_tags (list of strings)
"""

    try:
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        result = json.loads(response.choices[0].message.content)
        # Ensure all keys exist
        defaults = {
            "reasoning_strategy": "unknown",
            "algorithm_pattern": None,
            "mathematical_pattern": None,
            "common_mistakes": [],
            "time_complexity": None,
            "suggested_improvement": None,
            "concept_tags": []
        }
        for k, v in defaults.items():
            if k not in result:
                result[k] = v
        return result
    except Exception as e:
        # Fallback
        return {
            "reasoning_strategy": "unknown",
            "algorithm_pattern": None,
            "mathematical_pattern": None,
            "common_mistakes": [],
            "time_complexity": None,
            "suggested_improvement": None,
            "concept_tags": []
        }