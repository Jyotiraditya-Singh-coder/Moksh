import os
import json
import random
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def generate_question(profile):
    weak = profile.get('weakTopics', [])
    strong = profile.get('strongTopics', [])
    lang = profile.get('preferredLanguage', 'en')
    
    # Introduce randomness by asking for a random sub-topic or specific angle
    random_angle = random.choice(["a real-world scenario", "a debugging scenario", "a theoretical concept", "a code optimization problem", "an edge-case analysis"])

    prompt = f\"\"\"
You are an AI tutor. Generate a unique and random challenging quiz question for a student.
Context:
- Weak topics: {', '.join(weak) if weak else 'None'}
- Strong topics: {', '.join(strong) if strong else 'None'}
- Preferred language (for the explanation): {lang}

Requirements:
1. Target ONE of the weak topics.
2. The question style should be based on {random_angle}.
3. The generation MUST be entirely unique each time.
4. Provide JSON exactly matching this structure:
{{
  "question": "The generated question text",
  "difficulty": "beginner/intermediate/advanced",
  "topic": "The exact topic chosen",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "correct_option_index": 0,
  "solution": "Approach 1 description",
  "alternateApproach": "Approach 2 description",
  "explanation": "Step-by-step detailed explanation",
  "learningTip": "One short learning tip"
}}
Respond ONLY with the raw JSON object.
\"\"\"

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9, # Higher temperature for more randomness
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Error generating question: {e}")
        # Fallback
        return {
            "question": "What is the time complexity of a hash map lookup?",
            "difficulty": "intermediate",
            "topic": "Data Structures",
            "options": ["O(1)", "O(n)", "O(log n)", "O(n^2)"],
            "correct_option_index": 0,
            "solution": "Hash maps use a hashing function to compute an index.",
            "alternateApproach": "Binary search trees take O(log n).",
            "explanation": "Because the hash function directly points to the memory location, lookup is normally O(1).",
            "learningTip": "Always consider hash maps when you need fast lookups."
        }
