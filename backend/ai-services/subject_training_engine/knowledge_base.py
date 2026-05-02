import faiss
import numpy as np
import pickle
import os
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
index = None
metadata = []  # each entry: { student_id, problem_id, analysis, topic, difficulty, concept_tags, correct, embedding_id }

INDEX_PATH = "knowledge_index.faiss"
META_PATH = "knowledge_meta.pkl"

def load_index():
    global index, metadata
    if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
        index = faiss.read_index(INDEX_PATH)
        with open(META_PATH, "rb") as f:
            metadata = pickle.load(f)
    else:
        dimension = 384
        index = faiss.IndexFlatL2(dimension)
        metadata = []

def save_index():
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump(metadata, f)

def update_knowledge_base(student_id: str, problem_id: str, analysis: dict, topic: str = None,
                          difficulty: str = None, correct: bool = False):
    load_index()
    text = f"{analysis.get('reasoning_strategy','')} {analysis.get('algorithm_pattern','')} {analysis.get('mathematical_pattern','')}"
    embedding = model.encode([text])[0].astype('float32')
    index.add(np.array([embedding]))
    metadata.append({
        "student_id": student_id,
        "problem_id": problem_id,
        "analysis": analysis,
        "topic": topic,
        "difficulty": difficulty,
        "correct": correct,
        "concept_tags": analysis.get('concept_tags', []),
        "embedding_id": index.ntotal - 1
    })
    save_index()

def search_similar_approaches(query_text: str, top_k: int = 5, topic_filter: str = None) -> list:
    load_index()
    if index.ntotal == 0:
        return []
    query_emb = model.encode([query_text])[0].astype('float32')
    distances, indices = index.search(np.array([query_emb]), top_k * 2)
    results = []
    for idx in indices[0]:
        if idx != -1 and idx < len(metadata):
            entry = metadata[idx]
            if topic_filter and entry.get("topic") != topic_filter:
                continue
            results.append(entry)
            if len(results) >= top_k:
                break
    return results

def get_student_history(student_id: str) -> list:
    load_index()
    return [entry for entry in metadata if entry.get("student_id") == student_id]

def compute_student_weakness_profile(student_id: str) -> dict:
    history = get_student_history(student_id)
    if not history:
        return {"weak_concepts": [], "strong_concepts": [], "concept_stats": {}}
    from collections import defaultdict
    concept_correct = defaultdict(int)
    concept_total = defaultdict(int)
    for entry in history:
        tags = entry.get("concept_tags", [])
        correct = entry.get("correct", False)
        for tag in tags:
            concept_total[tag] += 1
            if correct:
                concept_correct[tag] += 1
    weakness = []
    strength = []
    stats = {}
    for tag, total in concept_total.items():
        correct_count = concept_correct.get(tag, 0)
        ratio = correct_count / total if total > 0 else 0
        stats[tag] = {"total": total, "correct": correct_count, "ratio": ratio}
        if ratio < 0.4:
            weakness.append(tag)
        elif ratio > 0.8:
            strength.append(tag)
    return {
        "weak_concepts": weakness,
        "strong_concepts": strength,
        "concept_stats": stats
    }

def rebuild_index():
    """Rebuild FAISS index from metadata (if metadata exists)."""
    global index, metadata
    if not metadata:
        return
    texts = []
    for entry in metadata:
        analysis = entry['analysis']
        text = f"{analysis.get('reasoning_strategy','')} {analysis.get('algorithm_pattern','')} {analysis.get('mathematical_pattern','')}"
        texts.append(text)
    embeddings = model.encode(texts).astype('float32')
    index = faiss.IndexFlatL2(384)
    index.add(embeddings)
    # Update embedding_id in metadata (optional)
    for i, entry in enumerate(metadata):
        entry['embedding_id'] = i
    save_index()