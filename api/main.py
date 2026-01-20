from fastapi import FastAPI
from sqlalchemy import create_engine, text
import os

app = FastAPI(title="Medical Telegram Analytics API")

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

@app.get("/api/reports/top-products")
def top_products(limit: int = 10):
    query = """
    SELECT
        LOWER(word) AS product,
        COUNT(*) AS mentions
    FROM fct_messages,
    LATERAL regexp_split_to_table(message_text, '\\s+') AS word
    GROUP BY product
    ORDER BY mentions DESC
    LIMIT :limit;
    """
    with engine.connect() as conn:
        result = conn.execute(text(query), {"limit": limit})
        return result.mappings().all()


@app.get("/api/reports/visual-content")
def visual_content():
    query = """
    SELECT
        image_category,
        COUNT(*) AS total
    FROM fct_image_detections
    GROUP BY image_category;
    """
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return result.mappings().all()
