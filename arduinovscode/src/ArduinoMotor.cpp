#include <Arduino.h>

int ENAPin = 13;  
int DIRPin = 12;
int PULPin = 11;
int pulse = 200;  // 펄스의 지속 시간 (마이크로초)

void setup() {
    pinMode(ENAPin, OUTPUT);
    digitalWrite(ENAPin, LOW);  // 드라이버 활성화
    pinMode(DIRPin, OUTPUT);
    digitalWrite(DIRPin, LOW);
    pinMode(PULPin, OUTPUT);
    digitalWrite(PULPin, LOW);
    
    Serial.begin(9600);  // 시리얼 통신 시작
    delay(2000);  // 아두이노 초기화를 위한 대기 시간
}

void loop() {
    if (Serial.available() > 0) {  // 시리얼 입력이 있는 경우
        char command = Serial.read();  // 시리얼에서 명령을 읽음
        Serial.println(command);  // 디버깅: 수신된 명령 출력
        
        if (command == '1') {
            digitalWrite(DIRPin, HIGH);  // 회전 방향 설정
            int pulses = 200;  // 회전할 펄스 수 설정
            for (int i = 0; i < pulses; i++) {
                digitalWrite(PULPin, HIGH);
                delayMicroseconds(pulse);
                digitalWrite(PULPin, LOW);
                delayMicroseconds(pulse);
            }
            Serial.println("done");  // 디버깅 메시지
        }
    }
}
