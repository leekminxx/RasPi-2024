# date : 2024-06-27
# file : segment06_1.py
# desc : 1에서 9까지 점점 증가하면서 자리수가 점점 늘어나는 코드




import RPi.GPIO as GPIO
import time

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

def fndOut(data):  # 하나의 숫자를 출력하는 함수
    for i in range(0, 7):
        GPIO.output(fndSegs[i], fndData[data] & (0x01 << i))

try:
    while True:
        for i in range(0, 4):
            GPIO.output(fndSele[i], 0)  # FND 선택
#	    GPIO.output(6 , 1)
#	    GPIO.output(12, 1)

            for j in range(0, 10):
                fndOut(j)  # 숫자 j를 FND에 출력
                time.sleep(0.5)

#            GPIO.output(fndSele[i], 1)  # FND 선택 해제
except KeyboardInterrupt:
    GPIO.cleanup()
