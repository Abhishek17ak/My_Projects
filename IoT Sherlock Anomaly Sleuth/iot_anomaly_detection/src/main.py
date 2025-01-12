import os
import sys
from spark_setup import create_spark_session, check_spark_connection
from data_loading import load_and_preprocess_data
from feature_engineering import prepare_features
from model_training import train_and_evaluate_models, tune_random_forest
from streaming import start_streaming_detection
from visualization import start_dashboard

def main():
    # Set environment variables
    os.environ['PYSPARK_PYTHON'] = sys.executable
    os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

    # Create Spark session
    spark = create_spark_session()
    check_spark_connection(spark)

    # Load and preprocess data
    df = load_and_preprocess_data(spark)

    # Prepare features
    df_clean = prepare_features(df)

    # Train and evaluate models
    best_rf = train_and_evaluate_models(df_clean)

    # Tune Random Forest model
    best_rf = tune_random_forest(df_clean)

    # Start streaming detection
    start_streaming_detection(spark, best_rf)

    # Start dashboard
    start_dashboard()

if __name__ == "__main__":
    main()
