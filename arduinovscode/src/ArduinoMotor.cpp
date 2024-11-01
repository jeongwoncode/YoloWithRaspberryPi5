#include <Arduino.h>

int ENAPin = 13;  
int DIRPin = 12;
int PULPin = 11;
int pulse = 200;  // �޽��� ���� �ð� (����ũ����)

void setup() {
    pinMode(ENAPin, OUTPUT);
    digitalWrite(ENAPin, LOW);  // ����̹� Ȱ��ȭ
    pinMode(DIRPin, OUTPUT);
    digitalWrite(DIRPin, LOW);
    pinMode(PULPin, OUTPUT);
    digitalWrite(PULPin, LOW);
    
    Serial.begin(9600);  // �ø��� ��� ����
    delay(2000);  // �Ƶ��̳� �ʱ�ȭ�� ���� ��� �ð�
}

void loop() {
    if (Serial.available() > 0) {  // �ø��� �Է��� �ִ� ���
        char command = Serial.read();  // �ø��󿡼� ����� ����
        Serial.println(command);  // �����: ���ŵ� ��� ���
        
        if (command == '1') {
            digitalWrite(DIRPin, HIGH);  // ȸ�� ���� ����
            int pulses = 200;  // ȸ���� �޽� �� ����
            for (int i = 0; i < pulses; i++) {
                digitalWrite(PULPin, HIGH);
                delayMicroseconds(pulse);
                digitalWrite(PULPin, LOW);
                delayMicroseconds(pulse);
            }
            Serial.println("done");  // ����� �޽���
        }
    }
}
