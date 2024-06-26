import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 설정
segment_pins = [5, 6, 12, 16, 20, 13, 21]
com_pin = [4, 17, 27, 22]

# 각 숫자에 해당하는 7세그먼트 패턴 (0 ~ 9)
segment_patterns = [
    [1, 1, 1, 1, 1, 1, 0],  # 0
    [0, 1, 1, 0, 0, 0, 0],  # 1
    [1, 1, 0, 1, 1, 0, 1],  # 2
    [1, 1, 1, 1, 0, 0, 1],  # 3
    [0, 1, 1, 0, 0, 1, 1],  # 4
    [1, 0, 1, 1, 0, 1, 1],  # 5
    [1, 0, 1, 1, 1, 1, 1],  # 6
    [1, 1, 1, 0, 0, 0, 0],  # 7
    [1, 1, 1, 1, 1, 1, 1],  # 8
    [1, 1, 1, 1, 0, 1, 1]   # 9
]

def setup():
    GPIO.setmode(GPIO.BCM)
    for pin in segment_pins:
        GPIO.setup(pin, GPIO.OUT)
    for pin in com_pin:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)  # 공통 핀 비활성화

def display_digit(digit, position):
    pattern = segment_patterns[digit]
    for pin, state in zip(segment_pins, pattern):
        GPIO.output(pin, state)
    GPIO.output(com_pin[position], GPIO.LOW)  # 해당 자리수 활성화
    time.sleep(0.001)  # 잠깐 대기 (약 1ms)
    GPIO.output(com_pin[position], GPIO.HIGH)  # 해당 자리수 비활성화

def display_number(number):
    digits = [int(d) for d in str(number)]
    for i, digit in enumerate(digits):
        display_digit(digit, i)

def main():
    setup()
    try:
        while True:
            display_number(1234)
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
