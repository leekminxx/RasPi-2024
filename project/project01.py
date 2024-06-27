from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys

form_class = uic.loadUiType("led")[0]

class WindowClass(QMainWindow, form_class):
	def __init__(self):
			super().__init__()
			self.setupUi(self)

  def slot1(self):


if __name__ =="__main__":
		app = QApplication(sys.argv)
		myWindow = WindowClass()
		myWindow.show()
		app.exec_()
