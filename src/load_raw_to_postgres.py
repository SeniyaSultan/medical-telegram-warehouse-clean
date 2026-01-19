import os
import json
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Load DB credentials from .env
conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST", "localhost"),
    port=os.getenv("POSTGRES_PORT", 5432),
    user=os.getenv("POSTGRES_USER", "postgres"),
    password=os.getenv("POSTGRES_PASSWORD", "postgres"),
    database=os.getenv("POSTGRES_DB", "medical_dw")
)

cur = conn.cursor()

BASE_PATH = "data/raw/telegram_messages"

# Loop through all date folders
for date_dir in os.listdir(BASE_PATH):
    date_path = os.path.join(BASE_PATH, date_dir)
    if not os.path.isdir(date_path):
        continue

    for json_file in os.listdir(date_path):
        if json_file.endswith(".json"):
            file_path = os.path.join(date_path, json_file)
            channel_name = json_file.replace(".json", "")

            with open(file_path, "r", encoding="utf-8") as f:
                messages = json.load(f)

            for msg in messages:
                cur.execute("""
                    INSERT INTO raw.telegram_messages (
                        channel_name, message_date, message_text, views, forwards, has_media, image_path
                    ) VALUES (%s,%s,%s,%s,%s,%s,%s)
                    ON CONFLICT (message_id) DO NOTHING
                """, (
                    msg.get("channel_name"),
                    msg.get("message_date"),
                    msg.get("message_text"),
                    msg.get("views"),
                    msg.get("forwards"),
                    msg.get("has_media"),
                    msg.get("image_path")
                ))

conn.commit()
cur.close()
conn.close()
print("All JSON files loaded into Postgres successfully!")
