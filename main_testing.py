import gradio as gr
import time
import cv2
import threading
from colorama import Fore, Back, Style
from utils.ml import get_material
from utils.firebase import into_firebase
from utils.webhook import webhook_signal
from utils.doors import open_door, servo_setup
from utils.misc import rn_fancy, big_fancy_title4
from dotenv import load_dotenv
load_dotenv()

"""
testing the main.py file with a static image
"""
image_path = './testing-images/bottle.jpg'



# THE SETUP
print(big_fancy_title4)
print(Fore.MAGENTA + "\n===== SETUP STARTING =====\n" + Style.RESET_ALL)

def load_server(server_loaded_event):
    gr.Interface.load("models/yangy50/garbage-classification")
    server_loaded_event.set()

server_loaded_event = threading.Event()
interface_thread = threading.Thread(target=load_server, args=(server_loaded_event,))
interface_thread.start()

print(Fore.YELLOW + "Waiting for server to load..." + Style.RESET_ALL)
server_loaded_event.wait()
print(Fore.GREEN + "Server has loaded successfully!\n" + Style.RESET_ALL)

# servo angles setup
servo_setup()

print(Fore.MAGENTA + "\n===== SETUP DONE =====\n" + Style.RESET_ALL)



# THE MAIN LOOP
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
            'datetime': rn_fancy(),
            'img_bytes': img_bytes
        }
        
        open_door(material)
        webhook_signal(data)
        into_firebase(data)
        print("")

    elif key == 27:  # press Esc to quit
        break

cv2.destroyAllWindows()