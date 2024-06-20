# date : 2024-06-20
# file : pwm02.py
# desc : input 입력값을 받아서 melody 함수에 있는 값을호출하고 출력하여 소리를 재생

import RPi.GPIO as GPIO
import time

piezoPin = 13  

# 주파수 리스트
melody = [130, 147, 165, 175, 196, 220, 247, 262]

GPIO.setmode(GPIO.BCM)
GPIO.setup(piezoPin, GPIO.OUT)

# 아날로그 출력을 위한 객체 생성 (초기 주파수는 임의로 설정)
Buzz = GPIO.PWM(piezoPin, 440)

try:
    while True:
        user_input = input("1~8까지 입력 ").strip().lower()

        if user_input.isdigit():
            note_index = int(user_input) - 1

            if 0 <= note_index < len(melody):
                Buzz.start(50)  # duty cycle: 50%
                Buzz.ChangeFrequency(melody[note_index])
                time.sleep(0.5)  # 음을 0.5초 동안 재생
                Buzz.stop()
                time.sleep(0.1)  # 음 사이에 약간의 대기시간
            else:
                print(".")
        else:
            print(".")

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
