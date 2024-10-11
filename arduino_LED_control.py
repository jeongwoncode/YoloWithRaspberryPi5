import serial
import time

# Function to find available serial ports
def find_arduino_port():
    possible_ports = ['/dev/ttyUSB0', '/dev/ttyAMA0', '/dev/ttyS0']
    for port in possible_ports:
        try:
            arduino = serial.Serial(port, 9600)
            time.sleep(2)  # Wait for the connection to initialize
            return arduino
        except serial.SerialException:
            continue
    raise serial.SerialException("Could not find an available Arduino port.")

# Initialize serial connection to Arduino
arduino = find_arduino_port()

def blink_led(times, delay=1):
    for _ in range(times):
        arduino.write(b'1')  # Send signal to turn LED on
        time.sleep(delay)
        arduino.write(b'0')  # Send signal to turn LED off
        time.sleep(delay)

if __name__ == "__main__":
    while True:
        command = input("Enter 'b' to blink the LED or 'q' to quit: ")
        if command == 'b':
            blink_led(5, 0.5)  # Blink the LED 5 times with 0.5 second delay
        elif command == 'q':
            break

    arduino.close()