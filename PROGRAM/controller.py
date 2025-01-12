import pygame
from gpiozero import PWMOutputDevice
import time

# Initialize pygame
pygame.init()

# Define GPIO pins for PWM (GPIOs with PWM support on Pi Zero)
PWM_PIN_FORWARD = 12  # PWM pin for Forward (example)
PWM_PIN_REVERSE = 13  # PWM pin for Reverse (example)
PWM_PIN_LEFT = 18     # PWM pin for Left (example)
PWM_PIN_RIGHT = 19    # PWM pin for Right (example)

pwm_forward = PWMOutputDevice(PWM_PIN_FORWARD)
pwm_reverse = PWMOutputDevice(PWM_PIN_REVERSE)
pwm_left = PWMOutputDevice(PWM_PIN_LEFT)
pwm_right = PWMOutputDevice(PWM_PIN_RIGHT)

# Set deadzone
DEADZONE = 300  # Adjust this based on the joystick response

def map_joystick_to_pwm(axis_value, deadzone):
    # Apply deadzone: ignore values within the deadzone
    if abs(axis_value) < deadzone:
        return 0
    # Map to PWM range [0, 1] from joystick values [-32767, 32767]
    pwm_value = max(0, min(1, (axis_value - deadzone) / (32767 - deadzone) if axis_value > 0 else (axis_value + deadzone) / (32767 - deadzone)))
    return pwm_value

# Initialize the joystick (assuming it's the first joystick)
joystick = pygame.joystick.Joystick(0)
joystick.init()

def read_controller():
    print("Reading controller input...")
    while True:
        pygame.event.pump()  # Process joystick events

        # Get axis values
        x_axis_value = joystick.get_axis(0)  # Left-right axis
        y_axis_value = joystick.get_axis(1)  # Up-down axis

        # Map joystick values to PWM and control motors
        if x_axis_value > 0:
            pwm_left.value = 0  # No left movement
            pwm_right.value = map_joystick_to_pwm(x_axis_value * 32767, DEADZONE)
            print(f"Moving right with value {x_axis_value}")
        elif x_axis_value < 0:
            pwm_right.value = 0  # No right movement
            pwm_left.value = map_joystick_to_pwm(-x_axis_value * 32767, DEADZONE)
            print(f"Moving left with value {x_axis_value}")
        else:
            pwm_left.value = 0
            pwm_right.value = 0

        if y_axis_value > 0:
            pwm_forward.value = 0  # No forward movement
            pwm_reverse.value = map_joystick_to_pwm(y_axis_value * 32767, DEADZONE)
            print(f"Moving reverse with value {y_axis_value}")
        elif y_axis_value < 0:
            pwm_reverse.value = 0  # No reverse movement
            pwm_forward.value = map_joystick_to_pwm(-y_axis_value * 32767, DEADZONE)
            print(f"Moving forward with value {y_axis_value}")
        else:
            pwm_forward.value = 0
            pwm_reverse.value = 0

        time.sleep(0.1)  # Small delay to avoid high CPU usage

if __name__ == "__main__":
    try:
        read_controller()
    except KeyboardInterrupt:
        pass
    finally:
        pwm_forward.off()
        pwm_reverse.off()
        pwm_left.off()
        pwm_right.off()
