from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import joblib
import mlflow
import os
from model import DropoutPredictor
import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score

app = FastAPI(title="Dropout Prediction Service")

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)


model = None
def load_model():
    global model
    client = mlflow.tracking.MlflowClient()
    versions = client.get_latest_versions("dropout_model", stages=["Production"])
    if versions:
        model_uri = f"models:/dropout_model/Production"
        model = mlflow.pyfunc.load_model(model_uri)
    else:
        
        model = DropoutPredictor()
        model.load_model("model.pkl")
load_model()

class Features(BaseModel):
    attendance_rate: float
    test_scores: list[float]
    engagement_time: float
    assignment_completion: float
    weak_topics_count: int

class PredictionResponse(BaseModel):
    riskScore: float
    factors: list[dict]
    recommendations: list[str]

class TrainRequest(BaseModel):
    
    data_source: str = "mongodb"  

@app.post("/predict", response_model=PredictionResponse)
async def predict(features: Features):
    try:
        X = np.array([[
            features.attendance_rate,
            np.mean(features.test_scores) if features.test_scores else 0,
            features.engagement_time,
            features.assignment_completion,
            features.weak_topics_count
        ]])
        if hasattr(model, 'predict_with_explain'):
            risk_score, shap_values, top_factors = model.predict_with_explain(X)
        else:
            risk_score = model.predict(X)[0]
            top_factors = [{"feature": "attendance_rate", "impact": 0.5}]
        
        recommendations = []
        return {
            "riskScore": float(risk_score),
            "factors": top_factors,
            "recommendations": recommendations
        }
    except Exception as e:
        logging.error(f"Prediction error: {e}")
        raise HTTPException(500, detail=str(e))

@app.post("/train")
async def train(req: TrainRequest):
    """
    API endpoint to retrain the model.
    Expected to fetch data from MongoDB (or from request body).
    Registers new model in MLflow and promotes if better.
    """
    try:
        
        df = pd.read_csv("training_data.csv")
        X = df.drop("risk", axis=1)
        y = df["risk"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        from sklearn.ensemble import RandomForestClassifier
        new_model = RandomForestClassifier(n_estimators=100, random_state=42)
        new_model.fit(X_train, y_train)

        # Evaluate
        y_pred = new_model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        auc = roc_auc_score(y_test, new_model.predict_proba(X_test)[:, 1])

        # Log to MLflow
        with mlflow.start_run() as run:
            mlflow.log_params(new_model.get_params())
            mlflow.log_metrics({"accuracy": acc, "auc": auc})
            mlflow.sklearn.log_model(new_model, "model")
            run_id = run.info.run_id
            model_uri = f"runs:/{run_id}/model"
            # Register new version
            result = mlflow.register_model(model_uri, "dropout_model")
            version = result.version

        # Optionally promote to Production if better than current production
        client = mlflow.tracking.MlflowClient()
        current_prod = client.get_latest_versions("dropout_model", stages=["Production"])
        if current_prod:
            current_run_id = current_prod[0].run_id
            current_metrics = mlflow.get_run(current_run_id).data.metrics
            current_auc = current_metrics.get("auc", 0)
            if auc > current_auc:
                client.transition_model_version_stage(
                    name="dropout_model",
                    version=version,
                    stage="Production"
                )
                # Archive old production
                for v in current_prod:
                    client.transition_model_version_stage(
                        name="dropout_model",
                        version=v.version,
                        stage="Archived"
                    )
        else:
            # First model, promote directly
            client.transition_model_version_stage(
                name="dropout_model",
                version=version,
                stage="Production"
            )

        # Reload model into memory
        load_model()

        return {"message": "Training completed", "new_version": version, "accuracy": acc, "auc": auc}
    except Exception as e:
        logging.error(f"Training error: {e}")
        raise HTTPException(500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}