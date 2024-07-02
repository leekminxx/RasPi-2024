# 제일 정상적인 파일


from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QColor
import sys
import RPi.GPIO as GPIO
import time
import adafruit_dht
import board

# GPIO 설정
red = 25
green = 19
blue = 26
piezoPin = 4
trigPin = 27
echoPin = 17
sensor_pin = 20

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)
GPIO.setup(piezoPin, GPIO.OUT)
GPIO.setup(trigPin, GPIO.OUT)
GPIO.setup(echoPin, GPIO.IN)
GPIO.setup(sensor_pin, GPIO.IN)

dhtDevice = adafruit_dht.DHT11(board.D18)  # DHT11 센서 초기화

# PWM 설정
pwm_red = GPIO.PWM(red, 100)  # Red LED, 100 Hz
pwm_green = GPIO.PWM(green, 100)  # Green LED, 100 Hz
pwm_blue = GPIO.PWM(blue, 100)  # Blue LED, 100 Hz
pwm_piezo = GPIO.PWM(piezoPin, 1000)  # Piezo Buzzer, 1000 Hz

form_class = uic.loadUiType("led.ui")[0]

class UltrasonicThread(QThread):
    distance_measured = pyqtSignal(float)

    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            GPIO.output(trigPin, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(trigPin, GPIO.LOW)

            while GPIO.input(echoPin) == GPIO.LOW:
                pulse_start = time.time()

            while GPIO.input(echoPin) == GPIO.HIGH:
                pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17150
            distance = round(distance, 2)

            self.distance_measured.emit(distance)
            time.sleep(1)

class DHTThread(QThread):

    temp_measured = pyqtSignal(float)
    humid_measured = pyqtSignal(float)
    long_num = 0

    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            try:
                temp = dhtDevice.temperature
                humid = dhtDevice.humidity
                print(f'Temp: {temp}C / Humidity: {humid}%')
                self.temp_measured.emit(temp)
                self.humid_measured.emit(humid)
                time.sleep(2)
            except RuntimeError as error:
                print(f'Runtime error occurred: {error}')
                time.sleep(2)
            except Exception as error:
                print(f'Error occurred: {error}')
                time.sleep(2)


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
        
        self.dial_led.valueChanged.connect(self.dialValueChanged)
        self.dial_sound.valueChanged.connect(self.soundDialValueChanged)

        self.label_led.setText("0")
        self.label_sound.setText("0")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.cycleColors)
        self.cycling = False
        self.current_color_index = 0
        self.colors = [self.turnOnRed, self.turnOnGreen, self.turnOnBlue]

        self.ultrasonic_thread = UltrasonicThread()
        self.ultrasonic_thread.distance_measured.connect(self.handleDistance)
        self.ultrasonic_thread.start()

        self.dht_thread = DHTThread()
        self.dht_thread.temp_measured.connect(self.updateTemp)
        self.dht_thread.humid_measured.connect(self.updateHumid)
        self.dht_thread.start()

        self.current_led = None
        self.turnOffLED()
    
        # 버튼 초기 설정
        self.btn1_r.setStyleSheet("background-color: red")
        self.btn1_g.setStyleSheet("background-color: green")
        self.btn1_b.setStyleSheet("background-color: blue")
    
    def turnOnRed(self):
        self.stopAllPWMs()
        pwm_red.start(100)
        pwm_green.stop()
        pwm_blue.stop()
        GPIO.output(red, GPIO.LOW)
        GPIO.output(green, GPIO.HIGH)
        GPIO.output(blue, GPIO.HIGH)
        self.updateLabel("Red", QColor(255, 0, 0))
        self.current_led = pwm_red

    def turnOnGreen(self):
        self.stopAllPWMs()
        pwm_red.stop()
        pwm_green.start(100)
        pwm_blue.stop()
        GPIO.output(red, GPIO.HIGH)
        GPIO.output(green, GPIO.LOW)
        GPIO.output(blue, GPIO.HIGH)
        self.updateLabel("Green", QColor(0, 255, 0))
        self.current_led = pwm_green

    def turnOnBlue(self):
        self.stopAllPWMs()
        pwm_red.stop()
        pwm_green.stop()
        pwm_blue.start(100)
        GPIO.output(red, GPIO.HIGH)
        GPIO.output(green, GPIO.HIGH)
        GPIO.output(blue, GPIO.LOW)
        self.updateLabel("Blue", QColor(0, 0, 255))
        self.current_led = pwm_blue

    def turnOffLED(self):
        self.timer.stop()
        self.cycling = False
        self.stopAllPWMs()
        GPIO.output(red, GPIO.HIGH)
        GPIO.output(green, GPIO.HIGH)
        GPIO.output(blue, GPIO.HIGH)
        self.updateLabel("", QColor(0, 0, 0))
        self.current_led = None

    def toggleCycling(self):
        if self.cycling:
            self.timer.stop()
            self.cycling = False
        else:
            self.cycling = True
            self.timer.start(1000)
            self.cycleColors()

    def cycleColors(self):
        if self.cycling:
            self.colors[self.current_color_index]()
            self.current_color_index = (self.current_color_index + 1) % len(self.colors)

    def dialValueChanged(self, value):
        value = int(value)
        self.label_led.setText(f"{str(value)}")

        if self.current_led:
            self.current_led.ChangeDutyCycle(value)

    def soundDialValueChanged(self, value):
        volume = int(value)
        self.label_sound.setText(str(volume))
        pwm_piezo.start(volume)

    def togglePiezo(self):
        if pwm_piezo.is_started:
            pwm_piezo.stop()
            self.btn_sound.setText("소리 시작")
            self.updateSoundLabel(0)
        else:
            pwm_piezo.start(int(self.dial_sound.value()))
            self.btn_sound.setText("소리 중지")
            self.updateSoundLabel(int(self.dial_sound.value()))

    def updateLabel(self, color_name, color):
        self.label_led.setText(color_name)
        self.label_led.setStyleSheet(f"color: {color.name()}")

    def updateSoundLabel(self, volume):
        self.label_sound.setText(str(volume))

    def handleDistance(self, distance):
        self.lcdNumber_dis.display(distance)

        if distance <= 10:
            pwm_piezo.start(50)
            self.blinkRed()
        elif distance <= 20:
            pwm_piezo.start(30)
            self.blinkGreen()
        elif distance <= 30:
            pwm_piezo.start(10)
            self.blinkBlue()
        else:
            pwm_piezo.stop()
            self.stopAllPWMs()
            self.btn_sound.setText("소리 시작")
            self.updateSoundLabel(0)

    def blinkRed(self):
        GPIO.output(red, GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(red, GPIO.HIGH)
        time.sleep(0.5)

    def blinkGreen(self):
        GPIO.output(green, GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(green, GPIO.HIGH)
        time.sleep(0.5)

    def blinkBlue(self):
        GPIO.output(blue, GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(blue, GPIO.HIGH)
        time.sleep(0.5)

    def stopAllPWMs(self):
        #pwm_red.stop()
        pwm_green.stop()
        pwm_blue.stop()

    def updateTemp(self, temp):
        self.lcdNumber_temp.display(temp)

    def updateHumid(self, humid):
        self.lcdNumber_humid.display(humid)

    def closeEvent(self, event):
        self.ultrasonic_thread.terminate()
        self.dht_thread.terminate()
        GPIO.cleanup()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
