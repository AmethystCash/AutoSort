import gradio as gr
import time
import cv2
import threading
import datetime
from utils.ml import get_material
from utils.firebase import into_firebase
from utils.webhook import webhook_signal
from utils.doors import open_door
from dotenv import load_dotenv
load_dotenv()

"""
testing the main.py file with a static image
"""
image_path = './testing-images/paper.jpeg'



# setup
def load_server(server_loaded_event):
    gr.Interface.load("models/yangy50/garbage-classification")
    server_loaded_event.set()

server_loaded_event = threading.Event()
interface_thread = threading.Thread(target=load_server, args=(server_loaded_event,))
interface_thread.start()

print("waiting for server to load...")
server_loaded_event.wait()
print("server has loaded successfully!")



# main loop
while True:
    frame = cv2.imread(image_path)
    cv2.imshow('frame', frame)

    key = cv2.waitKey(1)
    if key == ord(' '):  # pretend that pressing SPACE is like throwing the trash in
        time.sleep(1)  # wait 1 sec for the trash to fall in
 
        _, img_encoded = cv2.imencode('.jpg', frame)
        img_bytes = img_encoded.tobytes()
        material, certainty = get_material(img_bytes)

        data = {
            'material': material,
            'certainty': certainty,
            'datetime': time.strftime("%X %x"), # format: hr:min:sec dd/mm/yy
            'img_bytes': img_bytes
        }
        
        open_door(material)
        webhook_signal(data)
        into_firebase(data)
        # that's why we need async

    elif key == 27:  # press Esc to quit
        break

cv2.destroyAllWindows()