# date : 2024-06-27
# file : segments06_2.py
# desc :

import RPi.GPIO as GPIO
import time
count = 0

fndData = [0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7d, 0x27, 0x7f, 0x6f]  # 0~9까지의 FND 데이터
fndSegs = [5, 6, 12, 16, 20, 13, 21]  # a~g LED 핀
fndSele = [4, 17, 27, 22]  # FND 선택 핀

# GPIO 설정
GPIO.setmode(GPIO.BCM)
for fndSeg in fndSegs:
    GPIO.setup(fndSeg, GPIO.OUT)
    GPIO.output(fndSeg, 0)
# FND 선택 핀 설정
for fndSel in fndSele:
    GPIO.setup(fndSel, GPIO.OUT)
    GPIO.output(fndSel, 1)  # 1로 초기화

def fndOut(data, sel):  # 하나의 숫자를 출력하는 함수
    for i in range(0, 7):
        GPIO.output(fndSegs[i], fndData[data] & (0x01 << i))
	for j in range(0, 2):         #표시할 자자리 수의 fnd만 on
	   if j == sel:
		GPIO.output(fndSels[j], 0)
	   else:
		GPIO.output(fndSels[j], 1)


try:
    while True:
	count += 1
	d1000 = count / 1000
	d100 = count % 100 / 100
	d10 = count % 100 / 10
	d1 = count % 10
	d = [d1, d10, d100 , d1000]

        for i in range(3,-1, -1):
#	    GPIO.output(6 , 1)
#	    GPIO.output(12, 1)
	   fndoOut(int(d[i]), i)  # d[i] 값을 정수로 변환하여 fndoOut 함수에 전달
	   time.sleep(0.3)

#            GPIO.output(fndSele[i], 1)  # FND 선택 해제
except KeyboardInterrupt:
    GPIO.cleanup()



