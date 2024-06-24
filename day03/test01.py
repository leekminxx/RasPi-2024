from flask import Flask
import RPi.GPIO as GPIO

app = Flask(__name__)

red_pin = 21

#GPIO 초기 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(red_pin, GPIO.OUT)

@app.route("/"):
def hell():
	return "Hello World!"

@app.route("/led/<state>")
def led_control(state):
	if state == "on":
		GPIO.output(red_pin, GPIO.HIGH)
		return "LED is ON"
	elif state == "off":
		GPIO.output(red_pin, GPIO.LOW)
		return "LED is oFF"
	elif state == "clear:
