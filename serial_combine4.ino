#include <Arduino.h>

// 모터 제어 핀
const int RPWM1 = 2;  
const int LPWM1 = 3;
const int RPWM2 = 4;  
const int LPWM2 = 5;
const int RPWM3 = 6;  
const int LPWM3 = 7;
const int RPWM4 = 8;  
const int LPWM4 = 9;

// 속도 제어 핀
const int Speed1 = 10;

// 스테퍼 모터 제어 핀
const int ENAPin1 = 46;  
const int DIRPin1 = 45;
const int PULPin1 = 44;

const int ENAPin2 = 13;  
const int DIRPin2 = 12;
const int PULPin2 = 11;

// 펄스 딜레이 및 회전 스텝 수 조정
const int pulseDelay1 = 100;  // 각속도 (μs)
const int radius1 = 1500;     // 반경 (스텝 수)

// 현재 실행 중인 명령을 추적하기 위한 변수
bool isProcessing = false;
String currentCommand = "";

void setup() {
    // 핀 모드 설정
    pinMode(RPWM1, OUTPUT);
    pinMode(LPWM1, OUTPUT);
    pinMode(RPWM2, OUTPUT);
    pinMode(LPWM2, OUTPUT);
    pinMode(RPWM3, OUTPUT);
    pinMode(LPWM3, OUTPUT);
    pinMode(RPWM4, OUTPUT);
    pinMode(LPWM4, OUTPUT);
    pinMode(Speed1, OUTPUT);
    
    pinMode(ENAPin1, OUTPUT);
    pinMode(DIRPin1, OUTPUT);
    pinMode(PULPin1, OUTPUT);
    pinMode(ENAPin2, OUTPUT);
    pinMode(DIRPin2, OUTPUT);
    pinMode(PULPin2, OUTPUT);

    // 모터 드라이버 초기화
    digitalWrite(ENAPin1, LOW);  
    digitalWrite(DIRPin1, LOW);  
    digitalWrite(PULPin1, LOW);
    
    digitalWrite(ENAPin2, LOW);  
    digitalWrite(DIRPin2, LOW);  
    digitalWrite(PULPin2, LOW);

    Serial.begin(115200);  // 시리얼 통신 시작
    Serial.println("Arduino is ready.");
}

void rotateMotor1(bool direction, int steps) {
    Serial.println("Rotating Motor 1...");
    digitalWrite(DIRPin1, direction ? HIGH : LOW);
    for (int i = 0; i < steps; i++) {
        digitalWrite(PULPin1, HIGH);
        delayMicroseconds(pulseDelay1);
        digitalWrite(PULPin1, LOW);
        delayMicroseconds(pulseDelay1);
        
        // "STOP" 명령을 받을 경우 중단
        if (Serial.available() > 0) {
            String newCommand = Serial.readStringUntil('\n');
            newCommand.trim();
            if (newCommand == "STOP") {
                Serial.println("Stopping Motor 1 rotation.");
                isProcessing = false;
                return;
            }
        }
    }
}

void rotateMotor2(bool direction, int steps) {
    Serial.println("Rotating Motor 2...");
    digitalWrite(DIRPin2, direction ? HIGH : LOW);  
    for (int i = 0; i < steps; i++) {
        digitalWrite(PULPin2, HIGH);
        delayMicroseconds(pulseDelay1);
        digitalWrite(PULPin2, LOW);
        delayMicroseconds(pulseDelay1);
        
        // "STOP" 명령을 받을 경우 중단
        if (Serial.available() > 0) {
            String newCommand = Serial.readStringUntil('\n');
            newCommand.trim();
            if (newCommand == "STOP") {
                Serial.println("Stopping Motor 2 rotation.");
                isProcessing = false;
                return;
            }
        }
    }
}

void linearrotate1(bool direction, int speedValue, int duration) {
    Serial.println("Activating Linear Actuator 1...");
    if (direction) {
        // 하강
        digitalWrite(RPWM1, LOW);
        digitalWrite(LPWM1, HIGH);
    } else {
        // 상승
        digitalWrite(RPWM1, HIGH);
        digitalWrite(LPWM1, LOW);
    }

    analogWrite(Speed1, speedValue);
    unsigned long startTime = millis();
    while (millis() - startTime < duration) {
        // "STOP" 명령을 받을 경우 중단
        if (Serial.available() > 0) {
            String newCommand = Serial.readStringUntil('\n');
            newCommand.trim();
            if (newCommand == "STOP") {
                Serial.println("Stopping Linear Actuator 1.");
                analogWrite(Speed1, 0); // 모터 정지
                isProcessing = false;
                return;
            }
        }
    }
    analogWrite(Speed1, 0); // 동작 후 모터 정지
}

void linearrotate2(bool direction, int speedValue, int duration) {
    Serial.println("Activating Linear Actuator 2...");
    if (direction) {
        // 하강
        digitalWrite(RPWM2, LOW);
        digitalWrite(LPWM2, HIGH);
    } else {
        // 상승
        digitalWrite(RPWM2, HIGH);
        digitalWrite(LPWM2, LOW);
    }

    analogWrite(Speed1, speedValue);
    unsigned long startTime = millis();
    while (millis() - startTime < duration) {
        // "STOP" 명령을 받을 경우 중단
        if (Serial.available() > 0) {
            String newCommand = Serial.readStringUntil('\n');
            newCommand.trim();
            if (newCommand == "STOP") {
                Serial.println("Stopping Linear Actuator 2.");
                analogWrite(Speed1, 0); // 모터 정지
                isProcessing = false;
                return;
            }
        }
    }
    analogWrite(Speed1, 0); // 동작 후 모터 정지
}

