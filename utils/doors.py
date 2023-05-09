from gpiozero import AngularServo
from time import sleep
from colorama import Fore, Back, Style

# NOTE:
# currently this script works no matter if you have a servo connected or not

# TODO:
# improve this code one day when we get more servos (or when I feel like it)
# too many prints
# better func for better setup
# async


try:
    servo1 = AngularServo(18, min_angle=0, max_angle=180, min_pulse_width=0.0005, max_pulse_width=0.0025)
    servo2 = AngularServo(17, min_angle=0, max_angle=180, min_pulse_width=0.0005, max_pulse_width=0.0025)
except:
    servo1 = None
    servo2 = None
    print(Fore.RED + "No servos connected" + Style.RESET_ALL)


def servo_setup():
    print(Fore.YELLOW + "Setting up servos..." + Style.RESET_ALL)
    try:
        servo1.angle = 140
        servo2.angle = 140
        print(Fore.GREEN + "Servo setup complete!" + Style.RESET_ALL)
    except:
        print(Fore.RED + "Servo setup failed" + Style.RESET_ALL)


def open_door(material):
    servo_mapper = {
        'plastic': servo2,
        'glass': None,  # update in the future with another servo
        'paper': servo1,
        'misc': None,  # update in the future with another servo
    }
    
    if material not in servo_mapper:
        print(Fore.RED + f"Invalid material: '{material}'" + Style.RESET_ALL)
        return
        
    servo = servo_mapper[material]
    if servo is None:
        print(Fore.RED + f"No servo available for '{material}'" + Style.RESET_ALL)
        return
    
    try:
        print(Fore.GREEN + f"Opening the '{material}' door using {servo} (pin {servo.pin})" + Style.RESET_ALL)
        servo.angle = 70
        sleep(5)
        servo.angle = 140
        print(Fore.GREEN + f"'{material}' door is closed" + Style.RESET_ALL)
    except:
        print(Fore.RED + f"Failed to open/close '{material}' door" + Style.RESET_ALL)