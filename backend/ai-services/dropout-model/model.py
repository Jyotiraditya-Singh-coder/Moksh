import joblib
import shap
import numpy as np
import mlflow
import mlflow.sklearn

class DropoutPredictor:
    def __init__(self):
        self.model = None
        self.explainer = None

    def load_model(self, path):
        self.model = joblib.load(path)
        self.explainer = shap.TreeExplainer(self.model)

    def predict_with_explain(self, X):
        pred = self.model.predict_proba(X)[:, 1]
        shap_values = self.explainer.shap_values(X)
        if isinstance(shap_values, list):
            shap_vals = shap_values[1]
        else:
            shap_vals = shap_values
        feature_names = ["attendance_rate", "avg_test_score", "engagement_time", "assignment_completion", "weak_topics_count"]
        impacts = list(zip(feature_names, shap_vals[0]))
        impacts.sort(key=lambda x: abs(x[1]), reverse=True)
        top_factors = [{"feature": f, "impact": float(i)} for f, i in impacts[:3]]
        return pred, shap_values, top_factors

    def save(self, path):
        joblib.dump(self.model, path)

    @staticmethod
    def log_to_mlflow(model, params, metrics):
        with mlflow.start_run():
            mlflow.log_params(params)
            mlflow.log_metrics(metrics)
            mlflow.sklearn.log_model(model, "model")
            # Register model
            mlflow.register_model(f"runs:/{mlflow.active_run().info.run_id}/model", "dropout_model")