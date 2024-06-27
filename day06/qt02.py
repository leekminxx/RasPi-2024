from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys

# Qt에서 만든 UI 파일을 로드합니다.
form_class = uic.loadUiType("./btn01.ui")[0]

# 윈도우 클래스 정의
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()  # 부모 클래스의 생성자(QMainWindow)를 호출합니다.
        self.setupUi(self)  # UI를 설정합니다.
        # 이벤트 함수 등록
        self.btn_1.clicked.connect(self.btn1Function)
        self.btn_2.clicked.connect(self.btn2Function)

    def btn1Function(self):
        print("LED ON Button Clicked")

    def btn2Function(self):
        print("LED OFF Button Clicked")

    def slot1(self):
        print("EXIT!!")

if __name__ == "__main__":
    app = QApplication(sys.argv)  # QApplication 객체를 생성합니다.
    myWindow = WindowClass()      # WindowClass의 인스턴스를 생성합니다.
    myWindow.show()               # 윈도우를 화면에 보이도록 설정합니다.
    app.exec_()                   # 이벤트 루프를 실행합니다.
