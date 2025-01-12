import os
from pyspark.sql.types import StructType, StructField, StringType, LongType, DoubleType

def find_conn_log_files(root_dir):
    conn_log_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == 'conn.log.labeled':
                conn_log_files.append(os.path.join(dirpath, filename))
    return conn_log_files

def load_and_preprocess_data(spark):
    dataset_dir = "../data/iot23_dataset"
    conn_log_files = find_conn_log_files(dataset_dir)

    schema = StructType([
        StructField("ts", StringType(), True),
        StructField("uid", StringType(), True),
        StructField("id.orig_h", StringType(), True),
        StructField("id.orig_p", LongType(), True),
        StructField("id.resp_h", StringType(), True),
        StructField("id.resp_p", LongType(), True),
        StructField("proto", StringType(), True),
        StructField("service", StringType(), True),
        StructField("duration", DoubleType(), True),
        StructField("orig_bytes", LongType(), True),
        StructField("resp_bytes", LongType(), True),
        StructField("conn_state", StringType(), True),
        StructField("local_orig", StringType(), True),
        StructField("local_resp", StringType(), True),
        StructField("missed_bytes", LongType(), True),
        StructField("history", StringType(), True),
        StructField("orig_pkts", LongType(), True),
        StructField("orig_ip_bytes", LongType(), True),
        StructField("resp_pkts", LongType(), True),
        StructField("resp_ip_bytes", LongType(), True),
        StructField("label", StringType(), True),
        StructField("detailed-label", StringType(), True)
    ])

    df = spark.read.csv(conn_log_files, sep="\t", schema=schema, comment="#")
    return df
