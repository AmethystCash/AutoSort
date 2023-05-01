import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()



def webhook_signal(data):
    material = data['material']
    certainty = data['certainty']
    date = data['datetime']
    img = data['img_bytes']
    
    embed = {
        "title": f"{material.title()} ({certainty * 100:.2f}%)",
        "description": "" if certainty != 0 else "The model did not respond :(",
        "color": 0x00ff00 if certainty != 0 else 0xff0000,
        "image": {"url": "attachment://image.jpg"},
        "footer": {
            "text": date
        }
    }
    files = {
        "image.jpg": img
    }
    payload = {
        "payload_json": json.dumps({"embeds": [embed]})
    }

    url = f"https://discord.com/api/webhooks/{os.environ['webhook_url']}"
    response = requests.post(url, data=payload, files=files)

    print(f"Webhook signal response: {response.status_code}\n{response.content}")