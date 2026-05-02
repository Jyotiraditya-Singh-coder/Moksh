import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Use same multilingual model
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

jobs = [
    {"title": "Data Scientist", "skills": ["python", "sql", "machine learning", "statistics"]},
    {"title": "Web Developer", "skills": ["javascript", "html", "css", "react"]},
    {"title": "DevOps Engineer", "skills": ["aws", "docker", "kubernetes", "linux"]},
    {"title": "Product Manager", "skills": ["agile", "scrum", "market research", "communication"]},
    {"title": "Machine Learning Engineer", "skills": ["python", "tensorflow", "pytorch", "mlops"]},
]
embeddings = model.encode([job['title'] for job in jobs])
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)
faiss.write_index(index, "job_index.faiss")
with open("job_metadata.pkl", "wb") as f:
    pickle.dump(jobs, f)