# ai-services/skill-navigator/learner_profiler.py
import numpy as np
from typing import Dict, List
from skill_graph import SkillGraph

class LearnerProfiler:
    def __init__(self):
        self.skill_graph = SkillGraph()

    def create_profile(self, student_id: str, interaction_history: List[Dict]) -> Dict:
        """
        Create a multi-dimensional learner profile from interaction history.
        Each interaction: {skill_id, correct, time_spent, hints_used, solution_text, etc.}
        """
        # Skill mastery estimates (simple average for demo)
        skill_mastery = {}
        for skill_id, _ in self.skill_graph.get_all_skills():
            relevant = [i for i in interaction_history if i.get('skill_id') == skill_id]
            if relevant:
                correct_count = sum(1 for r in relevant if r.get('correct', False))
                mastery = correct_count / len(relevant) if relevant else 0
            else:
                mastery = 0  # unknown
            skill_mastery[skill_id] = mastery

        # Learning pace (average time per problem)
        avg_time = np.mean([i.get('time_spent', 0) for i in interaction_history]) if interaction_history else 0

        # Hint dependency
        hints_used = np.mean([i.get('hints_used', 0) for i in interaction_history]) if interaction_history else 0

        # Conceptual strengths/weaknesses (from concept tags)
        concept_stats = {}
        for i in interaction_history:
            for tag in i.get('concept_tags', []):
                concept_stats[tag] = concept_stats.get(tag, 0) + (1 if i.get('correct') else -1)

        # Cognitive style (simplified: based on reasoning strategy frequency)
        strategies = [i.get('reasoning_strategy', 'unknown') for i in interaction_history if i.get('reasoning_strategy')]
        strategy_counts = {}
        for s in strategies:
            strategy_counts[s] = strategy_counts.get(s, 0) + 1
        dominant_strategy = max(strategy_counts, key=strategy_counts.get) if strategy_counts else 'unknown'

        return {
            "student_id": student_id,
            "skill_mastery": skill_mastery,
            "avg_time_per_problem": avg_time,
            "hint_dependency": hints_used,
            "concept_strengths": [k for k, v in concept_stats.items() if v > 0],
            "concept_weaknesses": [k for k, v in concept_stats.items() if v < 0],
            "dominant_reasoning_strategy": dominant_strategy,
            "total_interactions": len(interaction_history)
        }