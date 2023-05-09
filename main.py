import gradio as gr
import time
import cv2
import threading
from utils.ml import get_material
from utils.firebase import into_firebase
from utils.webhook import webhook_signal
from utils.doors import open_door
from utils.misc import rn_fancy
from dotenv import load_dotenv
load_dotenv()

from gpiozero import AngularServo
from time import sleep
servo =AngularServo(18, min_angle=0, max_angle=180, min_pulse_width=0.0005, max_pulse_width=0.0025)
servo2 =AngularServo(17, min_angle=0, max_angle=180, min_pulse_width=0.0005, max_pulse_width=0.0025)


"""
hi guys

this is a code revamp done on 29/04/2023
hopefully now it's easier to understand and work with



--Essential info--

currently the thing works like this:
1. load the object recognition model
2. start the main loop
3. you press space (pretend that that means throwing a piece of trash into the bin)
4. that triggers the object recognition model to run on the current frame
5. you get back packaging info
6. you send that info to firebase and discord
7. you open a door

the only files we have to worry about now are:
- main.py - the program runs here
- main_testing.py - testing with static images
- utils:
    - ml.py - object recognition model
    - firebase.py - firebase stuff
    - webhook.py - discord webhook stuff
    - doors.py - door opening stuff
    - misc.py - helper functions



--Remarks--

rn the door function just prints stuff to the console, to be edited later

I don't know how to incorporate the barcode reader into this
but if we want to do that we can just create a function for that in `utils` and then use it here

sometimes it might take longer for the object recognition model to load
even if it says it's done loading
I'm not sure how to solve this yet
but it shouldn't be a big issue since it only happens at the start

the repo was cleaned up recently
the old files (such as the barcode scanner) are in the `legacy-code` directory
the readme will be updated soon to reflect this
"""



# THE SETUP
def load_server():
    gr.Interface.load("models/yangy50/garbage-classification")
    return True 

interface_thread = threading.Thread(target=load_server)
interface_thread.start()

print("starting server loading...")
while True:
    if interface_thread.is_alive():
        print("waiting...")
        time.sleep(1)
    else:
        print("server has loaded successfully!")
        break

#setting servo angles
servo.angle = 140
servo2.angle = 140

#starting camera
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)



# THE MAIN LOOP
while True:
    success, frame = cap.read()
    cv2.imshow('frame', frame)

    key = cv2.waitKey(1)
    if key == ord(' '):  # press SPACE (pretend that pressing SPACE is like throwing the trash in)
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
        
        #open_door(material)

        if(material == 'plastic'):
            servo2.angle = 70
            sleep(5)
            servo2.angle = 140
             
        elif (material == 'paper'):
            servo.angle = 70
            sleep(5)
            servo.angle = 140
            
        webhook_signal(data)
        into_firebase(data)
        # that's why we need async (this takes a while of waiting)

    elif key == 27:  # press Esc to quit
        break

cap.release()
cv2.destroyAllWindows()
    













# old relics below

"""
import gradio as gr

gr.Interface.load("models/yangy50/garbage-classification").launch()
# if ml_scanner.py doesn't work, execute this, that usually fixes it after a few seconds
"""

"""
To see the barcode mechanism in action, run barcode_scanner.py

To see the machine learning mechanism in action, run ml_scanner.py
"""
