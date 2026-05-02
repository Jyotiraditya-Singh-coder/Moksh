import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
import joblib
import pickle

# Load interaction data (student_id, question_id, rating) from MongoDB or CSV
df = pd.read_csv("interactions.csv")  # columns: student_id, question_id, rating
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(df[['student_id', 'question_id', 'rating']], reader)
trainset, testset = train_test_split(data, test_size=0.2)

model = SVD(n_factors=50, random_state=42)
model.fit(trainset)

# Save model
joblib.dump(model, "svd_model.pkl")

# Save mapping dictionaries
student_inner_to_raw = {inner: raw for raw, inner in trainset._raw2inner_id_items}
item_inner_to_raw = {inner: raw for raw, inner in trainset._raw2inner_id_items}
joblib.dump(student_inner_to_raw, "student_factors.pkl")
joblib.dump(item_inner_to_raw, "item_factors.pkl")