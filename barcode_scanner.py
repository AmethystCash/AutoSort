import cv2
from pyzbar.pyzbar import decode
from barcode_api import print_barcode_info

# all barcode

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while True:
    success, frame = cap.read()

    for code in decode(frame):
        # print(code.type)
        print_barcode_info(code.data.decode('utf-8'))
        cv2.waitKey(1000)
        

    cv2.imshow('Testing-code-scan', frame)
    cv2.waitKey(1)
    
