import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

# Qt 에서 만든 파일을로드
form_class = uic.loadUiType("./test01.ui")[0]

# 윈도우 클래스 정의
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()  # 부모 클래스의 생성자(QMainWindow)를 호출
        self.setupUi(self)   # UI를 설정합니다.

if __name__ == "__main__":
    app = QApplication(sys.argv)  # QApplication 객체를 생성
    myWindow = WindowClass()      # WindowClass의 인스턴스를 생성
    myWindow.show()               # 윈도우를 화면에 보이도록 설정
    app.exec_()                   # 이벤트 루프를 실행
