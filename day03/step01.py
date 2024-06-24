# date : 2024-06-24
# file : step01.py
# desc : 시그널 핸들링을통한 좀비 프로세스의 소멸

import RPi.GPIO as GPIO
import time

steps = [21, 20, 16, 26]
GPIO.setmode(GPIO.BCM)

for step in steps:
    GPIO.setup(step, GPIO.OUT)
    GPIO.output(step, 0)

try:
    while True:
        GPIO.output(steps[0], 1)
        GPIO.output(steps[1], 0)
        GPIO.output(steps[2], 0)
        GPIO.output(steps[3], 0)
        time.sleep(0.01)

        GPIO.output(steps[0], 0)
        GPIO.output(steps[1], 1)
        GPIO.output(steps[2], 1)
        GPIO.output(steps[3], 0)
        time.sleep(0.01)

        GPIO.output(steps[0], 0)
        GPIO.output(steps[1], 1)
        GPIO.output(steps[2], 1)
        GPIO.output(steps[3], 1)
        time.sleep(0.01)

        GPIO.output(steps[0], 0)
        GPIO.output(steps[1], 0)
        GPIO.output(steps[2], 0)
        GPIO.output(steps[3], 1)
        time.sleep(0.01)

except KeyboardInterrupt:
    GPIO.cleanup()
