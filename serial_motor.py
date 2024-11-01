# -*- coding: utf-8 -*-
import serial
import time

# �ø��� ��Ʈ ���� (�Ƶ��̳밡 ����� ��Ʈ�� �����ϼ���)
ser = serial.Serial('/dev/ttyUSB0', 9600)  

time.sleep(2)  # �Ƶ��̳� �ʱ�ȭ�� ���� ��� �ð�
ser.flushInput()  # �ø��� �Է� ���� �÷���
ser.flushOutput()  # �ø��� ��� ���� �÷���

# �Ƶ��̳뿡 '1'�� �����Ͽ� ���͸� �۵���ŵ�ϴ�.
ser.write(b'1')
print("complete")

# �Ƶ��̳�κ����� ������ �н��ϴ�.
while True:
    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').rstrip()
        print('done:', data)
        if data == "done":
            print("done")
            break

ser.close()
