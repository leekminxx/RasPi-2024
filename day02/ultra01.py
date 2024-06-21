# date : 2024-06-21
# file : ultra01.py
# desc : Ultra 초음파 센서 코드 피에조 부조랑 연결하여 거리가 가까울수록 소리를 출력

import RPi.GPIO as GPIO  # 10us 동안 high 레벨을 가지고 trigger 출력하기 위해
import time

def measure():
    GPIO.output(trigPin, True)
    time.sleep(0.00001)
    GPIO.output(trigPin, False)

    start = time.time()  # 현재 시간 저장
    while GPIO.input(echoPin) == False:  # echo가 없으면
        start = time.time()  # 현재 시간을 start 변수에 저장
    while GPIO.input(echoPin) == True:  # echo가 있으면
        stop = time.time()  # 현재 시간을 stop 변수에 저장

    elapsed = stop - start  # 걸린 시간을 구하고
    distance = (elapsed * 19000) / 2  # 초음파 속도를 이용해서 거리 계산 (m/s)

    return distance  # 거리 반환

# 핀 설정
trigPin = 16
echoPin = 20
piezoPin = 13
ledPin = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(trigPin, GPIO.OUT)
GPIO.setup(echoPin, GPIO.IN)
GPIO.setup(piezoPin, GPIO.OUT)
GPIO.setup(ledPin, GPIO.OUT)

Buzz = GPIO.PWM(piezoPin, 440)

try:
	while True:
		distance = measure()
		print("Distance: %.2f cm" % distance)

		if distance <= 5:
				Buzz.start(50)
				Buzz.ChangeFrequency(200)
				time.sleep(0.1)
				GPIO.output(ledPin,False)
				Buzz.ChangeFrequency(400)
				time.sleep(0.1)
		elif distance <=15:
				Buzz.start(50)
				Buzz.ChangeFrequency(300)
				time.sleep(0.3)
				Buzz.stop()
				time.sleep(0.3)
		elif distance <=30:
				Buzz.start(50)
				Buzz.ChangeFrequency(400)
				time.sleep(0.6)
				Buzz.stop()
				time.sleep(0.6)
		else:
				Buzz.stop()
				time.sleep(0.1)
		GPIO.output(ledPin,True)
		time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
