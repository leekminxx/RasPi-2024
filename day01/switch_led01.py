# date : 2024-06-20
# file : switch_led01.py
# desc : 스위치를 눌러서 RGB의 값을변경
import RPi.GPIO as GPIO
import time

switch = 6

red_led = 21
green_led = 20
blue_led = 16

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(red_led , GPIO.OUT)
GPIO.setup(green_led, GPIO.OUT)
GPIO.setup(blue_led, GPIO.OUT)
GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)


try:
	while True:
		if GPIO.input(switch) == True:
			GPIO.output(green_led, False)
			GPIO.output(red_led, True)
			GPIO.output(blue_led, True)
			time.sleep(0.5)

		if GPIO.input(switch) == True:
			GPIO.output(green_led, True)
			GPIO.output(red_led, False)
			GPIO.output(blue_led, True)
			time.sleep(0.5)

		if GPIO.input(switch) == True:
			GPIO.output(red_led, True)
			GPIO.output(green_led, True)
			GPIO.output(blue_led, False)
			time.sleep(0.5)

except KeyboardInterrupt:
		GPIO.cleanup()
