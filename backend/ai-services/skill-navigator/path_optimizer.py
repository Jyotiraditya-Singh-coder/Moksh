# ai-services/skill-navigator/path_optimizer.py
import os
import json
from groq import Groq
from skill_graph import SkillGraph
from learner_profiler import LearnerProfiler
from knowledge_tracer import KnowledgeTracer

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

class PathOptimizer:
    def __init__(self):
        self.skill_graph = SkillGraph()
        self.profiler = LearnerProfiler()
        self.kt = KnowledgeTracer()

    def generate_optimal_path(self, student_id: str, learner_profile: dict, target_role: str = None):
        """
        Generate optimal learning path using LLM + knowledge tracing.
        """
        weak_skills = [s for s, m in learner_profile['skill_mastery'].items() if m < 0.4]
        strong_skills = [s for s, m in learner_profile['skill_mastery'].items() if m > 0.7]

        # Include target role skills if provided
        target_skills = []
        if target_role:
            # In real implementation, fetch from career aligner
            target_skills = self._get_skills_for_role(target_role)

        # Build prompt
        prompt = f"""
You are an expert learning path optimizer. Based on the student's profile, generate a personalized learning path.

Student profile:
- Weak skills: {', '.join(weak_skills) if weak_skills else 'None identified'}
- Strong skills: {', '.join(strong_skills) if strong_skills else 'None'}
- Dominant reasoning strategy: {learner_profile.get('dominant_reasoning_strategy', 'unknown')}
- Average time per problem: {learner_profile.get('avg_time_per_problem', 0):.1f} seconds
- Hint dependency: {learner_profile.get('hint_dependency', 0):.2f} hints per problem
{'- Target role skills: ' + ', '.join(target_skills) if target_skills else ''}

The skill graph has prerequisites: e.g., algebra → calculus, arrays → trees, etc.

Design a sequence of 5-8 skills to focus on, in optimal order, to strengthen weak areas while building toward the target role (if any). For each skill, suggest:
- skill_id
- reason (why this skill at this point)
- estimated time to master (hours)
- recommended problem types or resources

Return a JSON object with:
- path (list of skill steps, each with skill_id, reason, estimated_hours, resources)
- total_estimated_hours
- explanation (why this path is optimal for this student)
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
            # Fallback: simple prerequisite-based path
            path = []
            hours = 0
            for skill in weak_skills[:5]:
                path.append({
                    "skill_id": skill,
                    "reason": f"Weak area identified from your history.",
                    "estimated_hours": 3,
                    "resources": ["Practice problems", "Video tutorials"]
                })
                hours += 3
            return {
                "path": path,
                "total_estimated_hours": hours,
                "explanation": "Fallback path based on weak skills."
            }

    def _get_skills_for_role(self, role: str) -> list:
        # Placeholder: in real implementation, query career aligner
        role_skills = {
            "data scientist": ["python_basics", "statistics", "ml_basics", "probability", "linear_algebra"],
            "software engineer": ["python_basics", "data_structures", "algorithms", "arrays", "trees"],
            "machine learning engineer": ["python_basics", "ml_basics", "deep_learning", "linear_algebra", "probability"]
        }
        return role_skills.get(role.lower(), [])