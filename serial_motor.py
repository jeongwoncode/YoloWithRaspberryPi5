# -*- coding: utf-8 -*-
import serial
import time

# 시리얼 포트 설정 (아두이노가 연결된 포트로 변경하세요)
ser = serial.Serial('/dev/ttyUSB0', 9600)  

time.sleep(2)  # 아두이노 초기화를 위한 대기 시간
ser.flushInput()  # 시리얼 입력 버퍼 플러시
ser.flushOutput()  # 시리얼 출력 버퍼 플러시

# 아두이노에 '1'을 전송하여 모터를 작동시킵니다.
ser.write(b'1')
print("complete")

# 아두이노로부터의 응답을 읽습니다.
while True:
    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').rstrip()
        print('done:', data)
        if data == "done":
            print("done")
            break

ser.close()
