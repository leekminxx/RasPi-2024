#URL 접속을 /led/on , led/off로 접속하면 led를 on, off 하는 웹페이지를 만들어보기
from flask import Flask
import RPi.GPIO as GPIO

app = Flask(__name__)
red_pin = 21

# GPIO 초기 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(red_pin, GPIO.OUT)

@app.route("/")
def hello():
    return "Hello World!!"

@app.route("/led/<state>")
def led_control(state):
    if state == "on":
        GPIO.output(red_pin, GPIO.LOW)
        return "LED ON"
    elif state == "off":
        GPIO.output(red_pin, GPIO.HIGH)
        return "LED OFF"
    elif state == "clear":
        GPIO.cleanup()
        return "GPIO Cleanup()"
    else:
        return "Use 'on', 'off', or 'clear'."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="10011", debug=True)
