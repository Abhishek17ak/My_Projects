# ChurnGuard: Production-Grade Customer Churn Prediction System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PySpark](https://img.shields.io/badge/PySpark-3.5+-orange.svg)](https://spark.apache.org/)
[![Airflow](https://img.shields.io/badge/Airflow-3.0+-green.svg)](https://airflow.apache.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An end-to-end machine learning pipeline for predicting telecom customer churn, featuring automated daily retraining, distributed feature engineering with PySpark, and production orchestration with Apache Airflow.

## 🎯 Project Overview

ChurnGuard is a production-ready ML system designed to identify at-risk customers before they churn, enabling proactive retention strategies. The system processes 7,000+ customer records, engineers 54+ features using distributed computing, and achieves **76% accuracy** with **55% precision** and **81% ROC-AUC**.

### Key Features

* Automated ML Pipeline with Airflow
* Distributed Processing with PySpark
* High Model Performance
* Docker-based PostgreSQL Database
* Model Versioning and Monitoring

## 📊 Model Performance

| Metric    | Score  |
| --------- | ------ |
| Accuracy  | 76.51% |
| Precision | 55.16% |
| Recall    | 61.50% |
| F1-Score  | 58.15% |
| ROC-AUC   | 81.17% |

## 🏗️ Architecture

PostgreSQL → PySpark Feature Engineering → XGBoost Model Training → Airflow Orchestration → Scoring & Predictions

## 🛠️ Tech Stack

* Python 3.13
* XGBoost, scikit-learn
* PySpark 3.5+
* Apache Airflow 3.0
* PostgreSQL 17
* Docker
* Pandas, Matplotlib, Seaborn

## 📁 Project Structure

```
ChurnGuard/
├── data/
│   ├── WA_Fn-UseC_-Telco-Customer-Churn.csv
│   └── processed_features.parquet
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_feature_engineering.ipynb
│   └── 03_train_xgboost.ipynb
├── src/
│   └── feature_engineering.py
├── results/
│   └── xgboost_churn_model.pkl
├── setup_db.py
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

### Prerequisites

* Python 3.8+
* Docker Desktop
* Java 8+
* Homebrew (macOS)

### Installation

```
git clone https://github.com/Abhishek17ak/My_Projects.git
cd "My_Projects/ChurnGuard Project_Customer_Churn_Prediction"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
brew install libomp
```

### Database Setup

```
docker run -d --name churn-postgres -e POSTGRES_USER=churnuser -e POSTGRES_PASSWORD=churnpass -e POSTGRES_DB=churn_db -p 5432:5432 postgres:17
python setup_db.py
```

## 📊 Running the Pipeline

### Interactive Mode

```
jupyter notebook
```

Run notebooks in order.

### Production Mode (Airflow)

```
export AIRFLOW_HOME=~/airflow
airflow db migrate
airflow standalone
```

Navigate to: [http://localhost:8080](http://localhost:8080)

## 🔄 Airflow DAG Workflow

extract_customer_data → feature_engineering → train_xgboost_model → generate_predictions → cleanup_temp_files

## 📈 Key Insights

* Churn rate: ~26.5%
* Month-to-month contracts show highest churn
* Higher charges correlate with churn
* Tenure is strongest churn predictor

## 🐛 Troubleshooting

### Docker

```
docker ps
docker logs churn-postgres
docker restart churn-postgres
```

### PySpark

```
java -version
export JAVA_HOME=$(/usr/libexec/java_home)
```

### Airflow

```
ls -la ~/airflow/dags/
python ~/airflow/dags/churn_prediction_pipeline.py
```

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch
3. Commit and push
4. Open a PR

## 📄 License

MIT License

## 📧 Contact

Your Name – [abhishek.kalugade17@gmail.com](mailto:abhishek.kalugade17@gmail.com)

Project Link: [https://github.com/Abhishek17ak/My_Projects/tree/main/ChurnGuard%20Project_Customer_Churn_Prediction](https://github.com/Abhishek17ak/My_Projects/tree/main/ChurnGuard%20Project_Customer_Churn_Prediction)

⭐ If you found this helpful, please consider starring the repo.
