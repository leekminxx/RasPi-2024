# date : 2024-06-20
# file : inter01.py
# desc :  
import RPi.GPIO as GPIO
import time

#핀 설정
led = 21
switch = 6
#인터럽트 변수
intFlag = False

GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(switch, GPIO.IN)

def ledBlink(channel):
	global intFlag
		if intFlag  == False:
			 GPIO.output(led, True)
	 		 intFlag = True
	  else:
	  GPIO.output(led, False)
	  intFlag = False
#인터럽트 설정(switch 핀에 rising 신호가 잡히면 callback함수를 실행)
GPIO.add_event_detect(switch, GPIO.RISNG, callback=ledBlank)

try:
	while True:
		pass
except keyboardInterrupt:
	GPIO.cleanup()
