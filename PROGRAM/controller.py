import pygame
import time
from gpiozero import LED

# Initialize Pygame
pygame.init()

# Set up GPIO pins for controlling motors (LEDs to simulate motor control)
PIN_LEFT = 17  # Left motor pin
PIN_RIGHT = 18  # Right motor pin
PIN_FORWARD = 22  # Forward motor pin
PIN_REVERSE = 23  # Reverse motor pin

left_motor = LED(PIN_LEFT)  # Left motor control (ON/OFF)
right_motor = LED(PIN_RIGHT)  # Right motor control (ON/OFF)
forward_motor = LED(PIN_FORWARD)  # Forward motor control (ON/OFF)
reverse_motor = LED(PIN_REVERSE)  # Reverse motor control (ON/OFF)

# Set thresholds for detecting input
THRESHOLD = 0.1  # Ignore values below this threshold
DEADZONE = 0.1  # Small deadzone for joystick

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

        # Left/Right movement control
        if left_right > THRESHOLD:
            left_motor.on()  # Move left
            right_motor.off()  # Stop right
        elif left_right < -THRESHOLD:
            right_motor.on()  # Move right
            left_motor.off()  # Stop left
        else:
            left_motor.off()  # Stop left
            right_motor.off()  # Stop right

        # Forward/Reverse movement control
        if forward_reverse > THRESHOLD:
            forward_motor.on()  # Move forward
            reverse_motor.off()  # Stop reverse
        elif forward_reverse < -THRESHOLD:
            reverse_motor.on()  # Move reverse
            forward_motor.off()  # Stop forward
        else:
            forward_motor.off()  # Stop forward
            reverse_motor.off()  # Stop reverse

        # Print the values (debugging purposes)
        if left_right != 0 or forward_reverse != 0:
            print(f"Left/Right: {left_right}, Forward/Reverse: {forward_reverse}")

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program interrupted")

finally:
    pygame.quit()
