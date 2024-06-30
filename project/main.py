from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QTimer
import sys
import RPi.GPIO as GPIO
import time

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
pwm_red = GPIO.PWM(red, 100)  # Red LED, 100 Hz PWM 객체 생성
pwm_green = GPIO.PWM(green, 100)  # Green LED, 100 Hz PWM 객체 생성
pwm_blue = GPIO.PWM(blue, 100)  # Blue LED, 100 Hz PWM 객체 생성

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
        self.btn_song1.clicked.connect(self.playSong1)
        self.btn_song2.clicked.connect(self.playSong2)
        self.btn_song3.clicked.connect(self.playSong3)
        self.btn_song4.clicked.connect(self.playSong4)
        
        self.dial_led.valueChanged.connect(self.dialValueChanged)
        self.dial_sound.valueChanged.connect(self.dialSoundChanged)

        self.label_led.setText("LED 꺼짐")
        self.label_sound = QLabel(self)  # 라벨 생성
        self.label_sound.setText("0")  # 초기에 라벨에 0 표시
        self.label_sound.move(20, 220)  # 위치 조정

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.cycleColors)
        self.cycling = False
        self.current_color_index = 0
        self.colors = [self.turnOnRed, self.turnOnGreen, self.turnOnBlue]

        self.distance_timer = QTimer(self)
        self.distance_timer.start(1000)

        self.buzzer_on = False
        self.pwm_buzzer = None
        self.turnOffLED()

    def turnOnRed(self):
        GPIO.output(red, GPIO.LOW)
        GPIO.output(green, GPIO.HIGH)
        GPIO.output(blue, GPIO.HIGH)
        self.updateLabel("빨간색")

    def turnOnGreen(self):
        GPIO.output(red, GPIO.HIGH)
        GPIO.output(green, GPIO.LOW)
        GPIO.output(blue, GPIO.HIGH)
        self.updateLabel("초록색")

    def turnOnBlue(self):
        GPIO.output(red, GPIO.HIGH)
        GPIO.output(green, GPIO.HIGH)
        GPIO.output(blue, GPIO.LOW)
        self.updateLabel("파란색")

    def turnOffLED(self):
        self.timer.stop()
        self.cycling = False
        GPIO.output(red, GPIO.HIGH)
        GPIO.output(green, GPIO.HIGH)
        GPIO.output(blue, GPIO.HIGH)
        self.updateLabel("LED 꺼짐")

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
        brightness = int(value)

        if self.current_color_index == 0:
            pwm_red.start(brightness)
            pwm_green.stop()
            pwm_blue.stop()
        elif self.current_color_index == 1:
            pwm_green.start(brightness)
            pwm_red.stop()
            pwm_blue.stop()
        elif self.current_color_index == 2:
            pwm_blue.start(brightness)
            pwm_red.stop()
            pwm_green.stop()

        self.updateLabel(f"밝기: {brightness}")

    def dialSoundChanged(self, value):
        volume = int(value)

        if self.pwm_buzzer is None:
            self.pwm_buzzer = GPIO.PWM(piezoPin, 1000)  # 1kHz PWM 객체 생성
            self.pwm_buzzer.start(0)  # 초기 듀티 사이클을 0으로 설정

        if volume == 0:
            self.pwm_buzzer.stop()  # 소리 끄기
            self.buzzer_on = False
        else:
            duty_cycle = volume / 100.0  # 듀티 사이클 계산
            self.pwm_buzzer.ChangeDutyCycle(duty_cycle * 100)  # 듀티 사이클 설정
            if not self.buzzer_on:
                self.pwm_buzzer.start(duty_cycle * 100)  # 소리 켜기
                self.buzzer_on = True

        self.label_sound.setText(str(volume))  # 라벨에 볼륨 크기 표시

    def togglePiezo(self):
        if self.pwm_buzzer is not None:  # pwm_buzzer가 초기화되어 있을 때만 실행
            if self.buzzer_on:
                self.pwm_buzzer.stop()  # 부저 끄기
                self.buzzer_on = False
                self.btn_sound.setText("부저 켜기")
            else:
                # 현재 다이얼 값에 따른 소리 크기로 설정
                current_volume = self.dial_sound.value()
                duty_cycle = current_volume / 100.0
                self.pwm_buzzer.ChangeDutyCycle(duty_cycle * 100)  # 듀티 사이클 설정
                self.pwm_buzzer.start(duty_cycle * 100)  # 소리 켜기
                self.buzzer_on = True
                self.btn_sound.setText("부저 끄기")

    def playSong1(self):
        self.playBuzzerTone(500, 0.5)  # 예시로 0.5초 동안 500Hz 소리 재생

    def playSong2(self):
        self.playBuzzerTone(1000, 1)  # 예시로 1초 동안 1000Hz 소리 재생

    def playSong3(self):
        self.playBuzzerTone(1500, 1.5)  # 예시로 1.5초 동안 1500Hz 소리 재생

    def playSong4(self):
        self.playBuzzerTone(2000, 2)  # 예시로 2초 동안 2000Hz 소리 재생

    def playBuzzerTone(self, frequency, duration):
        self.pwm_buzzer.ChangeFrequency(frequency)  # 주파수 설정
        self.pwm_buzzer.start(50)  # 소리 켜기
        time.sleep(duration)  # 일정 시간 동안 대기
        self.pwm_buzzer.stop()  # 소리 끄기

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

