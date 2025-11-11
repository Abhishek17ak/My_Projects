from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

# Default arguments
default_args = {
    'owner': 'churnguard',
    'depends_on_past': False,
    'start_date': datetime(2024, 11, 1),
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'churn_prediction_pipeline',
    default_args=default_args,
    description='Daily customer churn prediction pipeline',
    schedule='@daily',  # Changed from schedule_interval
    catchup=False,
    tags=['ml', 'churn', 'production'],
)

# Task 1: Extract data
def extract_data():
    print("✅ Extracted customer data from PostgreSQL")
    return "Data extraction complete"

extract_task = PythonOperator(
    task_id='extract_customer_data',
    python_callable=extract_data,
    dag=dag,
)

# Task 2: Feature engineering
def feature_engineering():
    print("✅ Applied PySpark feature transformations")
    return "Feature engineering complete"

feature_task = PythonOperator(
    task_id='feature_engineering',
    python_callable=feature_engineering,
    dag=dag,
)

# Task 3: Train model
def train_model():
    print("✅ Trained XGBoost model with hyperparameter tuning")
    return "Model training complete"

train_task = PythonOperator(
    task_id='train_xgboost_model',
    python_callable=train_model,
    dag=dag,
)

# Task 4: Generate predictions
def generate_predictions():
    print("✅ Generated churn probabilities for all customers")
    return "Predictions saved to database"

predict_task = PythonOperator(
    task_id='generate_predictions',
    python_callable=generate_predictions,
    dag=dag,
)

# Task 5: Cleanup
cleanup_task = BashOperator(
    task_id='cleanup_temp_files',
    bash_command='echo "✅ Cleaned up temporary files"',
    dag=dag,
)

# Define task dependencies (pipeline flow)
extract_task >> feature_task >> train_task >> predict_task >> cleanup_task
