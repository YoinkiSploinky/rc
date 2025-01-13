import pygame
import time
from gpiozero import LED

# Initialize Pygame without video (only joystick)
pygame.joystick.init()  # Initialize joystick system only

if pygame.joystick.get_count() == 0:
    print("No joystick connected dumbass!")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

print("Joystick connected, buenos dias puta!")

# GPIO pins setup
PIN_LEFT = 18
PIN_RIGHT = 13
PIN_FORWARD = 17
PIN_REVERSE = 27

left_motor = LED(PIN_LEFT)
right_motor = LED(PIN_RIGHT)
forward_motor = LED(PIN_FORWARD)
reverse_motor = LED(PIN_REVERSE)

def apply_deadzone(value, deadzone=0.1):
    if abs(value) < deadzone:
        return 0.0
    return value

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
        if left_value < 0:  # Moving left
            left_motor.on()  # Turn left motor ON
            right_motor.off()  # Turn right motor OFF
            print(f"Moving left with value {left_value}")
        elif left_value > 0:  # Moving right
            right_motor.on()  # Turn right motor ON
            left_motor.off()  # Turn left motor OFF
            print(f"Moving right with value {left_value}")
        else:  # Stopped left/right
            left_motor.off()  # Stop left motor
            right_motor.off()  # Stop right motor
            print("Stopped left/right movement.")

        # Forward/Reverse Movement
        if forward_value < 0:  # Moving forward
            forward_motor.on()  # Turn forward motor ON
            reverse_motor.off()  # Turn reverse motor OFF
            print(f"Moving forward with value {forward_value}")
        elif forward_value > 0:  # Moving reverse
            reverse_motor.on()  # Turn reverse motor ON
            forward_motor.off()  # Turn forward motor OFF
            print(f"Moving reverse with value {forward_value}")
        else:  # Stopped forward/reverse
            forward_motor.off()  # Stop forward motor
            reverse_motor.off()  # Stop reverse motor
            print("Stopped forward/reverse movement.")

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program terminated by user.")
    pygame.quit()  # Quit pygame properly
