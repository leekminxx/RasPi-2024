# date : 2024-06-21
# file : pir02.py
# desc : 센서가 작동되면 led 불이 켜짐

import RPi.GPIO as GPIO
import time

pirPin = 24
ledPin = 21

GPIO.setmode(GPIO.BCM)
# GPIO.setup(pirPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
# 해당 핀의 풀다운 저항을 활성화
# 풀다운 저항을 활성화하면 핀이 부동 상태일 때(센서가 신호를 보내지 않을 때) 핀의 상태가 기본적으로 LOW(0)가 됨
GPIO.setup(pirPin, GPIO.IN)
GPIO.setup(ledPin , GPIO.OUT)

GPIO.output(ledPin, GPIO.HIGH)  

try:
	while True:
		if GPIO.input(pirPin) == True:
			print("check")
			GPIO.output(ledPin, GPIO.LOW) # 켜기
			time.sleep(0.2)
		else:
			GPIO.output(ledPin, GPIO.HIGH)
		time.sleep(0.1)
except KeyboardInterrupt:
	GPIO.cleanup()

