import requests
import json
import os
from dotenv import load_dotenv
from utils import webhook_signal
load_dotenv()




embed = {
    "title": "Example Embed",
    "description": "This is an example of an embed message.",
    "color": 16711680,
    "fields": [
        {
            "name": "Field 1",
            "value": "This is the value of field 1",
            "inline": False
        },
        {
            "name": "Field 2",
            "value": "This is the value of field 2",
            "inline": True
        }
    ]
}
data = {
    "content": "This is the main message content.",
    "embeds": [embed]
}

webhook_url = f"https://discord.com/api/webhooks/{os.environ['webhook_url']}"
headers = {"Content-Type": "application/json"}
response = requests.post(webhook_url, data=json.dumps(data), headers=headers)

if response.status_code != 204:
    print(f"Failed to send message with error code: {response.status_code}")
else:
    print("Message sent successfully!")