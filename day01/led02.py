# date : 2024-06-20
# file : led02.py
# desc : 자동으로 RGB값이 순서대로 나타남  

import RPi.GPIO as GPIO
import time

switch = 6
red_pin = 21 
green_pin = 16
blue_pin = 20
GPIO.cleanup()
GPIO.setmode(GPIO.BCM) # GPIO .BOARD(1~40)
GPIO.setup(red_pin, GPIO.OUT) #4pin output
GPIO.setup(green_pin, GPIO.OUT)
GPIO.setup(blue_pin, GPIO.OUT)

try:
    while (True):
        GPIO.output(red_pin, False)
        GPIO.output(green_pin, True)
        GPIO.output(blue_pin, True)
        time.sleep(0.5) #0.5sec // R

        GPIO.output(red_pin, True)
        GPIO.output(green_pin, False)
        GPIO.output(blue_pin, True)
        time.sleep(0.5) #0.5sec // G

        GPIO.output(red_pin, True)
        GPIO.output(green_pin, True)
        GPIO.output(blue_pin, False)
        time.sleep(0.5) #0.5sec // b

except KeyboardInterrupt:
    GPIO.cleanup()

