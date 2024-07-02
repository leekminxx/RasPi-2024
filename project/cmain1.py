from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import QThread, pyqtSignal, QStringListModel, QTimer
import sys
import RPi.GPIO as GPIO
import time
import threading
import adafruit_dht
import board

redPin = 25
greenPin = 5
bluePin = 6
piezoPin = 21
trigPin = 20
echoPin = 16
dhtPin = 12
dht_sensor = adafruit_dht.DHT11(board.D12)

class DHTSensorReader(QThread):
    update_signal = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        while self.running:
            try:
                temperature = dht_sensor.temperature
                humidity = dht_sensor.humidity
                if temperature is not None and humidity is not None:
                    temperature_str = f"Temperature: {temperature:.1f}°C"
                    humidity_str = f"Humidity: {humidity:.1f}%"
                    self.update_signal.emit([temperature_str, humidity_str])
                else:
                    self.update_signal.emit(["Failed to get reading. Try again!"])
            except RuntimeError as e:
                print(f"Error reading DHT sensor: {e}")
                self.update_signal.emit(["Failed to get reading. Try again!"])
            time.sleep(2)

    def stop(self):
        self.running = False
        self.wait()

# 소리와 거리를 재는 변수들을 설정
speedOfSound = 34300  # 음속 (cm/s)

GPIO.setmode(GPIO.BCM)
GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)
GPIO.setup(bluePin, GPIO.OUT)
GPIO.setup(piezoPin, GPIO.OUT)
GPIO.setup(trigPin, GPIO.OUT)
GPIO.setup(echoPin, GPIO.IN)

form_class = uic.loadUiType("main.ui")[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.btnRed.clicked.connect(lambda: self.setLED("red"))
        self.btnGreen.clicked.connect(lambda: self.setLED("green"))
        self.btnBlue.clicked.connect(lambda: self.setLED("blue"))
        self.btnOff.clicked.connect(lambda: self.setLED("off"))
        self.btnMeasureDistance.clicked.connect(self.startMeasurement)
        self.btnStopMeasure.clicked.connect(self.stopMeasurement)

        self.model = QStringListModel()
        self.listView.setModel(self.model)

        self.sensor_reader = DHTSensorReader()
        self.sensor_reader.update_signal.connect(self.update_list_view)
        self.is_running = False

        self.Stbtn.clicked.connect(self.start_clicked)
        self.Spbtn.clicked.connect(self.stop_clicked)

        self.distance = 0.0
        self.measuring = False
        self.measure_thread = None

        # Buzz PWM 객체 생성
        self.Buzz = GPIO.PWM(piezoPin, 440)
        self.Buzz.stop()

        self.lcdNumber.display(self.distance)

        self.labelLED.setText("LED Color Status")
        font = QFont()
        font.setPointSize(16)
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
        GPIO.output(trigPin, False)

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

            self.controlLEDAndBuzz()
            self.updateLCD()

    def controlLEDAndBuzz(self):
        if self.distance <= 5:
            GPIO.output(redPin, False)
            time.sleep(0.1)
            GPIO.output(redPin, True)
            time.sleep(0.1)
            self.Buzz.start(50)
            self.Buzz.ChangeFrequency(200)
        elif self.distance <= 10:
            GPIO.output(greenPin, False)
            GPIO.output(redPin, True)
            self.Buzz.start(50)
            self.Buzz.ChangeFrequency(300)
        else:
            GPIO.output(redPin, True)
            GPIO.output(greenPin, True)
            self.Buzz.stop()

    def updateLCD(self):
        self.lcdNumber.display(self.distance)

    def start_clicked(self):
        if not self.is_running:
            self.is_running = True
            self.sensor_reader.start()
            print("센서 측정 시작 버튼 눌림")

    def update_list_view(self, data):
        self.model.setStringList(data)
        if len(data) > 1:
            humidity = float(data[1].split(':')[1].strip('%'))
            if humidity < 50:
                GPIO.output(redPin, GPIO.HIGH)
            else:
                GPIO.output(redPin, GPIO.LOW)

    def stop_clicked(self):
        if self.is_running:
            self.is_running = False
            self.sensor_reader.stop()
            GPIO.output(redPin, GPIO.HIGH)
            print("센서 측정 정지 버튼 눌림")

    def closeEvent(self, event):
        GPIO.cleanup()
        if self.sensor_reader and self.sensor_reader.isRunning():
            self.sensor_reader.stop()
            self.sensor_reader.wait()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
