from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, DoubleType
from pyspark.ml.feature import VectorAssembler

def start_streaming_detection(spark, best_rf):
    schema = StructType([
        StructField("duration", DoubleType(), True),
        StructField("orig_bytes", DoubleType(), True),
        StructField("resp_bytes", DoubleType(), True),
        StructField("missed_bytes", DoubleType(), True),
        StructField("orig_pkts", DoubleType(), True),
        StructField("orig_ip_bytes", DoubleType(), True),
        StructField("resp_pkts", DoubleType(), True),
        StructField("resp_ip_bytes", DoubleType(), True)
    ])

    streaming_df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "iot_data") \
        .load() \
        .select(from_json(col("value").cast("string"), schema).alias("data")) \
        .select("data.*")

    feature_cols = ["duration", "orig_bytes", "resp_bytes", "missed_bytes", "orig_pkts", "orig_ip_bytes", "resp_pkts", "resp_ip_bytes"]
    assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
    streaming_vector = assembler.transform(streaming_df)

    streaming_predictions = best_rf.transform(streaming_vector)

    query = streaming_predictions \
        .writeStream \
        .outputMode("append") \
        .format("console") \
        .start()

    query.awaitTermination()
