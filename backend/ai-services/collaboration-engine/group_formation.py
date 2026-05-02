import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx

model = SentenceTransformer('all-MiniLM-L6-v2')

def form_study_groups(students: list, group_size: int = 3):
    """
    students: list of dicts with 'id' and 'skills' (list of skill embeddings)
    Uses complementary skill matching.
    """
    # Create skill vectors
    student_ids = [s['id'] for s in students]
    skill_vectors = np.array([s['skills'] for s in students])  # assume already embedded

    # Compute pairwise skill complementarity (inverse similarity)
    sim = cosine_similarity(skill_vectors)
    complement = 1 - sim  # high value means different skills

    # Build graph with complementarity weights
    G = nx.Graph()
    for i, sid in enumerate(student_ids):
        G.add_node(sid)
    for i in range(len(students)):
        for j in range(i+1, len(students)):
            G.add_edge(student_ids[i], student_ids[j], weight=complement[i][j])

    # Use community detection to form groups (e.g., greedy modularity)
    from networkx.algorithms.community import greedy_modularity_communities
    communities = list(greedy_modularity_communities(G, weight='weight'))
    groups = [list(c) for c in communities]

    # Ensure groups are of desired size (merge if needed)
    # (simplified: return as is)
    return groups