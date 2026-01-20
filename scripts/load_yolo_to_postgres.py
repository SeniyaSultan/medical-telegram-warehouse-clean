import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("POSTGRES_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")

print("DEBUG:", DB_HOST, DB_NAME, DB_USER, DB_PASS)

conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASS
)

cur = conn.cursor()

cur.execute("""
CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.image_detections (
    message_id TEXT,
    channel_name TEXT,
    detected_object TEXT,
    confidence FLOAT,
    image_category TEXT
);
""")

df = pd.read_csv("data/yolo_results.csv")

for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO raw.image_detections
        VALUES (%s, %s, %s, %s, %s)
    """, tuple(row))

conn.commit()
cur.close()
conn.close()

print("✅ YOLO results loaded into Postgres")
