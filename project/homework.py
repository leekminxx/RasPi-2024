# from PyQt5.QtWidgets import *
# from PyQt5 import uic
# from PyQt5.QtCore import QTimer
# import sys
# import RPi.GPIO as GPIO
# import time

# red = 25
# green = 19
# blue = 26
# piezoPin = 17
# trigPin = 27
# echoPin = 4

# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(red, GPIO.OUT)
# GPIO.setup(green, GPIO.OUT)
# GPIO.setup(blue, GPIO.OUT)
# GPIO.setup(piezoPin, GPIO.OUT)

# form_class = uic.loadUiType("led.ui")[0]

# class WindowClass(QMainWindow, form_class):
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)
#         self.btn_2.clicked.connect(self.turnOffLED)
#         self.btn1_r.clicked.connect(self.turnOnRed)
#         self.btn1_g.clicked.connect(self.turnOnGreen)
#         self.btn1_b.clicked.connect(self.turnOnBlue)
#         self.btn_switch.clicked.connect(self.toggleCycling)

#         self.label_led.setText("check")

#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.cycleColors)
#         self.cycling = False
#         self.current_color_index = 0
#         self.colors = [self.turnOnRed, self.turnOnGreen, self.turnOnBlue]

#         self.distance_timer = QTimer(self)
#         self.distance_timer.start(1000)

#         # �ʱ� ���¿��� LED�� ���ݴϴ�.
#         self.turnOffLED()

#     def turnOnRed(self):
#         GPIO.output(red, False)
#         GPIO.output(green, True)
#         GPIO.output(blue, True)
#         self.updateLabel("Red")

#     def turnOnGreen(self):
#         GPIO.output(red, True)
#         GPIO.output(green, False)
#         GPIO.output(blue, True)
#         self.updateLabel("Green")

#     def turnOnBlue(self):
#         GPIO.output(red, True)
#         GPIO.output(green, True)
#         GPIO.output(blue, False)
#         self.updateLabel("Blue")

#     def turnOffLED(self):
#         self.timer.stop()
#         self.cycling = False
#         GPIO.output(red, True)
#         GPIO.output(green, True)
#         GPIO.output(blue, True)
#         self.updateLabel("")

#     def toggleCycling(self):
#         if self.cycling:
#             self.timer.stop()
#         else:
#             self.timer.start(1000)
#             self.cycleColors()
#             self.cycling = not self.cycling

#     def cycleColors(self):
#         self.colors[self.current_color_index]()
#         self.current_color_index = (self.current_color_index + 1) % len(self.colors)

#     def updateLabel(self, color_name):
#         self.label_led.setText(color_name)

#     def closeEvent(self, event):
#         self.timer.stop()
#         self.distance_timer.stop()
#         GPIO.cleanup()
#         event.accept()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     myWindow = WindowClass()
#     myWindow.show()
#     app.exec_()

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QTimer
import sys
import RPi.GPIO as GPIO

red = 25
green = 19
blue = 26
piezoPin = 4

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)
GPIO.setup(piezoPin, GPIO.OUT)

# PWM 객체 생성
pwm_red = GPIO.PWM(red, 100)  # Red LED, 100 Hz 주파수로 PWM 객체 생성
pwm_green = GPIO.PWM(green, 100)  # Green LED, 100 Hz 주파수로 PWM 객체 생성
pwm_blue = GPIO.PWM(blue, 100)  # Blue LED, 100 Hz 주파수로 PWM 객체 생성

form_class = uic.loadUiType("led.ui")[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_2.clicked.connect(self.turnOffLED)
        self.btn1_r.clicked.connect(self.turnOnRed)
        self.btn1_g.clicked.connect(self.turnOnGreen)
        self.btn1_b.clicked.connect(self.turnOnBlue)
        self.btn_switch.clicked.connect(self.toggleCycling)
        self.btn_sound.clicked.connect(self.togglePiezo)
        
        # 다이얼 값 변경 시그널 연결
        self.dial_led.valueChanged.connect(self.dialValueChanged)

        self.label_led.setText("확인")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.cycleColors)
        self.cycling = False
        self.current_color_index = 0
        self.colors = [self.turnOnRed, self.turnOnGreen, self.turnOnBlue]

        self.distance_timer = QTimer(self)
        self.distance_timer.start(1000)

        # LED가 꺼진 상태에서 시작하도록 설정
        self.turnOffLED()

    def turnOnRed(self):
        GPIO.output(red, GPIO.LOW)
        GPIO.output(green, GPIO.HIGH)
        GPIO.output(blue, GPIO.HIGH)
        self.updateLabel("Red")

    def turnOnGreen(self):
        GPIO.output(red, GPIO.HIGH)
        GPIO.output(green, GPIO.LOW)
        GPIO.output(blue, GPIO.HIGH)
        self.updateLabel("Green")

    def turnOnBlue(self):
        GPIO.output(red, GPIO.HIGH)
        GPIO.output(green, GPIO.HIGH)
        GPIO.output(blue, GPIO.LOW)
        self.updateLabel("Blue")

    def turnOffLED(self):
        self.timer.stop()
        self.cycling = False
        GPIO.output(red, GPIO.HIGH)
        GPIO.output(green, GPIO.HIGH)
        GPIO.output(blue, GPIO.HIGH)
        self.updateLabel("")

    def toggleCycling(self):
        if self.cycling:
            self.timer.stop()
        else:
            self.timer.start(1000)
            self.cycleColors()
            self.cycling = not self.cycling

    def cycleColors(self):
        self.colors[self.current_color_index]()
        self.current_color_index = (self.current_color_index + 1) % len(self.colors)

    def dialValueChanged(self, value):
        # 다이얼 값을 0-100에서 0-100으로 스케일 조정하여 밝기를 설정합니다.
        brightness = int(value)

        if self.current_color_index == 0:
            # Red LED
            pwm_red.start(brightness)
            pwm_green.stop()
            pwm_blue.stop()
        elif self.current_color_index == 1:
            # Green LED
            pwm_green.start(brightness)
            pwm_red.stop()
            pwm_blue.stop()
        elif self.current_color_index == 2:
            # Blue LED
            pwm_blue.start(brightness)
            pwm_red.stop()
            pwm_green.stop()

        # Update label to show intensity
        self.updateLabel(f"강도: {brightness}")

    def togglePiezo(self):
        # 피에조 부저를 토글하는 함수
        if GPIO.input(piezoPin) == GPIO.LOW:
            GPIO.output(piezoPin, GPIO.HIGH)
            self.btn_sound.setText("부저 끄기")
        else:
            GPIO.output(piezoPin, GPIO.LOW)
            self.btn_sound.setText("부저 켜기")

    def updateLabel(self, color_name):
        self.label_led.setText(color_name)

    def closeEvent(self, event):
        self.timer.stop()
        self.distance_timer.stop()
        GPIO.cleanup()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()





