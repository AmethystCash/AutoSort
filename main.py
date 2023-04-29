import gradio as gr
import time
import cv2
import threading
from utils import get_material, into_firebase, open_door
from dotenv import load_dotenv
load_dotenv()

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
6. you send that info to firebase
7. you open a door

the only files we have to worry about now are:
- main.py - the program runs here
- utils.py - contains the object recognition, firebase and door functions
- main_testing.py - testing with static images



--Remarks--

rn the firebase/door functions both just print stuff to the console
feel free to edit them to your liking
and feel free to edit the data format in the main loop too

I don't know how to incorporate the barcode reader into this
but if we want to do that we can just create a function for that in utils.py and then use it here

sometimes it might take longer for the object recognition model to load
even if it says it's done loading
I'm not sure how to solve this yet
but it shouldn't be a big issue since it only happens at the start
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

        image_path = './testing-images/bottle.jpg'
        frame = cv2.imread(image_path)
        material, certainty = get_material(frame)
        
        # get other potential info, like time, or even the img itself
        data = {
            'material': material,
            'certainty': certainty
            # idk what else do you want to be sent or in what format but feel free to edit this part
        }
        
        open_door(material)
        into_firebase(data)

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