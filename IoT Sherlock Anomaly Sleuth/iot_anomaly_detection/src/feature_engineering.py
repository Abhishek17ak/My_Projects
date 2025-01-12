from pyspark.sql.functions import when, col
from pyspark.ml.feature import VectorAssembler

def prepare_features(df):
    df = df.withColumn("is_malicious", when(col("label").contains("Malicio"), 1).otherwise(0))

    selected_features = [
        "duration", "orig_bytes", "resp_bytes", "missed_bytes",
        "orig_pkts", "orig_ip_bytes", "resp_pkts", "resp_ip_bytes",
        "is_malicious"
    ]

    df_selected = df.select(selected_features)
    df_clean = df_selected.na.fill(0)

    feature_columns = ["duration", "orig_bytes", "resp_bytes", "missed_bytes", "orig_pkts", "orig_ip_bytes", "resp_pkts", "resp_ip_bytes"]
    assembler = VectorAssembler(inputCols=feature_columns, outputCol="features")
    df_vectorized = assembler.transform(df_clean)

    return df_vectorized
