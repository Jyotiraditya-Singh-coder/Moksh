# ai-services/skill-navigator/knowledge_tracer.py
import numpy as np
from sklearn.linear_model import LogisticRegression
import joblib
import os

class KnowledgeTracer:
    """
    Simple Bayesian Knowledge Tracing using logistic regression.
    For production, use Deep Knowledge Tracing or more sophisticated models.
    """
    def __init__(self):
        self.model = LogisticRegression()
        self.trained = False

    def train(self, X, y):
        """X: features (e.g., previous correctness, time, hint usage)"""
        self.model.fit(X, y)
        self.trained = True

    def predict_knowledge(self, features):
        """Return probability of knowing the skill."""
        if not self.trained:
            return 0.5  # default
        return self.model.predict_proba([features])[0][1]

    def save(self, path):
        joblib.dump(self.model, path)

    def load(self, path):
        if os.path.exists(path):
            self.model = joblib.load(path)
            self.trained = True