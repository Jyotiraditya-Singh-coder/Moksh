import mlflow
import os

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

def load_production_model(model_name):
    client = mlflow.tracking.MlflowClient()
    versions = client.get_latest_versions(model_name, stages=["Production"])
    if not versions:
        raise Exception(f"No production model found for {model_name}")
    model_uri = f"models:/{model_name}/Production"
    return mlflow.pyfunc.load_model(model_uri)