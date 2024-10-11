#include <Arduino.h>

int ledPin = 12;  // LED가 연결된 핀 번호

void setup() {
    pinMode(ledPin, OUTPUT);
    digitalWrite(ledPin, LOW);  // 초기 상태에서 LED 꺼짐으로 설정
    Serial.begin(9600);  // 시리얼 통신 시작
}

void loop() {
    if (Serial.available() > 0) {  // 시리얼 입력이 있는 경우
        char command = Serial.read();  // 시리얼에서 명령을 읽음
        Serial.println(command);  // 디버깅: 수신된 명령 출력
        
        if (command == '1') {
            digitalWrite(ledPin, HIGH);  // LED ON
            delay(500);  // 0.5초 대기
            digitalWrite(ledPin, LOW);   // LED OFF
            delay(200);
        }
    }
}
