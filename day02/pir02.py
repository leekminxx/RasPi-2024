# date : 2024-06-21
# file : pir02.py
# desc : 센서가 작동되면 led 불이 켜짐

import RPi.GPIO as GPIO
import time

pirPin = 24
ledPin = 21

GPIO.setmode(GPIO.BCM)
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

