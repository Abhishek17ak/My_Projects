from pyspark.sql import SparkSession

def create_spark_session():
    spark = SparkSession.builder \
        .appName("IoT Anomaly Detection") \
        .config("spark.driver.memory", "4g") \
        .config("spark.executor.memory", "4g") \
        .config("spark.cores.max", "4") \
        .config("spark.sql.shuffle.partitions", "100") \
        .config("spark.default.parallelism", "100") \
        .config("spark.driver.maxResultSize", "2g") \
        .master("local[*]") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")
    return spark

def check_spark_connection(spark):
    try:
        spark.sql("SELECT 1").show()
        print("Spark session is active and connected.")
    except Exception as e:
        print(f"Error connecting to Spark: {str(e)}")
