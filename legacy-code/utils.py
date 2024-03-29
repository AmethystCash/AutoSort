import requests
import os
from dotenv import load_dotenv
import cv2
load_dotenv()

# For firebase integration
import firebase_admin
from firebase_admin import db
import json
import time
cred_obj = firebase_admin.credentials.Certificate('autosort-c230c-3aa20a6e2336.json')
default_app = firebase_admin.initialize_app(
    cred_obj, 
    {'databaseURL': "https://autosort-c230c-default-rtdb.europe-west1.firebasedatabase.app"})
ref = db.reference("/bin1-entries")  # bin1 db location


trash_mapper = {
    'paper': 'paper',
    'cardboard': 'paper',
    'metal': 'plastic',
    'plastic': 'plastic',
    'glass': 'glass',
    'trash': 'misc',
}

API_URL = "https://api-inference.huggingface.co/models/yangy50/garbage-classification"
headers = {"Authorization": f"Bearer {os.getenv('API_KEY')}"}







"""
TODO: 
3. error handling
4. documentation
"""








# the function that tells us what material the object is made of

def get_material_old(frame):
    _, img_encoded = cv2.imencode('.jpg', frame)
    response = requests.post(API_URL, headers=headers, data=img_encoded.tobytes())
    if response.ok:
        predictions = response.json()
        print(predictions)
        material = predictions[0]['label']
        certainty = predictions[0]['score']
        return trash_mapper[material], certainty
    else:
        print(f"Request failed with status code {response.status_code}")
        return trash_mapper['trash'], 0
    
    
def get_material(img_bytes):
    response = requests.post(API_URL, headers=headers, data=img_bytes)
    if response.ok:
        predictions = response.json()
        print(predictions)
        material = predictions[0]['label']
        certainty = predictions[0]['score']
        return trash_mapper[material], certainty
    else:
        print(f"Request failed with status code {response.status_code}")
        return trash_mapper['trash'], 0
    
    
    
    
    
# the firebase push function

def into_firebase(data):
    material = data['material']
    accuracy = data['certainty']
    
    most_recent = time.strftime("%X %x")  # format: hr:min:sec dd/mm/yy
    entries_len = len(ref.get())
    entry_set = {"Accuracy %": accuracy, "Time": most_recent, "Type": material}
    #test_set = {"Test": "test"}

    entry_num = entries_len
    entry_name = str(entry_num)
    ref.child(entry_name).update(entry_set)
    print(f"Firebase entries length: {entries_len}")
    




# a fun lil discord webhook, this way we can avoid restructuring the firebase

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





# the door opening function

def open_door(material):
    door_mapper = {
        'plastic': 1,
        'glass': 2,
        'paper': 3,
        'misc': 4,
    }
    # you can use either this or some if/else
    
    print(f"opening the {material} door with number {door_mapper[material]}")
