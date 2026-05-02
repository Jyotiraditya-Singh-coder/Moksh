import whisper
import os
from groq import Groq

model = whisper.load_model("base")
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def process_audio(audio_bytes, language):
    with open("temp_audio.wav", "wb") as f:
        f.write(audio_bytes)
    result = model.transcribe("temp_audio.wav", language=language)
    text = result["text"]
    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {"role": "system", "content": "You are a helpful tutor. Explain concepts simply."},
            {"role": "user", "content": f"Explain this in {language}: {text}"}
        ]
    )
    answer = response.choices[0].message.content
    os.remove("temp_audio.wav")
    return answer