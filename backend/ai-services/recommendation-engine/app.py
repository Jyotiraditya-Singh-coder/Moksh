from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import joblib
import mlflow
import os
import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise import accuracy
import logging
import tempfile
from typing import List

app = FastAPI(title="Recommendation Engine")

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

model = None
student_factors = None
item_factors = None

def load_model():
    global model, student_factors, item_factors
    client = mlflow.tracking.MlflowClient()
    versions = client.get_latest_versions("recommendation_model", stages=["Production"])
    if versions:
        model_uri = f"models:/recommendation_model/Production"
        model = mlflow.pyfunc.load_model(model_uri)
        local_path = mlflow.artifacts.download_artifacts(run_id=versions[0].run_id, artifact_path="factors")
        student_factors = joblib.load(os.path.join(local_path, "student_factors.pkl"))
        item_factors = joblib.load(os.path.join(local_path, "item_factors.pkl"))
    else:
        model = joblib.load("svd_model.pkl")
        student_factors = joblib.load("student_factors.pkl")
        item_factors = joblib.load("item_factors.pkl")
load_model()

class RecommendRequest(BaseModel):
    student_id: str
    n_recommendations: int = 5

class RecommendResponse(BaseModel):
    question_ids: list[str]

class TrainRequest(BaseModel):
    data_source: str = "mongodb"

class Interaction(BaseModel):
    student_id: str
    question_id: str
    rating: float  # 1-5

class FineTuneData(BaseModel):
    interactions: List[Interaction]

@app.post("/recommend-question", response_model=RecommendResponse)
async def recommend(req: RecommendRequest):
    try:
        return {"question_ids": ["q1", "q2", "q3"]}
    except Exception as e:
        logging.error(e)
        raise HTTPException(500, detail=str(e))

@app.post("/train")
async def train(req: TrainRequest):
    try:
        df = pd.read_csv("interactions.csv")
        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(df[['student_id', 'question_id', 'rating']], reader)
        trainset, testset = train_test_split(data, test_size=0.2)
        model_svd = SVD(n_factors=50, random_state=42)
        model_svd.fit(trainset)
        predictions = model_svd.test(testset)
        rmse = accuracy.rmse(predictions, verbose=False)
        student_inner_to_raw = {inner: raw for raw, inner in trainset._raw2inner_id_items.items()}
        item_inner_to_raw = {inner: raw for raw, inner in trainset._raw2inner_id_items.items()}
        with mlflow.start_run() as run:
            mlflow.log_param("n_factors", 50)
            mlflow.log_metric("rmse", rmse)
            mlflow.sklearn.log_model(model_svd, "model")
            with tempfile.TemporaryDirectory() as tmpdir:
                joblib.dump(student_inner_to_raw, os.path.join(tmpdir, "student_factors.pkl"))
                joblib.dump(item_inner_to_raw, os.path.join(tmpdir, "item_factors.pkl"))
                mlflow.log_artifacts(tmpdir, artifact_path="factors")
            run_id = run.info.run_id
            model_uri = f"runs:/{run_id}/model"
            result = mlflow.register_model(model_uri, "recommendation_model")
            version = result.version
        client = mlflow.tracking.MlflowClient()
        client.transition_model_version_stage(
            name="recommendation_model",
            version=version,
            stage="Production"
        )
        load_model()
        return {"message": "Training completed", "version": version, "rmse": rmse}
    except Exception as e:
        logging.error(e)
        raise HTTPException(500, detail=str(e))

# NEW: Fine-tune endpoint
@app.post("/fine-tune")
async def fine_tune(data: FineTuneData):
    try:
        df = pd.DataFrame([i.dict() for i in data.interactions])
        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(df[['student_id', 'question_id', 'rating']], reader)
        trainset, testset = train_test_split(data, test_size=0.2)
        model_svd = SVD(n_factors=50, random_state=42)
        model_svd.fit(trainset)
        predictions = model_svd.test(testset)
        rmse = accuracy.rmse(predictions, verbose=False)
        student_inner_to_raw = {inner: raw for raw, inner in trainset._raw2inner_id_items.items()}
        item_inner_to_raw = {inner: raw for raw, inner in trainset._raw2inner_id_items.items()}
        with mlflow.start_run() as run:
            mlflow.log_param("n_factors", 50)
            mlflow.log_metric("rmse", rmse)
            mlflow.sklearn.log_model(model_svd, "model")
            with tempfile.TemporaryDirectory() as tmpdir:
                joblib.dump(student_inner_to_raw, os.path.join(tmpdir, "student_factors.pkl"))
                joblib.dump(item_inner_to_raw, os.path.join(tmpdir, "item_factors.pkl"))
                mlflow.log_artifacts(tmpdir, artifact_path="factors")
            run_id = run.info.run_id
            model_uri = f"runs:/{run_id}/model"
            result = mlflow.register_model(model_uri, "recommendation_model")
            version = result.version
        client = mlflow.tracking.MlflowClient()
        client.transition_model_version_stage(
            name="recommendation_model",
            version=version,
            stage="Production"
        )
        load_model()
        return {"message": "Fine-tuning completed", "version": version, "rmse": rmse}
    except Exception as e:
        logging.error(e)
        raise HTTPException(500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}