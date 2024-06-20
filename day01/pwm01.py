# date : 2024-06-20
# file : pwm01.py
# desc : melody 함수에 들어있는 음향값을 순서대로 출력시킴
# 피에조소리 주파수 설정

import RPi.GPIO as GPIO
import time

piezoPin  = 13 # +에 연결 
melody = [130, 147, 165, 175, 196, 220, 247, 262 ]

GPIO.setmode(GPIO.BCM)
GPIO.setup(piezoPin, GPIO.OUT)


#아날로그 출력을 위한 객체생성(440HZ  출력)
Buzz = GPIO.PWM(piezoPin, 440)

try:
	while True:
		Buzz.start(50) #duty cycle:50
		for i in range(0, len(melody)):
			Buzz.ChangeFrequency(melody[i])
			time.sleep(0.3)
		Buzz.stop()
		time.sleep(1)

except KeyboardInterrupt:
	GPIO.cleanup()

