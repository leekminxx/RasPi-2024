# RasPi-2024
라즈베리파이 설계 과정 레퍼지토리
## 1일차
- 키르히호프 법칙 
    - KVC(전압 법칙): 키르히호프 전압 법칙은 회로의 닫힌 루프에서 모든 전압 강하의 합이 0
    - KCL(전류 법칙): 키르히호프 전류 법칙은 회로의 임의의 접점에서 들어오는 전류의 합과 나가는 전류의 합이 같음
    ![KCL](https://raw.githubusercontent.com/leekminxx/RasPi-2024/main/img/r001.png)

- 전기회로 구조
    - 전류 ! : 모든 전류는 그라운드를 통해서 흐름 
    - 전압|볼트(V) : 전압은 전기 회로 내에서 전하가 이동하는 데 필요한 에너지 차이를 의미 , 전위차 또는 전기압이라고도 함
    - 저항|옴(Ω): 회로 내에서 전류의 흐름을 제어하고 조절하는 역할
        - 옴의 법칙 (Ohm's Law)
            - 전류 (I): 전하의 흐름, 단위는 암페어(A)
            - 전압 (V): 전하가 이동하는 데 필요한 에너지 차이, 단위는 볼트(V)
            - 저항 (R): 전류의 흐름을 방해하는 물질의 특성, 단위는 옴(Ω)

- GPIO 설정함수
    - GPIO.setmode(GPIO.BOARD) - wPi
    - GPIO.setmode(GPIO.BCM) - BCM
    - GPIO.setup(channel, GPIO.mode)
    - channel : 핀 번호, mode : IN/OUT
    - GPIO.cleanup()

- GPIO 출력함수
   - GPIO.output(channel , state)
    - channel : 핀 번호, state ; HIGH/LOW or 1/0 or True/Fasle
- GPIO 입력함수
   - GPIO.input(channel)
    - channel; 핀번호, 반환값 H/L or 1/- or T/F
- 시간지연 함수 TIME.SLEEP(SECS)


- VRGB
    - vcc : G , 에서 전류가 흘러옴 > 그라운드를 향해야 한바퀴를 돌아서 전류가 흐름 전원이 공급
    - R : Red색상을 켜기 위해선 R을 거쳐서 ground 로 향하면 됨 

- 스위치 
    ![input](https://raw.githubusercontent.com/leekminxx/RasPi-2024/main/img/r002.png)



- 피에조 부저(piezo buzzer)  (PWM 방식으로 작동)
    - (압전효과) 물체에 기계적인 압력을 가하면 전압이 발생하고 , 역으로 전압을 가하면 기계적인 변형이 발생하는 형상 
    - 디지털 핀의 전압을 매우 짧은 시간 안에 바꾸어가며 주파수에 맞는 소리를 낼 수 있음 
    - 능동 부저(Active Buzzer)
        - 외부 전원으로만 소리가 발생 **단순한 소리출력만 가능**
    - 수동 부저(Passive Buzzer)
        - 외부전기 신호를 받아서 소리를 발생시킴 
        - 능동부저와 다르게 **발진 회로가 없어 외부에서 제공되는 주파수 신호가 필요함**
        - 다양한 음색을 출력가능 
        - tone() , noTone()함수를 사용

    - ![피에조 부저원리(압전효과)](https://raw.githubusercontent.com/leekminxx/RasPi-2024/main/img/r004.png)


## 2일차 
- 적외선 인체감지 센서(PIR, Passive Infrated Sensor)
    - 역할 : 센서는 적외선을 감지하여 움직임을 감지하는 센서
        - 핀 구성 3가지 
            - VCC: 전원 공급 핀(보통 5V 또는 3.3V)
            - GND: 접지 핀
            - OUT: 출력 핀 (감지 신호 출력)
        - 특징 : 
            - 출력 신호: 디지털 출력 (High/Low 신호)
    - 감도조절
        - 모듈 앞에 노란색 조절기 돌리기 

- 가상환경
    - venv 모듈 사용
        - 프로젝트 디텍토리 
        - 가상환경을 생성 : python3 -m venv env
        - 가상환경 활성화 : source ./env/bin/activate
        - 가상환경을 실행하려면 : pip install RPi.GPIO 를 통해서 패키지 설치
        - 가상환경을 빠져나오려면 : decativate

- 초음파 센서 (HC-SR04 초음파 센서)
 - 초음파를 방출하고 반사되어 돌아오는 시간을 측정하여 거리를 계산 (약 40KHz)
 - 실내에서 측정할 경우 반사 물체가 너무 가깝거나 너무 멀리 있을 때 정확한 측정이 어려울 수 있음
    - 작동원리
        - 송신기 : 40KHz 영역대의 초음파를 방출 
        - 수신시 : 송신기에서 방출된 초음파가 물체에 반사되어 수신기에 돌아온 시간을 통해 거리를 측정
  - ![초음파센서 작동원리](https://raw.githubusercontent.com/leekminxx/RasPi-2024/main/img/r003.png)
    - 라즈베리파이 연결
        - 필요한 부품:
            - 라즈베리파이
            - HC-SR04 초음파 센서
            - 점퍼 케이블

    - 핀 구성 4가지:
        - VCC: 전원 입력 (5V)
        - Trig: 트리거 핀, 초음파 신호를 보내는 핀
        - Echo: 에코 핀, 반사된 신호를 수신하는 핀
        - GND: 그라운드

- 라즈베리파이 입출력 키트 확인 방법
    - sudo ./build : WiringPi 라이브러리를 빌드 (관리자권한 실행)
    - WiringPi Build script : WiringPi 라이브러리빌드를 실행 
    - gpio -v : 설치된 WiringPi 의 버전을 확인 세부정보확인가능
    - goio readall : GPIO 핀의 상태를 자세히 볼 수 있음 , 핀의 입출력 정보를 확인 할 수 있음


## day03
- 아두이노 1채널 5V 미니 릴레이 모듈 ![SZH-EK082](https://raw.githubusercontent.com/leekminxx/RasPi-2024/main/img/r005.png)
    - 전기적 신호를 사용하여 높은 전압 또는 전류를 제어할 수 있도록 도와주는 장치 
    - 가정 자동화, 로봇 공학, DIY 전자 프로젝트 등 다양한 분야에서 사용
        - 전기 특성 
            - 정격 전압 : DC 5V
            - 정격 전류 : 10A
            - 최대 출력 전압 : AC 250V / DC 30V
        -  핀 구성 3가지
            - VCC: 5V 전원 공급.
            - GND: 접지.
            - IN: 제어 신호 입력. HIGH 신호를 주면 릴레이가 활성화.
- 릴레이의 작동 원리 
    - 릴레이는 쉽게 말해서 ON , OFF가 있는 일종의 '스위치' 
    - (일반적인 스위치와의 동작원리는 아님) : 일반 스위치 : 수동으로 ON , OFF | 릴레이 : 자동으로 ON , OFF
    - **별도로 분리되어 흐르는 전기를 스위칭**할 수 있는 신호 또는 펄스를 만들어줌
    - 작동하기 위해 전압은 낮지만 , 입력할 수 있는 전압은 높음
    - 낮은 전압/전류를 이용하여 더 높은 전압/전류를 제어화는데에 많이 사용 
- 특징
    - 아두이노를 통해 다양한 고전력 기기를 손쉽게 제어가능.
    - 다양한 전자 프로젝트에 유용하게 활용될 수 있는 중요한 컴포넌트중 하나.


- 스테퍼모터(stepper motor,), 스텝모터(step motor), 또는 스테핑모터(stepping motor)
    - 전기모터의 한 종류 , 각도를 정밀하게 제어할 수 있음
    - 일정한 각도로 나누어진 여러 단계(step)로 회전 
    - 회전차를 일정한 각도로 움직이게 함
        - 정밀한 제어: 각 스텝의 각도가 정해져 있어 정밀한 위치 제어가 가능
        - 높은 반복 정밀도: 동일한 조건에서 반복적으로 같은 위치로 돌아올 수 있음
        - 개방 루프 제어: 피드백 시스템이 없이도 정밀하게 제어할 수 있음
    

- 모터 드라이버 
 - ![모터 드라이버 아두이노](https://raw.githubusercontent.com/leekminxx/RasPi-2024/main/img/r007.png)

    - 모터 컨트롤에 많은 전류가 사용되기 때문에 드라이브 회로나 모듈을 거쳐서 전압 , 전류를 증폭시킨 다음 모터를 구동해야 하기 때문에 사용 
    - 작은 전류와 전압을 제어하는 프로세서와 큰 전류로 작동하는 모터 사이에 중재 역할을 하는 장치
    - ![모터 드라이버](https://raw.githubusercontent.com/leekminxx/RasPi-2024/main/img/r006.png)

