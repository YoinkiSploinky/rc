import pygame
from gpiozero import PWMOutputDevice
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

# Define PWM pins (update these with your actual GPIO pin numbers)
PWM_PIN_LEFT = 12  # GPIO 12 for left motor
PWM_PIN_RIGHT = 13  # GPIO 13 for right motor
PWM_PIN_FORWARD = 17  # GPIO 17 for forward motor
PWM_PIN_REVERSE = 18  # GPIO 18 for reverse motor

# Initialize PWMOutputDevices
pwm_left = PWMOutputDevice(PWM_PIN_LEFT)
pwm_right = PWMOutputDevice(PWM_PIN_RIGHT)
pwm_forward = PWMOutputDevice(PWM_PIN_FORWARD)
pwm_reverse = PWMOutputDevice(PWM_PIN_REVERSE)

# Function to map joystick axis to PWM signal
def map_joystick_to_pwm(value, min_value=-1.0, max_value=1.0, min_pwm=0.0, max_pwm=1.0):
    return (value - min_value) / (max_value - min_value) * (max_pwm - min_pwm) + min_pwm

# Function to ignore small joystick movements
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
            pwm_left.value = map_joystick_to_pwm(left_value)  # Left motor moves forward when negative
            pwm_right.value = 0  # Right motor stops when moving left
            print(f"Moving left with value {left_value}")
        elif left_value > 0 and left_value != prev_left_value:  # Moving right
            pwm_right.value = map_joystick_to_pwm(left_value)  # Right motor moves forward when positive
            pwm_left.value = 0  # Left motor stops when moving right
            print(f"Moving right with value {left_value}")
        elif left_value == 0 and prev_left_value != 0:  # Stopped left/right
            pwm_left.value = 0  # Stop left motor if no left/right movement
            pwm_right.value = 0  # Stop right motor if no left/right movement
            print("Stopped left/right movement.")

        # Forward/Reverse Movement
        if forward_value < 0 and forward_value != prev_forward_value:  # Moving forward
            pwm_forward.value = map_joystick_to_pwm(forward_value)  # Forward motor moves forward when negative
            pwm_reverse.value = 0  # Reverse motor stops when moving forward
            print(f"Moving forward with value {forward_value}")
        elif forward_value > 0 and forward_value != prev_forward_value:  # Moving reverse
            pwm_reverse.value = map_joystick_to_pwm(forward_value)  # Reverse motor moves forward when positive
            pwm_forward.value = 0  # Forward motor stops when moving reverse
            print(f"Moving reverse with value {forward_value}")
        elif forward_value == 0 and prev_forward_value != 0:  # Stopped forward/reverse
            pwm_forward.value = 0  # Stop forward motor if no forward/reverse movement
            pwm_reverse.value = 0  # Stop reverse motor if no forward/reverse movement
            print("Stopped forward/reverse movement.")

        # Save previous values to avoid spamming
        prev_left_value = left_value
        prev_forward_value = forward_value

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program terminated by user.")
    pygame.quit()
