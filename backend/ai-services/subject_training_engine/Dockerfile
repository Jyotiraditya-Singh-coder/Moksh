FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create empty FAISS index on first run (will be overwritten if exists)
RUN python -c "from knowledge_base import load_index; load_index()"

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8008"]