import inputs
import time
from gpiozero import PWMLED, Device
from gpiozero.pins.native import NativeGPIOPin
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero.pins.rpigpio import RPiGPIOFactory

# Ensure all pins are supported before use.
# Use PiGPIO or RPi.GPIO if available; otherwise, fallback to native GPIO.

try:
    # Try to use PiGPIO (hardware PWM support)
    from gpiozero.pins.pigpio import PiGPIOFactory
    Device.pin_factory = PiGPIOFactory()
    print("Using PiGPIO for hardware PWM")
except ImportError:
    try:
        # Fall back to RPi.GPIO if PiGPIO is not available
        from gpiozero.pins.rpigpio import RPiGPIOFactory
        Device.pin_factory = RPiGPIOFactory()
        print("Using RPi.GPIO for hardware PWM")
    except ImportError:
        # Fall back to Native GPIO if no hardware PWM factory found
        Device.pin_factory = NativeGPIOPin()
        print("Using Native GPIO (Software PWM)")

# GPIO pin definitions for PWM (choose PWM-capable pins)
PWM_PIN_FORWARD = 18  # Hardware PWM pin (GPIO18)
PWM_PIN_REVERSE = 19  # Hardware PWM pin (GPIO19)
PWM_PIN_LEFT = 16     # Software PWM pin (GPIO16)
PWM_PIN_RIGHT = 17    # Software PWM pin (GPIO17)

# Set up PWM devices (either hardware or software based)
pwm_forward = PWMLED(PWM_PIN_FORWARD)
pwm_reverse = PWMLED(PWM_PIN_REVERSE)
pwm_left = PWMLED(PWM_PIN_LEFT)
pwm_right = PWMLED(PWM_PIN_RIGHT)

# Deadzone settings
DEADZONE = 300  # Deadzone size in joystick value (adjustable)

def map_joystick_to_pwm(axis_value, deadzone):
    """Maps joystick axis values to PWM duty cycle."""
    # Apply deadzone: ignore values within the deadzone
    if abs(axis_value) < deadzone:
        return 0  # Neutral position

    # Map the joystick value (from -32767 to 32767) to a PWM duty cycle (0 to 1)
    if axis_value > 0:
        pwm_value = (axis_value - deadzone) / (32767 - deadzone) * 1
    else:
        pwm_value = (axis_value + deadzone) / (32767 - deadzone) * 1

    # Ensure the PWM value is within the range [0, 1]
    pwm_value = max(0, min(1, pwm_value))
    return pwm_value

def read_controller():
    """Reads the joystick/controller input and maps it to PWM signals."""
    print("Starting to read the controller inputs...")
    while True:
        events = inputs.get_key()  # Get input events (button presses, joystick movements, etc.)
        for event in events:
            if event.ev_type == 'Absolute':
                if event.ev_code == 'ABS_X':  # X-axis (left-right)
                    x_axis_value = event.ev_value
                    # Map to PWM and update the right/left motors
                    if x_axis_value > 0:
                        pwm_left.value = 0  # No left movement
                        pwm_right.value = map_joystick_to_pwm(x_axis_value, DEADZONE)
                        print(f"Moving right with value {x_axis_value}")
                    elif x_axis_value < 0:
                        pwm_right.value = 0  # No right movement
                        pwm_left.value = map_joystick_to_pwm(-x_axis_value, DEADZONE)
                        print(f"Moving left with value {x_axis_value}")
                    else:
                        # If it's neutral, turn both off
                        pwm_left.value = 0
                        pwm_right.value = 0

                elif event.ev_code == 'ABS_Y':  # Y-axis (forward-reverse)
                    y_axis_value = event.ev_value
                    # Map to PWM and update the forward/reverse motors
                    if y_axis_value > 0:
                        pwm_forward.value = 0  # No forward movement
                        pwm_reverse.value = map_joystick_to_pwm(y_axis_value, DEADZONE)
                        print(f"Moving reverse with value {y_axis_value}")
                    elif y_axis_value < 0:
                        pwm_reverse.value = 0  # No reverse movement
                        pwm_forward.value = map_joystick_to_pwm(-y_axis_value, DEADZONE)
                        print(f"Moving forward with value {y_axis_value}")
                    else:
                        # If it's neutral, turn both off
                        pwm_forward.value = 0
                        pwm_reverse.value = 0

        time.sleep(0.1)  # Small delay to avoid high CPU usage

if __name__ == "__main__":
    try:
        read_controller()
    except KeyboardInterrupt:
        pass
    finally:
        # Cleanup PWM settings (turn off all PWM devices)
        pwm_forward.off()
        pwm_reverse.off()
        pwm_left.off()
        pwm_right.off()
        print("Cleanup done.")
