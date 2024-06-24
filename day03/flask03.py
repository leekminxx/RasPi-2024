# URL 접속을 /led/on , /let/off 로 접속하면 led를 on,off하는 웹페이지를 만들기
from flask import Flask
import RPi.GPIO as GPIO

app = Flask(__name__)

red_pin = 21

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(red_pin, GPIO.OUT)

@app.route("/on")
def on():
    GPIO.output(red_pin, GPIO.LOW)
    return "LED on!!"

@app.route("/off")
def off():
    GPIO.output(red_pin, GPIO.HIGH)
    return "<h1>LED off!!</h1>"

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=10011, debug=True)
    except KeyboardInterrupt:
        GPIO.cleanup()
