import time
import cv2
import numpy as np
import torch
from pathlib import Path
from models.common import DetectMultiBackend
from utils.general import check_img_size, non_max_suppression, scale_boxes
from utils.torch_utils import select_device
import gpiod
from gpiod.line import Direction, Value

# Initialize the GPIO chip
def initialize_gpio():
    try:
        chip = gpiod.Chip('/dev/gpiochip4')  # Use the correct GPIO chip
        return chip
    except Exception as e:
        print(f"Failed to initialize GPIO chip: /dev/gpiochip4, Error: {e}")
        return None

# Request a specific GPIO line
def request_line(chip, line_offset, direction):
    try:
        line_settings = gpiod.LineSettings()
        line_settings.direction = direction
        request = chip.request_lines(
            consumer="yolo_motor_test5",
            config={line_offset: line_settings}
        )
        return request
    except Exception as e:
        print(f"Failed to request line {line_offset} on chip, Error: {e}")
        return None

# Initialize GPIO chip
chip = initialize_gpio()
if not chip:
    raise RuntimeError("GPIO chip initialization failed.")

# Request motor lines
ena1_line = request_line(chip, 17, Direction.OUTPUT)  # green
dir1_line = request_line(chip, 22, Direction.OUTPUT)  # yellow
pul1_line = request_line(chip, 27, Direction.OUTPUT)  # orange
ena2_line = request_line(chip, 23, Direction.OUTPUT)  # red
dir2_line = request_line(chip, 24, Direction.OUTPUT)  # purple
pul2_line = request_line(chip, 25, Direction.OUTPUT)  # blue

if not all([ena1_line, dir1_line, pul1_line, ena2_line, dir2_line, pul2_line]):
    raise RuntimeError("One or more GPIO lines failed to initialize.")

# Activate ENA pins (if necessary)
ena1_line.set_values({17: Value.INACTIVE})
ena2_line.set_values({23: Value.INACTIVE})

# Function to rotate motor1 forward
def rotate_motor1_forward(dir_line, pul_line, pulses, delay=0.001):
    print(f"Rotating motor 1 forward for {pulses} pulses")
    dir_line.set_values({dir_line.offsets[0]: Value.ACTIVE})
    for _ in range(pulses):
        pul_line.set_values({pul_line.offsets[0]: Value.ACTIVE})
        time.sleep(delay)
        pul_line.set_values({pul_line.offsets[0]: Value.INACTIVE})
        time.sleep(delay)
    print("Motor 1 forward rotation complete")

# Function to rotate motor1 backward
def rotate_motor1_backward(dir_line, pul_line, pulses, delay=0.001):
    print(f"Rotating motor 1 backward for {pulses} pulses")
    dir_line.set_values({dir_line.offsets[0]: Value.INACTIVE})
    for _ in range(pulses):
        pul_line.set_values({pul_line.offsets[0]: Value.ACTIVE})
        time.sleep(delay)
        pul_line.set_values({pul_line.offsets[0]: Value.INACTIVE})
        time.sleep(delay)
    print("Motor 1 backward rotation complete")

# Function to rotate motor2
def rotate_motor2(dir_line, pul_line, pulses, delay=0.001):
    print(f"Rotating motor 2 for {pulses} pulses")
    dir_line.set_values({dir_line.offsets[0]: Value.ACTIVE})
    for _ in range(pulses):
        pul_line.set_values({pul_line.offsets[0]: Value.ACTIVE})
        time.sleep(delay)
        pul_line.set_values({pul_line.offsets[0]: Value.INACTIVE})
        time.sleep(delay)
    print("Motor 2 rotation complete")

