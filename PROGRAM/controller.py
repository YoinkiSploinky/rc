import pygame
import time
from gpiozero import PWMOutputDevice

# Initialize Pygame
pygame.init()

# Set up PWM for controlling motors (GPIO pins)
PWM_PIN_LEFT = 17  # Left motor PWM pin
PWM_PIN_RIGHT = 18  # Right motor PWM pin

pwm_left = PWMOutputDevice(PWM_PIN_LEFT, frequency=100)  # 100Hz frequency
pwm_right = PWMOutputDevice(PWM_PIN_RIGHT, frequency=100)  # 100Hz frequency

# Set deadzone threshold (ignores values above 0.8 or below -0.8)
DEADZONE_MIN = -0.8
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

        # Apply deadzone (ignore values above 0.8 or below -0.8)
        if left_right > DEADZONE_MAX or left_right < DEADZONE_MIN:
            left_right = 0.0  # Ignore input if it's outside the range
        if forward_reverse > DEADZONE_MAX or forward_reverse < DEADZONE_MIN:
            forward_reverse = 0.0  # Ignore input if it's outside the range

        # Control left motor (forward/reverse)
        if forward_reverse < 0:
            pwm_left.value = abs(forward_reverse)  # Forward
        elif forward_reverse > 0:
            pwm_left.value = abs(forward_reverse)  # Reverse
        else:
            pwm_left.value = 0  # Stop

        # Control right motor (left/right)
        if left_right < 0:
            pwm_right.value = abs(left_right)  # Move left
        elif left_right > 0:
            pwm_right.value = abs(left_right)  # Move right
        else:
            pwm_right.value = 0  # Stop

        # Print the values (debugging purposes)
        if left_right != 0 or forward_reverse != 0:
            print(f"Left/Right: {left_right}, Forward/Reverse: {forward_reverse}")

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program interrupted")

finally:
    pygame.quit()
