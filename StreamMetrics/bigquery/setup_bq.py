from google.cloud import bigquery
import os

# Set credentials path (adjust if needed)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./bigquery/service-account.json"

# Replace with YOUR actual project ID
PROJECT_ID = "streammetrics-prod"  # ← CHANGE THIS

client = bigquery.Client(project=PROJECT_ID)

# Create dataset
dataset_id = f"{PROJECT_ID}.streammetrics"
dataset = bigquery.Dataset(dataset_id)
dataset.location = "US"

try:
    dataset = client.create_dataset(dataset, exists_ok=True)
    print(f"✅ Dataset 'streammetrics' created in project {PROJECT_ID}")
except Exception as e:
    print(f"⚠️  Dataset creation error: {e}")

# Create table schema
schema = [
    bigquery.SchemaField("window_start", "TIMESTAMP"),
    bigquery.SchemaField("window_end", "TIMESTAMP"),
    bigquery.SchemaField("event_type", "STRING"),
    bigquery.SchemaField("avg_value", "FLOAT"),
    bigquery.SchemaField("ingestion_time", "TIMESTAMP"),
]

table_id = f"{PROJECT_ID}.streammetrics.windowed_metrics"
table = bigquery.Table(table_id, schema=schema)

# Partition by ingestion_time for cost optimization (important for resume!)
table.time_partitioning = bigquery.TimePartitioning(
    type_=bigquery.TimePartitioningType.DAY,
    field="ingestion_time",
)

try:
    table = client.create_table(table, exists_ok=True)
    print(f"✅ Table 'windowed_metrics' created with daily partitioning")
    print(f"   Table ID: {table_id}")
except Exception as e:
    print(f"⚠️  Table creation error: {e}")

print("\n✅ BigQuery setup complete!")
print(f"   Dataset: {PROJECT_ID}.streammetrics")
print(f"   Table: {PROJECT_ID}.streammetrics.windowed_metrics")
