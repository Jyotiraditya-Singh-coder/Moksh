from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from tutor import process_audio
import logging

app = FastAPI()

@app.post("/ask")
async def ask(audio: UploadFile = File(...), language: str = Form("en")):
    try:
        audio_bytes = await audio.read()
        answer = process_audio(audio_bytes, language)
        return {"answer": answer}
    except Exception as e:
        logging.error(e)
        raise HTTPException(500, detail=str(e))