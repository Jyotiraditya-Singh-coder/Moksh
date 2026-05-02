FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Assume model is built during image build (or mounted)
RUN python train.py  # or download pre-trained
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8006"]