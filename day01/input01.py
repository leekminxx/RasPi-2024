# date : 2024-06-20
# file : input01.py
# desc : 스위치를 연결해서 누르면 pushed 가 출력


import RPi.GPIO as GPIO
import time

switch = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(switch, GPIO.IN)

try:
    while True:
        if GPIO.input(switch) == True:
            print("pushed")
            time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()
