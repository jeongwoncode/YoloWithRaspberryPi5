import gpiod
import time
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
def rotate_motor1_forward(dir_line, pul_line, pulses, delay=0.0005):
    print(f"Rotating motor 1 forward for {pulses} pulses")
    dir_line.set_values({dir_line.offsets[0]: Value.ACTIVE})  # Set direction to forward
    for _ in range(pulses):
        pul_line.set_values({pul_line.offsets[0]: Value.ACTIVE})
        time.sleep(delay)
        pul_line.set_values({pul_line.offsets[0]: Value.INACTIVE})
        time.sleep(delay)
    print("Motor 1 forward rotation complete")



# Execute motor rotation and measure execution time
pulses = 190  # Number of pulses for the motor to rotate

# Measure and execute forward rotation
start_time = time.time()
rotate_motor1_forward(dir1_line, pul1_line, pulses)
end_time = time.time()
print(f"Motor 1 forward rotation time: {end_time - start_time:.4f} seconds")