void linearrotate3(bool direction, int speedValue, int duration) {
    Serial.println("Activating Linear Actuator 3...");
    if (direction) {
        // 하강
        digitalWrite(RPWM3, LOW);
        digitalWrite(LPWM3, HIGH);
    } else {
        // 상승
        digitalWrite(RPWM3, HIGH);
        digitalWrite(LPWM3, LOW);
    }

    analogWrite(Speed1, speedValue);
    unsigned long startTime = millis();
    while (millis() - startTime < duration) {
        // "STOP" 명령을 받을 경우 중단
        if (Serial.available() > 0) {
            String newCommand = Serial.readStringUntil('\n');
            newCommand.trim();
            if (newCommand == "STOP") {
                Serial.println("Stopping Linear Actuator 3.");
                analogWrite(Speed1, 0); // 모터 정지
                isProcessing = false;
                return;
            }
        }
    }
    analogWrite(Speed1, 0); // 동작 후 모터 정지
}

void linearrotate4(bool direction, int speedValue, int duration) {
    Serial.println("Activating Linear Actuator 4...");
    if (direction) {
        // 하강
        digitalWrite(RPWM4, LOW);
        digitalWrite(LPWM4, HIGH);
    } else {
        // 상승
        digitalWrite(RPWM4, HIGH);
        digitalWrite(LPWM4, LOW);
    }

    analogWrite(Speed1, speedValue);
    unsigned long startTime = millis();
    while (millis() - startTime < duration) {
        // "STOP" 명령을 받을 경우 중단
        if (Serial.available() > 0) {
            String newCommand = Serial.readStringUntil('\n');
            newCommand.trim();
            if (newCommand == "STOP") {
                Serial.println("Stopping Linear Actuator 4.");
                analogWrite(Speed1, 0); // 모터 정지
                isProcessing = false;
                return;
            }
        }
    }
    analogWrite(Speed1, 0); // 동작 후 모터 정지
}

void loop() {
    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');  // 명령 수신
        command.trim();  // 공백 제거
        Serial.println("Received Command: " + command);

        // 유효한 명령인지 확인
        if (command.length() == 0) {
            Serial.println("Empty command received. Ignoring...");
            return; // 빈 명령은 무시
        }

        // 현재 명령 처리 중인지 확인
        if (isProcessing) {
            Serial.println("Already processing a command. Ignoring new command.");
            return;
        }

        // 명령에 따른 동작 수행
        if (command == "M2C") {  // 캔
            Serial.println("Processing Plastic...");
            isProcessing = true;
            rotateMotor1(true, radius1);      // 열기
            delay(1000);
            rotateMotor1(false, radius1);     // 닫기
            delay(1000);
          //rotateMotor2(true, 1500);       == "M2G") {  // 유리
            Serial.println("Processing Glass...");
            isProcessing = true;
            rotateMotor1(true, radius1);
            delay(1000);
            rotateMotor1(false, radius1);  
            delay(1000);
            rotateMotor2(true, 1500);
            delay(1000);
            linearrotate2(false, 255, 6000);  // 하강
            delay(1000);
            linearrotate2(true, 255, 6000);   // 상승  
            isProcessing = false;
        }
        else if (command == "M2P") {  // 플라스틱
            Serial.println("Processing Can...");
            isProcessing = true;
            rotateMotor1(true, radius1);  
            delay(1000);
            rotateMotor1(false, radius1);
            delay(1000);
            rotateMotor2(true, 1500);
            delay(1000);
            linearrotate3(false, 255, 6000);  // 하강
            delay(1000);
            linearrotate3(true, 255, 6000);   // 상승  
            isProcessing = false;
        }
        else if (command == "M2PA") {  // 종이
            Serial.println("Processing Paper...");
            isProcessing = true;
            rotateMotor1(true, radius1);
            delay(1000);
            rotateMotor1(false, radius1);
            delay(1000);
            rotateMotor2(true, 1500);
            delay(1000);
            linearrotate4(false, 255, 6000);  // 하강
            delay(1000);
            linearrotate4(true, 255, 6000);   // 상승  
            isProcessing = false;
        }
        else if (command == "STOP") {  // 모든 동작 중지
            Serial.println("Stopping all actions...");
            // 현재 실행 중인 동작을 중지할 수 있는 로직 추가
            // 예: 모든 Speed1 핀을 LOW로 설정하여 모터 정지
            analogWrite(Speed1, 0);
            digitalWrite(RPWM1, LOW);
            digitalWrite(LPWM1, LOW);
            digitalWrite(RPWM2, LOW);
            digitalWrite(LPWM2, LOW);
            digitalWrite(RPWM3, LOW);
            digitalWrite(LPWM3, LOW);
            digitalWrite(RPWM4, LOW);
            digitalWrite(LPWM4, LOW);
            isProcessing = false;
        }
        else {
            Serial.println("Unknown command received. Ignoring...");
        }

        // 시리얼 버퍼 클리어 (추가)
        while (Serial.available() > 0) {
            Serial.read(); // 남아있는 데이터를 모두 읽어들여 버림
        }
    }
}
