# Medical Telegram Data Warehouse

An end-to-end data product pipeline for scraping, transforming, enriching, and analyzing Telegram channels selling Ethiopian medical and cosmetic products. Built with **Python, dbt, FastAPI, YOLOv8, and Dagster**.

---

## 🚀 Project Overview

This project extracts data from public Telegram channels, transforms it into a clean **data warehouse**, enriches it with **image detection**, and exposes analytics via a **REST API**.  

Key capabilities:

- Scrape messages and images from multiple Telegram channels
- Store raw data in a **Data Lake**
- Transform and clean data into a **dimensional star schema** using **dbt**
- Enrich images using **YOLOv8 object detection**
- Expose analytics endpoints via **FastAPI**
- Automate the full pipeline using **Dagster**


medical-telegram-warehouse/
├── .env # Environment variables (API keys, DB creds)
├── api/ # FastAPI application
│ ├── main.py # API entry point
│ ├── database.py # DB connection
│ └── schemas.py # Pydantic models
├── data/ # Raw and processed data
│ ├── raw/ # Raw JSON from Telegram
│ └── images/ # Downloaded images
├── medical_warehouse/ # dbt project
│ ├── models/
│ │ ├── staging/ # Staging models
│ │ └── marts/ # Dimension & fact tables
│ └── tests/ # Custom dbt tests
├── scripts/ # Helper scripts (load to Postgres, YOLO)
├── src/ # Scraper & YOLO scripts
├── tests/ # Unit tests
├── Dockerfile # Python environment
├── docker-compose.yml # Multi-container setup
└── README.md


---

## ⚙️ Setup Instructions

1. Clone the repo:

```bash
git clone https://github.com/SeniyaSultan/medical-telegram-warehouse-clean.git
cd medical-telegram-warehouse-clean
Install Python dependencies:

pip install -r requirements.txt


Copy .env.example to .env and fill in your credentials:

TELEGRAM_BOT_TOKEN=...
TELEGRAM_API_ID=...
TELEGRAM_API_HASH=...
POSTGRES_DB=medical_dw
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_HOST=localhost
POSTGRES_PORT=5432


Create the PostgreSQL database (if not exists):

CREATE DATABASE medical_dw;

🏃 Running the Pipeline

Scrape Telegram messages:

python src/scraper.py


Download message images:

python scripts/download_images.py


Load raw JSON into Postgres:

python scripts/load_raw_to_postgres.py


Run dbt transformations:

dbt run
dbt test
dbt docs generate
dbt docs serve


YOLO image enrichment:

python src/yolo_detect.py
python scripts/load_yolo_to_postgres.py


Start FastAPI for analytics:

uvicorn api.main:app --reload


API docs available at: http://127.0.0.1:8000/docs

Optional: Run full pipeline with Dagster

dagster dev -f medical_warehouse/models/pipeline.py

📊 Data Product Features

Top Products Report: Most mentioned products across channels

Channel Activity: Posting trends per channel

Message Search: Search messages by keyword

Visual Content Stats: Analytics for image posts, classified by YOLO categories

✅ Key Technologies

Python: Scraping, transformation, API

Telethon: Telegram scraping

PostgreSQL: Data warehouse

dbt: ELT transformations & testing

YOLOv8 (Ultralytics): Image detection & categorization

FastAPI: Analytical REST API

Dagster: Pipeline orchestration

Docker: Environment reproducibility

📖 Notes

Sensitive credentials stored in .env (do not commit).

dbt tests ensure unique keys, relationships, and business rules.

Error handling added for YOLO, Postgres, and scraping.

dbt docs provide a visual overview of the star schema.

📌 References

Telethon Documentation

dbt Documentation

Ultralytics YOLOv8

FastAPI Documentation

Dagster Docs
---

## 👤 Author

**Seniya Sultan**  
Junior ML  & Software Developer | Front-End Developer | Aspiring Machine Learning Enthusiast  
[GitHub](https://github.com/SeniyaSultan) | [LinkedIn](https://www.linkedin.com/in/seniyasultan/)

---

## 📂 Folder Structure

