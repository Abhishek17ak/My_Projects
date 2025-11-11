import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import pandas as pd

# Step 1: Connect as any user to create churnuser
try:
    # Try connecting with no specific user (container default)
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="postgres",  # Default DB
        user="",  # Empty to use system default
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    # Create user and database
    cursor.execute("CREATE USER churnuser WITH PASSWORD 'churnpass';")
    cursor.execute("CREATE DATABASE churn_db OWNER churnuser;")
    cursor.execute("GRANT ALL PRIVILEGES ON DATABASE churn_db TO churnuser;")
    
    cursor.close()
    conn.close()
    print("✅ User and database created successfully!")
    
except Exception as e:
    print(f"⚠️ Error during setup: {e}")
    print("Trying alternative connection method...")

# Step 2: Connect to churn_db and create table
try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="churn_db",
        user="churnuser",
        password="churnpass"
    )
    cursor = conn.cursor()
    
    # Create customers table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS customers (
        customerid VARCHAR PRIMARY KEY,
        gender VARCHAR,
        seniorcitizen INT,
        partner VARCHAR,
        dependents VARCHAR,
        tenure INT,
        phoneservice VARCHAR,
        multiplelines VARCHAR,
        internetservice VARCHAR,
        onlinesecurity VARCHAR,
        onlinebackup VARCHAR,
        deviceprotection VARCHAR,
        techsupport VARCHAR,
        streamingtv VARCHAR,
        streamingmovies VARCHAR,
        contract VARCHAR,
        paperlessbilling VARCHAR,
        paymentmethod VARCHAR,
        monthlycharges NUMERIC,
        totalcharges VARCHAR,
        churn VARCHAR
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    
    # Load CSV data
    df = pd.read_csv('./data/WA_Fn-UseC_-Telco-Customer-Churn.csv')
    
    # Clean column names (lowercase, no spaces)
    df.columns = df.columns.str.lower().str.replace(' ', '')
    
    # Insert data
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO customers VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (customerid) DO NOTHING
        """, tuple(row))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"✅ Loaded {len(df)} rows into customers table!")
    
except Exception as e:
    print(f"❌ Error: {e}")


