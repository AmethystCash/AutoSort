import requests
import os
from dotenv import load_dotenv
import cv2
load_dotenv()

trash_mapper = {
    'paper': 'Paper',
    'cardboard': 'Paper',
    'metal': 'Plastic',
    'plastic': 'Plastic',
    'glass': 'Glass',
    'trash': 'Misc',
}

API_URL = "https://api-inference.huggingface.co/models/yangy50/garbage-classification"
headers = {"Authorization": f"Bearer {os.getenv('API_KEY')}"}


# the function that tells us what material the object is made of

def get_material(frame):
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
    
    
    
# the firebase push function

def into_firebase(data):
    
    most_recent = time.strftime("%X %x")
    package_num = ref.child(data).child("Total").get() # The value of the 'Total' key
    package_num += 1
    package_up = {"Total": package_num, "Time of Most Recent": most_recent}
    ref.child(data).update(package_up) # Updates total and time
    
    print(ref.child(data).get())  # Prints the material data for testing purposes
    
    

# the door opening function

def open_door(material):
    door_mapper = {
        'Plastic': 1,
        'Glass': 2,
        'Paper': 3,
        'Misc': 4,
    }
    # you can use either this or some if/else
    
    print(f"opening the {material} door with number {door_mapper[material]}")
