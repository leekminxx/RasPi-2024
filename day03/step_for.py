# date : 2024-06-24
# file : step_for.py
# desc : for 문을 이용한 모터드라이버 코드

import RPi.GPIO as GPIO
import time

steps = [21, 20, 16, 26]
GPIO.setmode(GPIO.BCM)

for step in steps:
    GPIO.setup(step, GPIO.OUT)
    GPIO.output(step, 0)

try:
    while True:
        for i in range(4):
            for j in range(4):
                GPIO.output(steps[j], 1 if i == j else 0)
            time.sleep(0.01)

except KeyboardInterrupt:
    GPIO.cleanup()
