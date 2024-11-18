import time
import serial
from ultralytics import YOLO
import cv2

def initialize_serial(port='/dev/ttyACM0', baudrate=115200, timeout=1):
    try:
        ser = serial.Serial(port, baudrate, timeout=timeout)
        time.sleep(2)  # Arduino 초기화 대기
        print(f"Connected to Arduino on {port}")
        return ser
    except Exception as e:
        print(f"Failed to initialize serial port {port}: {e}")
        return None

def send_command(ser, command):
    if ser and ser.is_open:
        try:
            print(f"Sending Command: {command}")
            ser.write(f"{command}\n".encode())
        except Exception as e:
            print(f"Error while sending command: {e}")
    else:
        print("Serial port not open or not initialized.")

def load_model(weights_path):
    model = YOLO(weights_path)
    model.to('cpu')  # GPU 사용 시 'cuda'로 변경
    print("YOLO model loaded.")
    return model

def process_detections(detections, ser):
    plastic_items = ['pet']
    glass_items = ['glass_bottle']
    can_items = ['can']
    general_items = ['paper']
    allowed_classes = plastic_items + glass_items + can_items + general_items

    for detection in detections:
        name = detection['name']
        confidence = detection['confidence']

        if name in allowed_classes and confidence >= 0.5:
            print(f"Detected: {name} (confidence {confidence:.2f})")
            if name in plastic_items:
                send_command(ser, 'M2P')
            elif name in glass_items:
                send_command(ser, 'M2G')
            elif name in can_items:
                send_command(ser, 'M2C')
            elif name in general_items:
                send_command(ser, 'M2PA')
            time.sleep(5)  # 다음 감지 전 대기 시간
        else:
            print(f"Object '{name}' skipped (confidence {confidence:.2f}), below threshold (50%).")

def start_webcam_detection(model, ser):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to open webcam.")
        return

    print("Starting webcam detection. Press 'q' to exit.")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to read from webcam. Exiting.")
            break

        # YOLO 검출 수행
        results = model(frame)
        detections = []
        for result in results:
            for box in result.boxes:
                detections.append({
                    'class': int(box.cls[0]),
                    'name': model.names[int(box.cls[0])],
                    'confidence': box.conf[0].item()
                })

        # 검출 처리
        if detections:
            process_detections(detections, ser)

        # 프레임 표시 
        annotated_frame = results[0].plot()
        cv2.imshow("Webcam Detection", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Webcam detection stopped.")

if __name__ == '__main__':
    weights_path = '/home/capstone/yolo_env/7993_2best.pt'  # YOLO 가중치 경로
    serial_port = '/dev/ttyACM0'  # 필요 시 조정

    # 시리얼 연결 초기화
    ser = initialize_serial(port=serial_port, baudrate=115200, timeout=1)
    if not ser:
        raise RuntimeError("Failed to establish serial connection.")

    # YOLO 모델 로드
    model = load_model(weights_path)

    try:
        # 웹캠 검출 시작
        start_webcam_detection(model, ser)
    except KeyboardInterrupt:
        print("Detection interrupted.")
    finally:
        if ser:
            send_command(ser, 'STOP')  # 프로그램 종료 전에 STOP 명령 전송
            ser.close()
        print("Program terminated.")
