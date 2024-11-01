# -*- coding: utf-8 -*-
import cv2
import torch

# YOLOv5 모델 로드 (사전 학습된 모델 경로를 설정해야 함)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

def main():
    cap = cv2.VideoCapture(0)  # 웹캠 연결 (0번 카메라)

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # YOLO 추론 수행
        results = model(frame)

        # 결과 이미지 가져오기
        result_img = results.render()[0]

        # 결과 화면 출력
        cv2.imshow('YOLO Inference', result_img)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
