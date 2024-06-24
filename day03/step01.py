# date : 2024-06-24
# file : step01.py
# desc : 스테퍼모터제어를 위한 모터드라이버 코드
import RPi.GPIO as GPIO
import time

steps = [21, 20, 16, 26]
GPIO.setmode(GPIO.BCM)

for step in steps:
    GPIO.setup(step, GPIO.OUT)
    GPIO.output(step, 0)

try:
    while True:
        GPIO.output(steps[0], 1) #핀을 HIGH로 설정하고 나머지 핀들을 LOW로 설정하면서 첫 번째 스텝을 활성화
        GPIO.output(steps[1], 0) #LOW(0) 모터를 반시계방향으로
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
