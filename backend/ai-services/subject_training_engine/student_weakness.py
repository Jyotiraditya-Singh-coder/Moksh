# ai-services/subject_training_engine/student_weakness.py
from knowledge_base import compute_student_weakness_profile

def get_weakness_profile(student_id: str) -> dict:
    """
    Public interface to get a student's weakness profile.
    """
    return compute_student_weakness_profile(student_id)