# -*- coding: utf-8 -*-
import cv2
import torch

# YOLOv5 �� �ε� (���� �н��� �� ��θ� �����ؾ� ��)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

def main():
    cap = cv2.VideoCapture(0)  # ��ķ ���� (0�� ī�޶�)

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # YOLO �߷� ����
        results = model(frame)

        # ��� �̹��� ��������
        result_img = results.render()[0]

        # ��� ȭ�� ���
        cv2.imshow('YOLO Inference', result_img)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
