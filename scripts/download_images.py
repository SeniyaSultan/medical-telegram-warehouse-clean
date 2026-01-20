import os
import json
import requests

RAW_PATH = "data/raw/telegram_messages"
IMG_PATH = "data/raw/images"

for file in os.listdir(os.path.join(RAW_PATH, "2026-01-19")):
    if not file.endswith(".json"):
        continue

    channel_name = file.replace(".json", "")
    os.makedirs(os.path.join(IMG_PATH, channel_name), exist_ok=True)

    with open(os.path.join(RAW_PATH, "2026-01-19", file), "r", encoding="utf-8") as f:
        messages = json.load(f)

    for msg in messages:
        if msg.get("has_media") and msg.get("image_url"):
            img_url = msg["image_url"]
            msg_id = msg["message_id"]
            save_path = os.path.join(IMG_PATH, channel_name, f"{msg_id}.jpg")

            try:
                r = requests.get(img_url)
                if r.status_code == 200:
                    with open(save_path, "wb") as img_f:
                        img_f.write(r.content)
            except Exception as e:
                print(f"Failed {msg_id}: {e}")

print("✅ All images downloaded")
