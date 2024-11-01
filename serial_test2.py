# -*- coding: utf-8 -*-
import serial
import time

# 아두이노 포트와의 시리얼 연결 초기화
arduino = serial.Serial('/dev/ttyUSB0', 9600)
time.sleep(0.5)  # 연결 초기화 시간 대기

# LED 제어 함수
def blink_led(times, delay):
    for _ in range(times):
        arduino.write(b'1') 
        time.sleep(delay)  

if __name__ == "__main__":
    try:
        while True:
            command = input("Enter 'a' to blink 1 time, 's' to blink 2 times, 'd' to blink 3 times, 'f' to blink 4 times, or 'q' to quit: ")
            if command == 'a':
                blink_led(1, 0.5)
            elif command == 's':
                blink_led(2, 0.5)
            elif command == 'd':
                blink_led(3, 0.5)
            elif command == 'f':
                blink_led(4, 0.5)
            elif command == 'q':
                break

    except KeyboardInterrupt:
        print("\nProgram interrupted.")
    finally:
        arduino.close()
        print("Serial connection closed.")
