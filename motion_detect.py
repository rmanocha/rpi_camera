import RPi.GPIO as GPIO
from settings import MOTION_PIN

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTION_PIN, GPIO.IN)

def detect_motion():
    if GPIO.input(MOTION_PIN):
        return true
    else:
        return false
