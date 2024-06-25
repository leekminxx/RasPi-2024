# date : 2024-06-25
# file : html_flask01.py
# desc :동일한폴더 위치에 templates 폴더를 만들고 거기에 html파일을 저장한다

from flask import Flask, request, render_template
import RPi.GPIO as GPIO

app = Flask(__name__)

led = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(led ,GPIO.OUT)
GPIO.setwarnings(False)

@app.route('/')
def home():
	return render_template("index.html")

@app.route('/data' , methods = ['POST'])
def data():
	data = request.form['led']

	if(data == 'on'):
		GPIO.output(led, False)
		return home()

	elif(data == 'off'):
		GPIO.output(led, True)
		return home()
		
if __name__== '__main__':
	app.run(host = '0.0.0.0' , port= '18080', debug=True)
