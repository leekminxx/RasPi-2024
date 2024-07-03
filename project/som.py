from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QColor
import sys
import RPi.GPIO as GPIO
import time

# GPIO 설정
red = 25
green = 19
blue = 26
piezoPin = 4
trigPin = 27
echoPin = 17

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)
GPIO.setup(piezoPin, GPIO.OUT)
GPIO.setup(trigPin, GPIO.OUT)
GPIO.setup(echoPin, GPIO.IN)

# Qt에서 만든 UI 파일을 로드합니다.
form_class = uic.loadUiType("./btn01.ui")[0]

# 윈도우 클래스 정의
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()  # 부모 클래스의 생성자(QMainWindow)를 호출합니다.
        self.setupUi(self)  # UI를 설정합니다.
        # 이벤트 함수 등록
        self.btnRed.clicked.connect(self.btnRedFunction)
        self.btnBlue.clicked.connect(self.btnBlueFunction)
        self.btnGreen.clicked.connect(self.btnGreenFunction)

    def btnRedFunction(self):
        GPIO.output(red, False)
        GPIO.output(green, True)
        GPIO.output(blue, True)

    def btnBlueFunction(self):
        GPIO.output(red, True)
        GPIO.output(green, True)
        GPIO.output(blue, False)
        
    def btnGreenFunction(self):
        GPIO.output(red, True)
        GPIO.output(green, False)
        GPIO.output(blue, True)

if __name__ == "__main__":
    app = QApplication(sys.argv)  # QApplication 객체를 생성합니다.
    myWindow = WindowClass()      # WindowClass의 인스턴스를 생성합니다.
    myWindow.show()               # 윈도우를 화면에 보이도록 설정합니다.
    app.exec_()                   # 이벤트 루프를 실행합니다.