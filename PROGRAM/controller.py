import pygame
import time
from gpiozero import LED

# Initialize Pygame
pygame.init()

# Set up GPIO pins for controlling motors (LEDs to simulate motor control)
PIN_LEFT = 17  # Left motor pin
PIN_RIGHT = 18  # Right motor pin

left_motor = LED(PIN_LEFT)  # Left motor control (ON/OFF)
right_motor = LED(PIN_RIGHT)  # Right motor control (ON/OFF)

# Set thresholds for detecting input
THRESHOLD_MIN = 0.1
THRESHOLD_MAX = 0.8
DEADZONE_MIN = -0.1
DEADZONE_MAX = 0.8

# Initialize joystick
pygame.joystick.init()
if pygame.joystick.get_count() < 1:
    print("No joystick found!")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

# Main loop
try:
    while True:
        pygame.event.pump()

        # Read the joystick axes (left/right and forward/reverse)
        left_right = joystick.get_axis(0)  # Left/Right axis (X-axis)
        forward_reverse = joystick.get_axis(1)  # Forward/Reverse axis (Y-axis)

        # Check if left/right axis is within threshold for left/right movement
        if left_right > THRESHOLD_MIN and left_right < THRESHOLD_MAX:
            left_motor.on()  # Move left
        elif left_right < DEADZONE_MIN and left_right > -DEADZONE_MAX:
            left_motor.on()  # Move right
        else:
            left_motor.off()  # Stop

        # Check if forward/reverse axis is within threshold for forward/reverse movement
        if forward_reverse > THRESHOLD_MIN and forward_reverse < THRESHOLD_MAX:
            right_motor.on()  # Move forward
        elif forward_reverse < DEADZONE_MIN and forward_reverse > -DEADZONE_MAX:
            right_motor.on()  # Move reverse
        else:
            right_motor.off()  # Stop

        # Print the values (debugging purposes)
        if left_right != 0 or forward_reverse != 0:
            print(f"Left/Right: {left_right}, Forward/Reverse: {forward_reverse}")

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program interrupted")

finally:
    pygame.quit()
