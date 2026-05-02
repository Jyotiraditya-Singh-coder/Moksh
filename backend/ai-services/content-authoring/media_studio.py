from gtts import gTTS
import os
import base64

def text_to_speech(text: str, lang: str = "en") -> str:
    """Generate speech and return base64 audio"""
    tts = gTTS(text=text, lang=lang)
    tts.save("temp.mp3")
    with open("temp.mp3", "rb") as f:
        audio_b64 = base64.b64encode(f.read()).decode()
    os.remove("temp.mp3")
    return audio_b64

# Optional: image generation using Hugging Face's free inference API
def generate_image(prompt: str) -> bytes:
    import requests
    API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    headers = {"Authorization": f"Bearer {os.environ.get('HF_TOKEN')}"}
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    return response.content  # raw image bytes
