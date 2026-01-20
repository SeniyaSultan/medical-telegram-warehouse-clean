from dagster import op, job
import subprocess

@op
def scrape():
    subprocess.run(["python", "src/scraper.py"], check=True)

@op
def load_raw():
    subprocess.run(["python", "scripts/load_raw_to_postgres.py"], check=True)

@op
def dbt_run():
    subprocess.run(["dbt", "run"], check=True)

@op
def yolo():
    subprocess.run(["python", "src/yolo_detect.py"], check=True)
    subprocess.run(["python", "scripts/load_yolo_to_postgres.py"], check=True)

@job
def telegram_pipeline():
    scrape()
    load_raw()
    dbt_run()
    yolo()
