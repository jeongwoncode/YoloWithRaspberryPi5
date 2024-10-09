import gpiod

def test_gpiod_chip(chip_path):
    try:
        chip = gpiod.Chip(chip_path)
        print(f"Successfully accessed {chip_path}")
    except Exception as e:
        print(f"Error accessing {chip_path}: {e}")

test_gpiod_chip('/dev/gpiochip0')
test_gpiod_chip('/dev/gpiochip1')
test_gpiod_chip('/dev/gpiochip2')
test_gpiod_chip('/dev/gpiochip3')
test_gpiod_chip('/dev/gpiochip4')
