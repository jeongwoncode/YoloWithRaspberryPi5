# -*- coding: utf-8 -*-
import gpiod

# GPIO ? ??? ????
chip = gpiod.Chip('gpiochip0')  # ???? GPIO ? ???? ??еч? ????

# GPIO ???? ???? ???
def get_line(pin_number):
    line = chip.get_line(pin_number)
    config = gpiod.line_request()
    config.consumer = 'motor_control'
    config.request_type = gpiod.line_request.DIRECTION_OUTPUT
    line.request(config)
    return line

# ?????? GPIO ????
test_line = get_line(17)  # green

# ???? ????
test_line.set_value(1)
print("GPIO 17 set to HIGH")
test_line.set_value(0)
print("GPIO 17 set to LOW")
