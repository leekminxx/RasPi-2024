# date : 2024-06-25
# file : cam_flask01.py
# desc : 카메라 모듈을 연결하여 구현하는 코드


from picamera2 import Picamera2, Preview
import time

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start()
time.sleep(2)
picam2.capture_file("test1.jpg")
