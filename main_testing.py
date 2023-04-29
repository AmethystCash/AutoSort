import gradio as gr
import time
import cv2
import threading
from utils import get_material, into_firebase, open_door
from dotenv import load_dotenv
load_dotenv()

"""
testing the main.py file with a static image
"""
image_path = './testing-images/bottle.jpg'



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
 
        material, certainty = get_material(frame)
        
        # get other potential info, like time, or even the img itself
        data = {
            'material': material,
            'certainty': certainty
            # idk what else do you want to be sent or in what format but feel free to edit this part
        }
        
        into_firebase(data)
        open_door(material)

    elif key == 27:  # press Esc to quit
        break

cv2.destroyAllWindows()