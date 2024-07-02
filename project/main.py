from PyQt5 import uic
from PyQt5.QtWidgets import *
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
        self.btnRed.clicked.connect(self.btnRedFunction)
        self.btnGreen.clicked.connect(self.btnGreenFunction)
        self.btnBlue.clicked.connect(self.btnBlueFunction)
        self.btnOff.clicked.connect(self.btnOffFunction)
        self.btnMeasureDistance.clicked.connect(self.btnMeasureDistanceFunction)
        self.btnStopMeasure.clicked.connect(self.btnStopMeasureFunction)

        # 초음파 측정을 위한 변수 초기화
        self.distance = 0.0
        self.measuring = False
        self.measure_thread = None

        # Buzz PWM 객체 초기화
        self.Buzz = GPIO.PWM(piezoPin, 440)

        # LCD 초기화
        self.lcdNumber.display(self.distance)

    def btnRedFunction(self):
        GPIO.output(redPin, False)
        GPIO.output(greenPin, True)
        GPIO.output(bluePin, True)

    def btnGreenFunction(self):
        GPIO.output(redPin, True)
        GPIO.output(greenPin, False)
        GPIO.output(bluePin, True)

    def btnBlueFunction(self):
        GPIO.output(redPin, True)
        GPIO.output(greenPin, True)
        GPIO.output(bluePin, False)

    def btnOffFunction(self):
        GPIO.output(redPin, True)
        GPIO.output(greenPin, True)
        GPIO.output(bluePin, True)

    def btnMeasureDistanceFunction(self):
        if not self.measuring:
            self.measuring = True
            self.measure_thread = threading.Thread(target=self.measureDistanceLoop)
            self.measure_thread.start()

    def btnStopMeasureFunction(self):
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

            # 거리에 따라 다른 소리 출력
            self.generateSound()

            # LCD에 거리 값 표시
            self.updateLCD()

    def generateSound(self):
        # 거리에 따라 다른 소리를 생성하는 함수
        if self.distance <= 5:
            self.Buzz.start(50)  # 부저 시작
            self.Buzz.ChangeFrequency(200)  # 주파수 변경
            time.sleep(0.1)  # 소리 지속 시간
            self.Buzz.ChangeFrequency(400)  # 주파수 변경
            time.sleep(0.1)  # 소리 지속 시간

        elif self.distance <= 10:
            self.Buzz.start(50)  # 부저 시작
            self.Buzz.ChangeFrequency(300)  # 주파수 변경
            time.sleep(0.5)  # 소리 지속 시간

        else:
            self.Buzz.stop()  # 부저 정지

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
