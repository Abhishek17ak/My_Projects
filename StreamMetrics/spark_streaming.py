from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType, FloatType, IntegerType

spark = SparkSession.builder \
    .appName("KafkaStructuredStreaming") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.0") \
    .getOrCreate()

# Read from Kafka topic
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "test-metrics") \
    .option("startingOffsets", "earliest") \
    .load()

# Define JSON schema
schema = StructType() \
    .add("event_type", StringType()) \
    .add("value", FloatType()) \
    .add("server", StringType()) \
    .add("timestamp", IntegerType())

# Parse JSON payloads
parsed = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

# Output parsed columns to the console
query = parsed.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
