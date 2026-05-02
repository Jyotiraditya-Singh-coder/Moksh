# ai-services/quant-mentor/mentor.py
import os
import json
from groq import Groq
from knowledge_graph import QuantKnowledgeGraph

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
kg = QuantKnowledgeGraph()

def generate_quant_guide(user_background: dict) -> dict:
    """
    Generate personalized quant trading preparation guide.
    user_background: e.g., {"degree": "Computer Science", "year": 1, "known_topics": ["python", "algorithms"]}
    """
    known = user_background.get("known_topics", [])
    degree = user_background.get("degree", "Computer Science")
    year = user_background.get("year", 1)

    # Retrieve related topics from knowledge graph based on known topics
    recommendations = []
    for topic in known:
        related = kg.get_related(topic, depth=2)
        recommendations.extend(related)
    # Remove duplicates and known
    recommendations = list(set(recommendations) - set(known))
    # Limit to top 10
    recommendations = recommendations[:10]

    # Build prompt
    prompt = f"""
Act as an elite Quant Trading Career Mentor. Your goal is to provide a comprehensive, actionable preparation guide for a student looking to break into quantitative trading. Tailor your advice to be highly relevant for a {year}-year {degree} student, ensuring they leverage their foundational knowledge while building specialized skills.

The student already knows: {', '.join(known) if known else 'None'}.
Based on the knowledge graph, related topics to explore include: {', '.join(recommendations) if recommendations else 'None'}.

Structure your response using the following framework:

1. Core Skills to Master
Break down the required skills into specific, actionable areas:

- Mathematics & Statistics: Emphasize Probability (Bayes' Theorem, Expected Value, Markov Chains), Combinatorics, Linear Algebra, and Calculus.
- Programming Proficiency: Focus heavily on C++ for low-latency systems and Python for data analysis and modeling.
- Computer Science Fundamentals: Highlight the importance of Data Structures and Algorithms (DSA) and algorithmic time complexity.
- Mental Math: Stress the need for lightning-fast arithmetic without a calculator.
- Finance Knowledge: Explain that while deep finance knowledge is sometimes optional, understanding basics like market making, options, and order books gives a strong edge.

2. Amount of Preparation (The Timeline)
Provide a realistic timeline and daily routine:

- Long-Term Roadmap: Advise them to maintain a high GPA, participate in hackathons, and seek software engineering or research internships early on.
- Interview Prep Phase: Recommend a dedicated 3 to 4-month intense preparation cycle prior to interviews.
- Daily Routine: Suggest a daily breakdown (e.g., 15 minutes of mental math, 1–2 hours of Leetcode/DSA practice, and 1 hour of probability/brainteasers).

3. Types of Interview Questions to Prepare For
Categorize the questions they will face and provide one specific example for each:

- Brainteasers & Logic Puzzles: Questions testing lateral thinking under pressure (e.g., "100 pirates are dividing gold...").
- Probability & Expected Value: Heavy focus on dice, cards, and coin flip scenarios (e.g., "What is the expected value of rolling a die and either taking the payout or rolling again?").
- Coding & DSA: Standard algorithmic challenges focusing on optimized C++ or Python code (e.g., "Design a data structure with O(1) push and random pop").
- Mental Math Drills: Rapid-fire arithmetic (e.g., "What is 43 x 57?").
- Behavioral & Market Awareness: Questions assessing how they handle risk, failure, and teamwork.

Maintain an encouraging but candid tone. Remind the user that consistency is key and that struggling with mock interviews initially is a normal part of the learning process.

Return a JSON object with keys:
- core_skills (object with subkeys: mathematics, programming, cs_fundamentals, mental_math, finance_knowledge)
- timeline (object with subkeys: long_term_roadmap, interview_prep_phase, daily_routine)
- interview_questions (object with categories as keys and examples as values)
- recommended_topics (list of topic IDs from the knowledge graph to focus on)
- explanation (string summarizing why this path fits the student)
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
        # Fallback
        return {
            "core_skills": {
                "mathematics": "Probability, Statistics, Linear Algebra, Calculus",
                "programming": "Python, C++",
                "cs_fundamentals": "Data Structures, Algorithms, Time Complexity",
                "mental_math": "Rapid arithmetic",
                "finance_knowledge": "Market making, options, order books"
            },
            "timeline": {
                "long_term_roadmap": "Maintain high GPA, internships, hackathons",
                "interview_prep_phase": "3-4 months intense prep",
                "daily_routine": "15 min mental math, 1-2 hours Leetcode, 1 hour probability"
            },
            "interview_questions": {
                "brainteasers": "100 pirates dividing gold",
                "probability": "Expected value of die roll with option to reroll",
                "coding": "Design data structure with O(1) push and random pop",
                "mental_math": "43 x 57",
                "behavioral": "Tell me about a time you failed"
            },
            "recommended_topics": recommendations[:5],
            "explanation": "Fallback guide due to error."
        }