from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from rag_engine import generate_rag_response

app = FastAPI(title="RAG MySQL Groq Service")

class RagRequest(BaseModel):
    query: str

@app.post("/api/rag/ask")
async def ask_rag(request: RagRequest):
    try:
        response = generate_rag_response(request.query)
        return {"answer": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8013)
