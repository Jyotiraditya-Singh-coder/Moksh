import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import pickle
import os
import logging

# Use multilingual model
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
index = None
job_metadata = None
INDEX_PATH = "job_index.faiss"
META_PATH = "job_metadata.pkl"

def load_index():
    global index, job_metadata
    if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
        index = faiss.read_index(INDEX_PATH)
        with open(META_PATH, "rb") as f:
            job_metadata = pickle.load(f)
    else:
        index = None
        job_metadata = []

def save_index():
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump(job_metadata, f)

# Load at module import
load_index()

def extract_skills(text):
    """
    Extract skills from resume text.
    In production, replace with a proper NER library (e.g., spaCy, transformers).
    """
    # Dummy implementation – returns a fixed set of skills
    return ["python", "sql", "communication", "machine learning", "aws"]

def analyze(resume_text, target_role):
    """
    Original analysis function: compare resume skills with job requirements.
    """
    if index is None or index.ntotal == 0:
        return {"missingSkills": [], "roadmap": []}
    
    resume_skills = extract_skills(resume_text)
    query_emb = model.encode([target_role])
    distances, indices = index.search(query_emb, k=5)
    
    required_skills = set()
    for idx in indices[0]:
        if idx != -1 and idx < len(job_metadata):
            required_skills.update(job_metadata[idx].get('skills', []))
    
    missing = list(required_skills - set(resume_skills))
    roadmap = [
        {
            "skill": s,
            "resources": ["Coursera course", "book", "online tutorial"],
            "estimatedHours": 10
        }
        for s in missing
    ]
    return {"missingSkills": missing, "roadmap": roadmap}

def add_job_role(job_title: str, skills: list):
    """
    Add a new job role to the database.
    Updates both metadata and FAISS index.
    """
    global index, job_metadata
    if index is None:
        # Initialize index if not present
        dimension = model.get_sentence_embedding_dimension()
        index = faiss.IndexFlatL2(dimension)
        job_metadata = []
    
    # Create embedding for job title
    emb = model.encode([job_title])[0].astype('float32')
    index.add(np.array([emb]))
    job_metadata.append({"title": job_title, "skills": skills})
    save_index()

def rebuild_index_from_metadata():
    """
    Rebuild the FAISS index from current job_metadata.
    Useful after many additions or if index gets corrupted.
    """
    global index
    if not job_metadata:
        return
    titles = [job["title"] for job in job_metadata]
    embeddings = model.encode(titles).astype('float32')
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    save_index()

def get_all_job_roles():
    """Return all stored job roles with their skills."""
    return [{"title": job["title"], "skills": job["skills"]} for job in job_metadata]