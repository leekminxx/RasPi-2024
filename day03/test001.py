import RPi.GPIO as GPIO
import time

steps = [21 , 20, 16, 26]
GPIO.setmode(GPIO.BCM)

for step in steps:
	GPIO.setup(step, GPIO.OUT)
	GPIO.output(step, 0)

try:
	while True:
		for i in range(4)
			for j in rnage(4)
				GPIO.output(steps[j], i if i == j else 0)
			time.sleep(0.01)
		
