# src/scraper_tgstat.py
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os
from loguru import logger

# Channels to scrape (public tgstat pages)
CHANNELS = [
    "chemed",
    "lobelia4cosmetics",
    "tikvahpharma"
]

BASE_PATH = "data/raw/telegram_messages"

def scrape_channel(channel):
    logger.info(f"Scraping {channel} from tgstat...")
    url = f"https://t.me/s/{channel}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to fetch {channel}: {e}")
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    posts = soup.find_all("div", class_="tgme_widget_message_wrap")

    logger.info(f"Found {len(posts)} posts for {channel}")

    messages = []
    for post in posts:
        text_div = post.find("div", class_="tgme_widget_message_text")
        record = {
            "channel_name": channel,
            "message_date": datetime.utcnow().isoformat(),
            "message_text": text_div.text if text_div else "",
            "views": None,
            "forwards": None,
            "has_media": False,
            "image_path": None
        }
        messages.append(record)

    return messages   # ✅ THIS WAS MISSING


def save_messages(channel, messages):
    date = datetime.utcnow().strftime("%Y-%m-%d")
    out_dir = f"{BASE_PATH}/{date}"
    os.makedirs(out_dir, exist_ok=True)
    file_path = f"{out_dir}/{channel}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)
    logger.success(f"Saved {len(messages)} messages for {channel} to {file_path}")

def main():
    os.makedirs(BASE_PATH, exist_ok=True)
    for channel in CHANNELS:
        messages = scrape_channel(channel)
        save_messages(channel, messages)  # ← remove the if

if __name__ == "__main__":
    main()
