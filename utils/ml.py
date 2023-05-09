import requests
import cv2
import os
from colorama import Fore, Back, Style
from dotenv import load_dotenv
load_dotenv()

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


def get_material(img_bytes):
    response = requests.post(API_URL, headers=headers, data=img_bytes)
    
    if response.ok:
        predictions = response.json()
        
        print(Fore.GREEN + f"Get material successful (status code {response.status_code})" + Style.RESET_ALL)
        print(predictions)
        
        material = predictions[0]['label']
        certainty = predictions[0]['score']
        return trash_mapper[material], certainty
    else:
        print(Fore.RED + f"Get material failed (status code {response.status_code})" + Style.RESET_ALL)
        return trash_mapper['trash'], 0


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
    
    
