import faiss
import numpy as np
import pickle
import os
from sentence_transformers import SentenceTransformer

class SkillTaxonomyExtractor:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.skills = {}  # id -> description
        self._load_or_init()

    def _load_or_init(self):
        if os.path.exists("skill_index.faiss") and os.path.exists("skills.pkl"):
            self.index = faiss.read_index("skill_index.faiss")
            with open("skills.pkl", "rb") as f:
                self.skills = pickle.load(f)
        else:
            self.skills = {
                "math.algebra.equations": "Solving linear and quadratic equations",
                "math.calculus.derivatives": "Computing derivatives using rules",
                "cs.dp.memoization": "Optimizing recursive solutions with memoization",
                "cs.graphs.bfs": "Breadth-first search traversal",
                "ml.supervised.classification": "Supervised learning for classification",
            }
            embeddings = self.model.encode(list(self.skills.values()))
            self.index = faiss.IndexFlatL2(embeddings.shape[1])
            self.index.add(embeddings)
            self._save()

    def _save(self):
        faiss.write_index(self.index, "skill_index.faiss")
        with open("skills.pkl", "wb") as f:
            pickle.dump(self.skills, f)

    def extract_skills(self, text: str, top_k: int = 5):
        emb = self.model.encode([text])
        distances, indices = self.index.search(emb, top_k)
        skill_ids = list(self.skills.keys())
        results = []
        for i, idx in enumerate(indices[0]):
            results.append({
                "skill_id": skill_ids[idx],
                "description": self.skills[skill_ids[idx]],
                "similarity": float(1 - distances[0][i])
            })
        return results

    def add_custom_skill(self, skill_id: str, description: str):
        """Add a new skill to the taxonomy and update the index."""
        self.skills[skill_id] = description
        embeddings = self.model.encode(list(self.skills.values()))
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)
        self._save()