from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, lit
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler, StandardScaler
from functools import reduce

def load_data_from_postgres():
    """Load customer data from PostgreSQL"""
    spark = SparkSession.builder \
        .appName("ChurnGuard-FeatureEngineering") \
        .config("spark.jars", "/Users/abhishekkalugade/Programming/My_Projects/ChurnGuard Project_Customer_Churn_Prediction/postgresql-42.7.8.jar") \
        .getOrCreate()
    
    jdbc_url = "jdbc:postgresql://localhost:5432/churn_db"
    properties = {
        "user": "churnuser",
        "password": "churnpass",
        "driver": "org.postgresql.Driver"
    }
    
    df = spark.read.jdbc(url=jdbc_url, table="customers", properties=properties)
    return spark, df

def engineer_features(df):
    """Create new features for churn prediction"""
    
    # 1. Tenure Buckets (group similar tenure customers)
    df = df.withColumn("tenure_group", 
        when(col("tenure") <= 12, "0-1 year")
        .when(col("tenure") <= 24, "1-2 years")
        .when(col("tenure") <= 48, "2-4 years")
        .when(col("tenure") <= 60, "4-5 years")
        .otherwise("5+ years")
    )
    
    # 2. Total Services Count (internet, phone, etc.)
    service_cols = ['phoneservice', 'multiplelines', 'internetservice', 
                    'onlinesecurity', 'onlinebackup', 'deviceprotection', 
                    'techsupport', 'streamingtv', 'streamingmovies']
    
    # Create service count columns and sum them
    service_conditions = [when(col(c) == "Yes", 1).otherwise(0) for c in service_cols]
    df = df.withColumn("total_services", reduce(lambda a, b: a + b, service_conditions))
    
    # 3. Monthly Charges per Service (value metric)
    df = df.withColumn("charges_per_service",
        col("monthlycharges") / (col("total_services") + 1)  # +1 to avoid division by zero
    )
    
    # 4. Has Partner or Dependents (family indicator)
    df = df.withColumn("has_family",
        when((col("partner") == "Yes") | (col("dependents") == "Yes"), 1).otherwise(0)
    )
    
    # 5. Convert totalcharges to numeric (handle empty strings)
    df = df.withColumn("totalcharges_clean",
        when(col("totalcharges") == " ", 0.0)
        .otherwise(col("totalcharges").cast("double"))
    )
    
    # 6. Average Monthly Spend (over tenure)
    df = df.withColumn("avg_monthly_spend",
        col("totalcharges_clean") / (col("tenure") + 1)
    )
    
    return df

def encode_categorical_features(df):
    """One-hot encode categorical variables"""
    
    categorical_cols = ['gender', 'partner', 'dependents', 'phoneservice',
                       'multiplelines', 'internetservice', 'onlinesecurity',
                       'onlinebackup', 'deviceprotection', 'techsupport',
                       'streamingtv', 'streamingmovies', 'contract',
                       'paperlessbilling', 'paymentmethod', 'tenure_group']
    
    # String Indexing
    indexers = [StringIndexer(inputCol=col, outputCol=col+"_index", handleInvalid="keep") 
                for col in categorical_cols]
    
    # One-Hot Encoding
    encoders = [OneHotEncoder(inputCol=col+"_index", outputCol=col+"_encoded") 
                for col in categorical_cols]
    
    from pyspark.ml import Pipeline
    pipeline = Pipeline(stages=indexers + encoders)
    df = pipeline.fit(df).transform(df)
    
    return df

def create_feature_vector(df):
    """Combine all features into a single vector for modeling"""
    
    # Select encoded categorical features
    encoded_cols = [c for c in df.columns if c.endswith("_encoded")]
    
    # Numeric features
    numeric_cols = ['tenure', 'monthlycharges', 'totalcharges_clean', 
                   'seniorcitizen', 'total_services', 'charges_per_service',
                   'has_family', 'avg_monthly_spend']
    
    # Assemble features
    assembler = VectorAssembler(
        inputCols=encoded_cols + numeric_cols,
        outputCol="features_unscaled"
    )
    df = assembler.transform(df)
    
    # Scale features
    scaler = StandardScaler(inputCol="features_unscaled", outputCol="features")
    df = scaler.fit(df).transform(df)
    
    # Encode target variable (churn)
    df = df.withColumn("label", when(col("churn") == "Yes", 1).otherwise(0))
    
    return df

if __name__ == "__main__":
    # Load data
    spark, df = load_data_from_postgres()
    print(f"Loaded {df.count()} rows")
    
    # Feature engineering
    df = engineer_features(df)
    print("✅ Feature engineering complete")
    
    # Encode categorical features
    df = encode_categorical_features(df)
    print("✅ Categorical encoding complete")
    
    # Create feature vector
    df = create_feature_vector(df)
    print("✅ Feature vector created")
    
    # Select final columns
    final_df = df.select("customerid", "features", "label")
    final_df.show(5)
    
    # Save processed data
    final_df.write.mode("overwrite").parquet("./data/processed_features.parquet")
    print("✅ Saved processed features to parquet")
    
    spark.stop()

