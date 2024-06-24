# date : 2024-06-24
# file : relay01.py
# desc : 시그널 핸들링을통한 좀비 프로세스의 소멸

import RPi.GPIO as GPIO
import time

relayPin = 27  # 사용할 핀 번호

GPIO.setmode(GPIO.BCM)
GPIO.setup(relayPin, GPIO.OUT)

try:
    while True:
        GPIO.output(relayPin, 1)  # 릴레이 켜기
        time.sleep(1)  # 1초 대기
        GPIO.output(relayPin, 0)  # 릴레이 끄기
        time.sleep(1)  # 1초 대기

except KeyboardInterrupt:
    GPIO.cleanup()  # 프로그램 종료 시 GPIO 정리
