import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
import joblib
import mlflow
from model import DropoutPredictor

# Load data
df = pd.read_csv("training_data.csv")
X = df.drop("risk", axis=1)
y = df["risk"]

# Train
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Evaluate
preds = model.predict(X)
acc = accuracy_score(y, preds)
auc = roc_auc_score(y, model.predict_proba(X)[:, 1])

# Log to MLflow
mlflow.set_tracking_uri("http://mlflow:5000")
with mlflow.start_run():
    mlflow.log_params(model.get_params())
    mlflow.log_metrics({"accuracy": acc, "auc": auc})
    mlflow.sklearn.log_model(model, "model")
    # Register
    mlflow.register_model(f"runs:/{mlflow.active_run().info.run_id}/model", "dropout_model")

# Also save locally for fallback
joblib.dump(model, "model.pkl")
print("Model trained and logged to MLflow.")