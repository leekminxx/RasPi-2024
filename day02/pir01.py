# date : 2024-06-21
# file : pir01.py
# desc : pir센서 손을 가져다 대면 True일떄 프린트문 출력

import RPi.GPIO as GPIO
import time

pirPin = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(pirPin, GPIO.IN)

try:
    while True:
        if GPIO.input(pirPin) == True:
            print("Detected")
            time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()
