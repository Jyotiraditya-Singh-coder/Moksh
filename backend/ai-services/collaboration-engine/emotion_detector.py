# Use a free speech emotion model from Hugging Face
import requests
import os
import base64

def detect_emotion(audio_base64: str) -> str:
    # Example using a free inference API (e.g., wav2vec2 emotion)
    API_URL = "https://api-inference.huggingface.co/models/harshit345/xlsr-wav2vec-speech-emotion-recognition"
    headers = {"Authorization": f"Bearer {os.environ.get('HF_TOKEN')}"}
    audio_bytes = base64.b64decode(audio_base64)
    response = requests.post(API_URL, headers=headers, data=audio_bytes)
    return response.json()  # returns emotion label