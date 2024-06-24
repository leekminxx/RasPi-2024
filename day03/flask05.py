# date : 2024-06-24
# file : flask05.py
# desc : 클라이언트가 서버에 데이터값을 넘겨주고 서버에서 받은다음 화면에 출력해서 보여주는 코드


from flask import Flask, request #request 를넣어야 함

app = Flask(__name__)

@app.route("/")
def get():
	value1=request.args.get("이름","user")
	value2=request.args.get("주소","부산")
	return value1+":"+value2

if __name__ == "__main__":
	app.run(host="0.0.0.0", port="10011", debug=True)
	
