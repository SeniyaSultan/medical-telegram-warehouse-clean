import os
import json
from datetime import datetime
from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto
from dotenv import load_dotenv
from loguru import logger
import asyncio

load_dotenv()

API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

CHANNELS = [
    "chemed",
    "lobelia4cosmetics",
    "tikvahpharma",
]

BASE_PATH = "data/raw/telegram_messages"

client = TelegramClient("bot_session", API_ID, API_HASH)

async def scrape():
    await client.start(bot_token=BOT_TOKEN)  # login as bot

    for channel in CHANNELS:
        logger.info(f"Scraping {channel}")
        messages = []
        async for msg in client.iter_messages(channel, limit=500):
            record = {
                "message_id": msg.id,
                "channel_name": channel,
                "message_date": msg.date.isoformat() if msg.date else None,
                "message_text": msg.text,
                "views": msg.views,
                "forwards": msg.forwards,
                "has_media": bool(msg.media),
                "image_path": None
            }

            if isinstance(msg.media, MessageMediaPhoto):
                img_dir = f"data/raw/images/{channel}"
                os.makedirs(img_dir, exist_ok=True)
                img_path = f"{img_dir}/{msg.id}.jpg"
                await msg.download_media(img_path)
                record["image_path"] = img_path

            messages.append(record)

        date = datetime.utcnow().strftime("%Y-%m-%d")
        out_dir = f"{BASE_PATH}/{date}"
        os.makedirs(out_dir, exist_ok=True)

        with open(f"{out_dir}/{channel}.json", "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)

        logger.success(f"{channel} done")

if __name__ == "__main__":
    asyncio.run(scrape())
