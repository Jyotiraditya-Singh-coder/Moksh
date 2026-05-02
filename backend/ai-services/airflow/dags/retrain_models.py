from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests

def train_dropout():
    response = requests.post("http://dropout-model:8001/train", json={"data_source": "mongodb"})
    print(response.json())

def train_recommendation():
    response = requests.post("http://recommendation-engine:8006/train", json={})
    print(response.json())

def train_kt():
    response = requests.post("http://skill-navigator:8009/train-kt", json={})
    print(response.json())

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('retrain_models', default_args=default_args, schedule_interval='@weekly')

t1 = PythonOperator(task_id='train_dropout', python_callable=train_dropout, dag=dag)
t2 = PythonOperator(task_id='train_recommendation', python_callable=train_recommendation, dag=dag)
t3 = PythonOperator(task_id='train_kt', python_callable=train_kt, dag=dag)

t1 >> t2 >> t3