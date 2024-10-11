# -*- coding: utf-8 -*-
import subprocess

def upload_arduino_code():
    # 아두이노 스케치 파일의 실제 경로를 설정하세요
    arduino_sketch_path = "/home/casptone/Downloads/yolov5-master/arduino_invscode/arduino_led_control.ino"
    
    compile_command = [
        "arduino-cli", "compile", "--fqbn", "arduino:avr:uno", arduino_sketch_path
    ]
    upload_command = [
        "arduino-cli", "upload", "-p", "/dev/ttyUSB0", "--fqbn", "arduino:avr:uno", arduino_sketch_path
    ]

    # 스케치 컴파일
    subprocess.run(compile_command, check=True)
    # 컴파일 후 아두이노 보드에 업로드
    subprocess.run(upload_command, check=True)

if __name__ == "__main__":
    try:
        upload_arduino_code()
        print("Arduino code uploaded successfully!")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
