from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QTimer
import sys
import RPi.GPIO as GPIO
import time

red = 25
green = 19
blue = 26
piezoPin = 17
trigPin = 27
echoPin = 4

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)
GPIO.setup(piezoPin, GPIO.OUT)

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

        self.label_led.setText("check")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.cycleColors)
        self.cycling = False
        self.current_color_index = 0
        self.colors = [self.turnOnRed, self.turnOnGreen, self.turnOnBlue]

        self.distance_timer = QTimer(self)
        self.distance_timer.start(1000)

    def turnOnRed(self):
        GPIO.output(red, False)
        GPIO.output(green, True)
        GPIO.output(blue, True)
        self.updateLabel("Red")

    def turnOnGreen(self):
        GPIO.output(red, True)
        GPIO.output(green, False)
        GPIO.output(blue, True)
        self.updateLabel("Green")

    def turnOnBlue(self):
        GPIO.output(red, True)
        GPIO.output(green, True)
        GPIO.output(blue, False)
        self.updateLabel("Blue")

    def turnOffLED(self):
        self.timer.stop()
        self.cycling = False
        GPIO.output(red, True)
        GPIO.output(green, True)
        GPIO.output(blue, True)
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
