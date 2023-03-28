import requests
import os
from dotenv import load_dotenv
load_dotenv()

# function for getting packaging info from a picture

API_URL = "https://api-inference.huggingface.co/models/yangy50/garbage-classification"
headers = {"Authorization": f"Bearer {os.getenv('API_URL')}"}


def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    if response.ok:
        predictions = response.json()
        print(predictions)
    else:
        print(f"Request failed with status code {response.status_code}")
