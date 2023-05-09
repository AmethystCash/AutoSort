import requests
import json
import os
from colorama import Fore, Back, Style
from dotenv import load_dotenv
load_dotenv()

url = f"https://discord.com/api/webhooks/{os.environ['webhook_url']}"

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

    response = requests.post(url, data=payload, files=files)

    if response.ok:
        print(Fore.GREEN + f"Webhook signal successful (status code: {response.status_code})" + Style.RESET_ALL)
    else:
        print(Fore.RED + f"Webhook signal failed (status code: {response.status_code})" + Style.RESET_ALL)
        