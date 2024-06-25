from picamera2 import Picamera2

picam2 = Picamera2()

# global_camera_info() 반환 값 출력
camera_info = picam2.global_camera_info()
print("Camera Info:", camera_info)

# camera_num이 유효한지 확인
camera_num = 0  # 기본값 설정, 필요한 경우 변경
if camera_num < len(camera_info):
    picam2 = Picamera2(camera_num=camera_num)
else:
    print(f"Error: camera_num {camera_num} is out of range.")
