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
PWM_PIN_LEFT = 12  # GPIO 12 for left movement (example pin)
PWM_PIN_RIGHT = 13  # GPIO 13 for right movement (example pin)
PWM_PIN_FORWARD = 17  # GPIO 17 for forward movement (example pin)
PWM_PIN_REVERSE = 18  # GPIO 18 for reverse movement (example pin)

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

        # Print values to verify them
        print(f"Moving left with value {left_value}")
        print(f"Moving forward with value {forward_value}")

        # Adjust PWM signals based on joystick input
        pwm_left.value = map_joystick_to_pwm(left_value)
        pwm_right.value = map_joystick_to_pwm(-left_value)  # Reverse direction for right motor
        pwm_forward.value = map_joystick_to_pwm(-forward_value)  # Reverse direction for forward movement
        pwm_reverse.value = map_joystick_to_pwm(forward_value)  # Reverse direction for reverse movement

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program terminated by user.")
    pygame.quit()
