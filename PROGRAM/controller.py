import pygame
from gpiozero import LED
import time

# Initialize pygame and joystick
pygame.init()
pygame.joystick.init()

# Check if joystick is connected
if pygame.joystick.get_count() == 0:
    print("No joystick detected!")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

# Define GPIO pins for the motors
PIN_LEFT = 12  # GPIO 12 for left motor
PIN_RIGHT = 13  # GPIO 13 for right motor
PIN_FORWARD = 17  # GPIO 17 for forward motor
PIN_REVERSE = 18  # GPIO 18 for reverse motor

# Initialize LED objects (to control the motors)
left_motor = LED(PIN_LEFT)
right_motor = LED(PIN_RIGHT)
forward_motor = LED(PIN_FORWARD)
reverse_motor = LED(PIN_REVERSE)

# Function to apply deadzone to joystick values
def apply_deadzone(value, deadzone=0.01):
    if abs(value) < deadzone:
        return 0.0  # Ignore small movements
    return value

# Track previous values to reduce spamming
prev_left_value = 0.0
prev_forward_value = 0.0

# Main loop
try:
    while True:
        pygame.event.pump()  # Process events
        
        # Get joystick axis values (left-right and forward-backward)
        left_value = joystick.get_axis(0)  # Axis 0: Left/Right (X axis)
        forward_value = joystick.get_axis(1)  # Axis 1: Forward/Backward (Y axis)

        # Apply deadzone to joystick values
        left_value = apply_deadzone(left_value)
        forward_value = apply_deadzone(forward_value)

        # Left/Right Movement
        if left_value < 0 and left_value != prev_left_value:  # Moving left
            left_motor.on()  # Turn left motor ON
            right_motor.off()  # Turn right motor OFF
            print(f"Moving left with value {left_value}")
        elif left_value > 0 and left_value != prev_left_value:  # Moving right
            right_motor.on()  # Turn right motor ON
            left_motor.off()  # Turn left motor OFF
            print(f"Moving right with value {left_value}")
        elif left_value == 0 and prev_left_value != 0:  # Stopped left/right
            left_motor.off()  # Stop left motor
            right_motor.off()  # Stop right motor
            print("Stopped left/right movement.")

        # Forward/Reverse Movement
        if forward_value < 0 and forward_value != prev_forward_value:  # Moving forward
            forward_motor.on()  # Turn forward motor ON
            reverse_motor.off()  # Turn reverse motor OFF
            print(f"Moving forward with value {forward_value}")
        elif forward_value > 0 and forward_value != prev_forward_value:  # Moving reverse
            reverse_motor.on()  # Turn reverse motor ON
            forward_motor.off()  # Turn forward motor OFF
            print(f"Moving reverse with value {forward_value}")
        elif forward_value == 0 and prev_forward_value != 0:  # Stopped forward/reverse
            forward_motor.off()  # Stop forward motor
            reverse_motor.off()  # Stop reverse motor
            print("Stopped forward/reverse movement.")

        # Save previous values to avoid spamming
        prev_left_value = left_value
        prev_forward_value = forward_value

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program terminated by user.")
    pygame.quit()