# Initialize YOLOv5 model
def initialize_model():
    model_dir = Path('/home/casptone/Downloads/yolov5-master')
    weight_files = list(model_dir.glob('best*.pt'))
    
    if not weight_files:
        raise FileNotFoundError("No 'best*.pt' files found in the directory")

    device = select_device('cpu')
    half = device.type != 'cpu'

    models = []
    for weights in weight_files:
        model = DetectMultiBackend(weights, device=device, dnn=False)
        stride, names, pt = model.stride, model.names, model.pt
        imgsz = check_img_size((640, 640), s=stride)
        model.warmup(imgsz=(1 if pt else 1, 3, *imgsz))
        models.append((model, names))

    return models, device, half, imgsz

# Capture and detect objects
def capture_and_detect(models, device, half, imgsz):
    cap = cv2.VideoCapture(0)
    frame_interval = 1
    last_processed_time = time.time()
    previous_detections = set()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        current_time = time.time()
        if current_time - last_processed_time < frame_interval:
            continue
        last_processed_time = current_time

        img = cv2.resize(frame, (640, 640))
        img = img[:, :, ::-1]
        img = img.transpose(2, 0, 1)
        img = np.ascontiguousarray(img)

        im = torch.from_numpy(img).to(device)
        im = im.half() if half else im.float()
        im /= 255
        if len(im.shape) == 3:
            im = im[None]

        current_detections = set()
        for model, names in models:
            pred = model(im)
            pred = non_max_suppression(pred, 0.25, 0.45, None, False, max_det=1000)

            for i, det in enumerate(pred):
                if len(det):
                    det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], frame.shape).round()
                    for *xyxy, conf, cls in reversed(det):
                        c = int(cls)
                        current_detections.add(names[c])

        if len(current_detections) > 1:
            print("Multiple objects detected, skipping motor actions.")
        else:
            disappeared_objects = previous_detections - current_detections
            new_objects = current_detections - previous_detections

            if new_objects:
                print(f"New detected objects: {', '.join(new_objects)}")
                run_motor_simulation(new_objects, action='detected')

            if disappeared_objects:
                print(f"Disappeared objects: {', '.join(disappeared_objects)}")
                run_motor_simulation(disappeared_objects, action='disappeared')

        previous_detections = current_detections

    cap.release()
    cv2.destroyAllWindows()

# Function to run motor simulation
def run_motor_simulation(detections, action='detected'):
    plastic_items = ['pet']
    glass_items = ['glass_bottle']
    can_items = ['can']
    general_items = ['paper']

    allowed_items = set(plastic_items + glass_items + can_items + general_items)

    for item in detections:
        if item not in allowed_items:
            print(f"Detected object '{item}' is not in the allowed list. Skipping motor actions.")
            continue

        time.sleep(1.5)
        if action == 'detected':
            # Rotate motor1 forward, then backward, then rotate motor2
            rotate_motor1_forward(dir1_line, pul1_line, 1000, delay=0.001)  # Motor 1 forward
            time.sleep(1)
            rotate_motor1_backward(dir1_line, pul1_line, 1000, delay=0.001)  # Motor 1 backward
            time.sleep(1)
            if item in plastic_items:
                print('Motor action on pet')
                rotate_motor2(dir2_line, pul2_line, 400, delay=0.001)  # Motor 2 action
                time.sleep(2)
            elif item in glass_items:
                print('Motor action on glass')
                rotate_motor2(dir2_line, pul2_line, 300, delay=0.001)  # Motor 2 action
                time.sleep(2)
            elif item in can_items:
                print('Motor action on can')
                rotate_motor2(dir2_line, pul2_line, 200, delay=0.001)  # Motor 2 action
                time.sleep(2)
            elif item in general_items:
                print('Motor action on paper')
                rotate_motor2(dir2_line, pul2_line, 100, delay=0.001)  # Motor 2 action
                time.sleep(2)
        elif action == 'disappeared':
            pass

# Main function
if __name__ == '__main__':
    models, device, half, imgsz = initialize_model()
    print("YOLOv5 initialized")
    capture_and_detect(models, device, half, imgsz)
    print("complete")
