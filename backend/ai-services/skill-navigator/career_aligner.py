# ai-services/skill-navigator/career_aligner.py
import json

class CareerAligner:
    def __init__(self):
        self.role_skills = {
            "data scientist": {
                "required": ["python_basics", "statistics", "ml_basics", "probability", "linear_algebra"],
                "preferred": ["deep_learning", "sql", "big_data"],
                "description": "Analyze and interpret complex data to help organizations make decisions."
            },
            "software engineer": {
                "required": ["python_basics", "data_structures", "algorithms", "arrays"],
                "preferred": ["trees", "graphs", "system_design"],
                "description": "Design, develop, and maintain software systems."
            },
            "machine learning engineer": {
                "required": ["python_basics", "ml_basics", "deep_learning", "linear_algebra", "probability"],
                "preferred": ["tensorflow", "pytorch", "mlops"],
                "description": "Build and deploy machine learning models."
            },
            "frontend developer": {
                "required": ["html_css", "javascript", "react"],
                "preferred": ["typescript", "web_performance"],
                "description": "Create user interfaces for web applications."
            },
            "backend developer": {
                "required": ["python_basics", "databases", "api_design"],
                "preferred": ["cloud_services", "microservices"],
                "description": "Build server-side logic and APIs."
            }
        }

    def get_role_skills(self, role: str) -> dict:
        """Return skill requirements for a role."""
        return self.role_skills.get(role.lower(), {})

    def analyze_readiness(self, learner_skills: dict, target_role: str) -> dict:
        """
        Compare learner's skill mastery with role requirements.
        learner_skills: dict {skill_id: mastery (0-1)}
        target_role: string
        Returns readiness score and gaps.
        """
        role_data = self.get_role_skills(target_role)
        if not role_data:
            return {"error": "Role not found"}

        required = role_data.get("required", [])
        preferred = role_data.get("preferred", [])

        # Compute readiness for required skills
        required_scores = []
        missing_required = []
        for skill in required:
            mastery = learner_skills.get(skill, 0)
            required_scores.append(mastery)
            if mastery < 0.6:
                missing_required.append(skill)

        # For preferred, just list missing
        missing_preferred = [s for s in preferred if learner_skills.get(s, 0) < 0.5]

        overall_readiness = sum(required_scores) / len(required_scores) if required_scores else 0

        return {
            "target_role": target_role,
            "readiness_score": overall_readiness,
            "missing_required": missing_required,
            "missing_preferred": missing_preferred,
            "has_required": [s for s in required if learner_skills.get(s, 0) >= 0.6]
        }