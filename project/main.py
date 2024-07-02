from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QPalette, QFont
import sys
import RPi.GPIO as GPIO
import time
import threading

redPin = 25
greenPin = 5
bluePin = 6
piezoPin = 21
trigPin = 20
echoPin = 16

# 초음파 센서와 부저 관련 변수 및 상수
speedOfSound = 34300  # 음속 (cm/s)

GPIO.setmode(GPIO.BCM)
GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)
GPIO.setup(bluePin, GPIO.OUT)
GPIO.setup(piezoPin, GPIO.OUT)
GPIO.setup(trigPin, GPIO.OUT)
GPIO.setup(echoPin, GPIO.IN)

# Qt에서 만든 UI 파일을 로드합니다.
form_class = uic.loadUiType("./main.ui")[0]

# 윈도우 클래스 정의
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()  # 부모 클래스의 생성자(QMainWindow)를 호출합니다.
        self.setupUi(self)  # UI를 설정합니다.
        # 이벤트 함수 등록
        self.btnRed.clicked.connect(lambda: self.setLED("red"))
        self.btnGreen.clicked.connect(lambda: self.setLED("green"))
        self.btnBlue.clicked.connect(lambda: self.setLED("blue"))
        self.btnOff.clicked.connect(lambda: self.setLED("off"))
        self.btnMeasureDistance.clicked.connect(self.startMeasurement)
        self.btnStopMeasure.clicked.connect(self.stopMeasurement)

        # 초음파 측정을 위한 변수 초기화
        self.distance = 0.0
        self.measuring = False
        self.measure_thread = None

        # Buzz PWM 객체 초기화
        self.Buzz = GPIO.PWM(piezoPin, 440)

        # LCD 초기화
        self.lcdNumber.display(self.distance)

        # labelLED 초기 텍스트 설정
        self.labelLED.setText("LED Color Status")

        # labelLED 텍스트 크기 설정
        font = QFont()
        font.setPointSize(16)  # 원하는 크기로 설정
        self.labelLED.setFont(font)

    def setLED(self, color):
        if color == "red":
            GPIO.output(redPin, False)
            GPIO.output(greenPin, True)
            GPIO.output(bluePin, True)
            self.updateLEDLabel(QColor(255, 0, 0))
        elif color == "green":
            GPIO.output(redPin, True)
            GPIO.output(greenPin, False)
            GPIO.output(bluePin, True)
            self.updateLEDLabel(QColor(0, 255, 0))
        elif color == "blue":
            GPIO.output(redPin, True)
            GPIO.output(greenPin, True)
            GPIO.output(bluePin, False)
            self.updateLEDLabel(QColor(0, 0, 255))
        elif color == "off":
            GPIO.output(redPin, True)
            GPIO.output(greenPin, True)
            GPIO.output(bluePin, True)
            self.updateLEDLabel(QColor(0, 0, 0))

    def updateLEDLabel(self, color):
        palette = self.labelLED.palette()
        palette.setColor(self.labelLED.foregroundRole(), color)
        self.labelLED.setPalette(palette)

    def startMeasurement(self):
        if not self.measuring:
            self.measuring = True
            self.measure_thread = threading.Thread(target=self.measureDistanceLoop)
            self.measure_thread.start()

    def stopMeasurement(self):
        self.measuring = False
        if self.measure_thread:
            self.measure_thread.join()
        GPIO.output(trigPin, False)  # 초음파 발신 핀을 끕니다.

    def measureDistanceLoop(self):
        while self.measuring:
            GPIO.output(trigPin, True)
            time.sleep(0.00001)
            GPIO.output(trigPin, False)

            startTime = time.time()
            stopTime = time.time()

            while GPIO.input(echoPin) == 0:
                startTime = time.time()

            while GPIO.input(echoPin) == 1:
                stopTime = time.time()

            deltaTime = stopTime - startTime
            self.distance = (deltaTime * speedOfSound) / 2

            # 거리에 따라 LED와 부저 제어
            self.controlLEDAndBuzz()

            # LCD에 거리 값 표시
            self.updateLCD()

    def controlLEDAndBuzz(self):
        if self.distance <= 5:
            # 빨간불 깜빡임 및 소리
            GPIO.output(redPin, False)
            time.sleep(0.1)
            GPIO.output(redPin, True)
            time.sleep(0.1)
            self.Buzz.start(50)
            self.Buzz.ChangeFrequency(200)
        elif self.distance <= 10:
            # 초록불 켜기 및 소리
            GPIO.output(greenPin, False)
            GPIO.output(redPin, True)
            self.Buzz.start(50)
            self.Buzz.ChangeFrequency(300)
        else:
            # 모든 불 끄기 및 부저 정지
            GPIO.output(redPin, True)
            GPIO.output(greenPin, True)
            self.Buzz.stop()

    def updateLCD(self):
        # LCD에 거리 값을 업데이트하는 함수
        self.lcdNumber.display(self.distance)

    def closeEvent(self, event):
        # 종료 시 GPIO 정리
        GPIO.cleanup()

if __name__ == "__main__":
    app = QApplication(sys.argv)  # QApplication 객체를 생성합니다.
    myWindow = WindowClass()      # WindowClass의 인스턴스를 생성합니다.
    myWindow.show()               # 윈도우를 화면에 보이도록 설정합니다.
    app.exec_()                   # 이벤트 루프를 실행합니다.