import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from PyQt5.QtCore import QTimer, QThread
import RPi.GPIO as GPIO
import time
import threading

# GPIO 설정
red = 24
green = 5
blue = 6
piezoPin = 21
trigPin = 20
echoPin = 16

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)
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
    self.btnBlue.clicked.connect(self.btnBlueFunction)
    self.btnGreen.clicked.connect(self.btnGreenFunction)
    self.btnLedOff.clicked.connect(self.btnLedOffFunction)
    self.btnDistance.clicked.connect(self.btnDistanceFunction)
    self.btnStop.clicked.connect(self.btnStopFunction)  # 추가: 거리 측정 중지 버튼
    self.measure_distance = False  # 거리 측정 상태를 나타내는 변수
    GPIO.setup(piezoPin, GPIO.OUT)
    self.piezo_pwm = GPIO.PWM(piezoPin, 440)

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

  def btnLedOffFunction(self):
    GPIO.output(red, True)
    GPIO.output(green, True)
    GPIO.output(blue, True)

  def btnDistanceFunction(self):
    self.measure_distance = True
    t = threading.Thread(target=self.measure_distance_thread)
    t.start()

  def measure_distance_thread(self):
    while self.measure_distance:
      # Measure distance using ultrasonic sensor
      GPIO.output(trigPin, True)
      time.sleep(0.00001)
      GPIO.output(trigPin, False)
            
      while GPIO.input(echoPin) == False:
        pulse_start = time.time()
            
      while GPIO.input(echoPin) == True:
        pulse_end = time.time()
            
      pulse_duration = pulse_end - pulse_start
      distance = pulse_duration * 17150
      distance = round(distance, 2)
            
      print(f"Distance: {distance} cm")
            
      self.update_lcd_number(distance)

  def update_lcd_number(self, distance):
    self.lcdNumber.display(distance)
    if distance <= 5:
      for _ in range(5):  # Blink for 5 times
        GPIO.output(red, False)
        GPIO.output(blue, True)
        self.piezo_pwm.start(50)  # 부저 PWM 시작 (duty cycle 50%)
        time.sleep(0.2)
        GPIO.output(red, True)
        self.piezo_pwm.stop()  # 부저 PWM 정지
        time.sleep(0.2)
    elif distance <= 10:
      for _ in range(5):  # Blink for 5 times
        GPIO.output(blue, False)
        GPIO.output(red, True)
        self.piezo_pwm.start(50)  # 부저 PWM 시작 (duty cycle 50%)
        time.sleep(0.6)
        GPIO.output(blue, True)
        self.piezo_pwm.stop()  # 부저 PWM 정지
        time.sleep(0.6)
    else:
      GPIO.output(red, True)
      GPIO.output(blue, True)
      self.piezo_pwm.stop()


  def btnStopFunction(self):
    self.measure_distance = False

if __name__ == "__main__":
  app = QApplication(sys.argv)  # QApplication 객체를 생성합니다.
  myWindow = WindowClass()      # WindowClass의 인스턴스를 생성합니다.
  myWindow.show()               # 윈도우를 화면에 보이도록 설정합니다.
  app.exec_()                   # 이벤트 루프를 실행합니다.
