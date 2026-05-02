# ai-services/skill-navigator/skill_graph.py
import networkx as nx
import json

class SkillGraph:
    """Simple skill graph with prerequisites and relationships."""
    def __init__(self):
        self.graph = nx.DiGraph()
        self._build_graph()

    def _build_graph(self):
        # Define skills and their relationships
        skills = [
            # Math foundations
            ("algebra", {"name": "Algebra", "category": "math", "difficulty": 1}),
            ("calculus", {"name": "Calculus", "category": "math", "difficulty": 3}),
            ("linear_algebra", {"name": "Linear Algebra", "category": "math", "difficulty": 3}),
            ("probability", {"name": "Probability", "category": "math", "difficulty": 2}),
            ("statistics", {"name": "Statistics", "category": "math", "difficulty": 3}),

            # Programming basics
            ("python_basics", {"name": "Python Basics", "category": "programming", "difficulty": 1}),
            ("data_structures", {"name": "Data Structures", "category": "programming", "difficulty": 2}),
            ("algorithms", {"name": "Algorithms", "category": "programming", "difficulty": 3}),

            # DSA
            ("arrays", {"name": "Arrays", "category": "dsa", "difficulty": 1}),
            ("linked_lists", {"name": "Linked Lists", "category": "dsa", "difficulty": 2}),
            ("trees", {"name": "Trees", "category": "dsa", "difficulty": 3}),
            ("graphs", {"name": "Graphs", "category": "dsa", "difficulty": 4}),
            ("dynamic_programming", {"name": "Dynamic Programming", "category": "dsa", "difficulty": 5}),

            # Machine learning
            ("ml_basics", {"name": "ML Basics", "category": "ml", "difficulty": 3}),
            ("deep_learning", {"name": "Deep Learning", "category": "ml", "difficulty": 5}),
        ]

        for skill_id, attrs in skills:
            self.graph.add_node(skill_id, **attrs)

        # Add prerequisite edges
        edges = [
            ("algebra", "calculus"),
            ("algebra", "linear_algebra"),
            ("calculus", "probability"),
            ("probability", "statistics"),
            ("python_basics", "data_structures"),
            ("data_structures", "algorithms"),
            ("arrays", "linked_lists"),
            ("linked_lists", "trees"),
            ("trees", "graphs"),
            ("graphs", "dynamic_programming"),
            ("python_basics", "ml_basics"),
            ("linear_algebra", "ml_basics"),
            ("probability", "ml_basics"),
            ("ml_basics", "deep_learning"),
        ]
        for u, v in edges:
            self.graph.add_edge(u, v)

    def get_prerequisites(self, skill_id):
        """Return list of prerequisite skill IDs."""
        return list(self.graph.predecessors(skill_id))

    def get_related_skills(self, skill_id, depth=1):
        """Get skills within depth steps."""
        related = set()
        for node in self.graph.nodes:
            try:
                if nx.shortest_path_length(self.graph, skill_id, node) <= depth:
                    related.add(node)
            except nx.NetworkXNoPath:
                continue
        return list(related)

    def get_all_skills(self):
        return list(self.graph.nodes(data=True))