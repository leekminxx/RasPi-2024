#정적라우팅
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
	return "Hello World!!"  #각 경로에 맞는 값을 보여줌 

@app.route("/name")
def name():
	return "<h1>my name is Hong Kill-dong</h1>"

@app.route("/age")
def age():
	return "<h1> 30 year's old</h1>"

if __name__ == "__main__":
	app.run(host="0.0.0.0", port="10011", debug=True)
