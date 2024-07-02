from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QTimer
import sys
import RPi.GPIO as GPIO
import time
import random

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

# PWM 객체 생성
pwm_red = GPIO.PWM(red, 100)
pwm_green = GPIO.PWM(green, 100)
pwm_blue = GPIO.PWM(blue, 100)

form_class = uic.loadUiType("led.ui")[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # 버튼 및 다이얼 연결
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

        # 초기 상태 설정
        self.label_sound = QLabel(self)
        self.label_sound.setText("0")
        self.label_sound.move(20, 220)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.cycleColors)
        self.cycling = False
        self.current_color_index = 0
        self.colors = [self.turnOnRed, self.turnOnGreen, self.turnOnBlue]

        self.distance_timer = QTimer(self)
        self.distance_timer.timeout.connect(self.measureDistance)
        self.distance_timer.start(1000)

        self.buzzer_on = False
        self.pwm_buzzer = None
        self.turnOffLED()

    def turnOnRed(self):
        self.timer.stop()
        self.cycling = False
        GPIO.output(red, GPIO.LOW)
        GPIO.output(green, GPIO.HIGH)
        GPIO.output(blue, GPIO.HIGH)
        self.updateLabel("Red", "Red 켜짐")

    def turnOnGreen(self):
        self.timer.stop()
        self.cycling = False
        GPIO.output(red, GPIO.HIGH)
        GPIO.output(green, GPIO.LOW)
        GPIO.output(blue, GPIO.HIGH)
        self.updateLabel("Green", "Green 켜짐")

    def turnOnBlue(self):
        self.timer.stop()
        self.cycling = False
        GPIO.output(red, GPIO.HIGH)
        GPIO.output(green, GPIO.HIGH)
        GPIO.output(blue, GPIO.LOW)
        self.updateLabel("Blue", "Blue 켜짐")

    def turnOffLED(self):
        self.timer.stop()
        self.cycling = False
        GPIO.output(red, GPIO.HIGH)
        GPIO.output(green, GPIO.HIGH)
        GPIO.output(blue, GPIO.HIGH)
        pwm_red.stop()
        pwm_green.stop()
        pwm_blue.stop()
        self.updateLabel("", "LED 꺼짐")

    def toggleCycling(self):
        if self.cycling:
            self.timer.stop()
            self.cycling = False
        else:
            self.timer.start(1000)
            self.cycleColors()
            self.cycling = True

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

        self.updateLabel("", f"밝기: {brightness}")

    def dialSoundChanged(self, value):
        volume = int(value)

        if self.pwm_buzzer is None:
            self.pwm_buzzer = GPIO.PWM(piezoPin, 1000)
            self.pwm_buzzer.start(0)

        if volume == 0:
            self.pwm_buzzer.stop()
            self.buzzer_on = False
        else:
            duty_cycle = volume / 100.0
            self.pwm_buzzer.ChangeDutyCycle(duty_cycle * 100)
            if not self.buzzer_on:
                self.pwm_buzzer.start(duty_cycle * 100)
                self.buzzer_on = True

        self.label_sound.setText(str(volume))

    def togglePiezo(self):
        if self.pwm_buzzer is not None:
            if self.buzzer_on:
                self.pwm_buzzer.stop()
                self.buzzer_on = False
                self.btn_sound.setText("부저 켜기")
            else:
                current_volume = self.dial_sound.value()
                duty_cycle = current_volume / 100.0
                self.pwm_buzzer.ChangeDutyCycle(duty_cycle * 100)
                self.pwm_buzzer.start(duty_cycle * 100)
                self.buzzer_on = True
                self.btn_sound.setText("부저 끄기")

    def playSong1(self):
        self.playBuzzerTone(500, 0.5)

    def playSong2(self):
        self.playBuzzerTone(1000, 1)

    def playSong3(self):
        self.playBuzzerTone(1500, 1.5)

    def playSong4(self):
        self.playBuzzerTone(2000, 2)

    def playBuzzerTone(self, frequency, duration):
        self.pwm_buzzer.ChangeFrequency(frequency)
        self.pwm_buzzer.start(50)
        time.sleep(duration)
        self.pwm_buzzer.stop()

    def measureDistance(self):
        GPIO.output(trigPin, True)
        time.sleep(0.00001)
        GPIO.output(trigPin, False)

        while GPIO.input(echoPin) == 0:
            pulse_start = time.time()

        while GPIO.input(echoPin) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)

        self.lcdNumber_dis.display(distance)

        if distance <= 10:
            self.turnOnRed()
        elif distance <= 20:
            self.turnOnGreen()
        elif distance <= 30:
            self.turnOnBlue()

    def updateLabel(self, color_name, status_text):
        self.label_sound.setText(color_name)
        # self.label_status.setText(status_text)  # label_status가 정의되지 않아 주석 처리

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
