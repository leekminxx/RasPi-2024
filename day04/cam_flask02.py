from picamera2 import Picamera2, Preview
#from gpiozero import Button
import RPi.GPIO as GPIO
import time

#swPin = Button(16)
swPin = 6
oldSw = 0
newSw = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(swPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

try:
    while True:
        newSw = GPIO.input(swPin)
        if newSw != oldSw:
            oldSw = newSw

            if newSw == 1:
                print("Click")

        time.sleep(0.2)

except KeyboardInterrupt:
    pass
