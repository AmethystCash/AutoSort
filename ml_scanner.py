import cv2
import requests
import os
import numpy as np
from dotenv import load_dotenv
load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/yangy50/garbage-classification"
headers = {"Authorization": f"Bearer {os.getenv('API_URL')}"}

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while True:
    success, frame = cap.read()
    cv2.imshow('frame', frame)

    key = cv2.waitKey(1)
    if key == ord(' '):  # press Space to take a pic that then gets sent to the api
        _, img_encoded = cv2.imencode('.jpg', frame)
        response = requests.post(API_URL, headers=headers, data=img_encoded.tobytes())
        if response.ok:
            predictions = response.json()
            print(predictions)
            cv2.waitKey(10000)
        else:
            print(f"Request failed with status code {response.status_code}")
        break

    elif key == 27:  # press Esc to quit
        break

cap.release()
cv2.destroyAllWindows()

