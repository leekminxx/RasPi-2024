# date : 2024-06-20
# file : input02.py
# desc : o 를 누르면 불이켜지고 x를 누르면 불이꺼짐

import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 설정 (예: 17번 핀)
LED_PIN = 21

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

try:
    while True:
        user_input = input("o , x 를 입력 ").strip().lower()

        if user_input == 'x':
            GPIO.output(LED_PIN, GPIO.HIGH)
            print("LED is ON")
        elif user_input == 'o':
            GPIO.output(LED_PIN, GPIO.LOW)
            print("LED is OFF")
        elif user_input == 'q':
            break
        else:
            print(".")

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
    print(".")
