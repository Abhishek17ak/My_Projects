from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, window, current_timestamp, from_unixtime
from pyspark.sql.types import StructType, StringType, FloatType, IntegerType, TimestampType
import os

# Set Google credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./bigquery/service-account.json"

# ⚠️ REPLACE THESE WITH YOUR VALUES
PROJECT_ID = "streammetrics-prod"  # Your GCP project ID
BUCKET_NAME = "streammetrics-temp-bucket"  # Your GCS bucket name

spark = SparkSession.builder \
    .appName("KafkaStructuredStreaming") \
    .config("spark.jars.packages", 
            "org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.1,"
            "com.google.cloud.spark:spark-bigquery-with-dependencies_2.13:0.36.0,"
            "javax.inject:javax.inject:1") \
    .getOrCreate()

# Set Google credentials in Spark config
spark.conf.set("google.cloud.auth.service.account.json.keyfile", 
               "./bigquery/service-account.json")

# Read from Kafka
raw_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "test-metrics") \
    .option("startingOffsets", "earliest") \
    .load()

# Parse JSON
schema = StructType() \
    .add("event_type", StringType()) \
    .add("value", FloatType()) \
    .add("server", StringType()) \
    .add("timestamp", IntegerType())

parsed = raw_df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")
parsed = parsed.withColumn("event_time", from_unixtime(col("timestamp")).cast(TimestampType()))

# Windowed aggregation
agg = parsed.groupBy(
    window(col("event_time"), "10 seconds", "5 seconds"),
    col("event_type")
).avg("value")

output = agg.select(
    col("window.start").alias("window_start"),
    col("window.end").alias("window_end"),
    col("event_type"),
    col("avg(value)").alias("avg_value"),
    current_timestamp().alias("ingestion_time")
)

# Write to BigQuery
print(f"📊 Starting streaming to BigQuery: {PROJECT_ID}.streammetrics.windowed_metrics")
query = output.writeStream \
    .outputMode("complete") \
    .format("bigquery") \
    .option("table", f"{PROJECT_ID}.streammetrics.windowed_metrics") \
    .option("temporaryGcsBucket", BUCKET_NAME) \
    .option("checkpointLocation", "./logs/bq-checkpoint") \
    .trigger(processingTime='10 seconds') \
    .start()

print("✅ Streaming job started. Waiting for events...")
query.awaitTermination()
