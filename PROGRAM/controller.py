import pygame
import time

# Initialize pygame
pygame.init()

# Check the number of joysticks connected
joystick_count = pygame.joystick.get_count()
print(f"Number of joysticks detected: {joystick_count}")

if joystick_count > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
else:
    print("No joystick found")
    pygame.quit()
    exit()

# Loop to read joystick inputs
print("Reading controller input...")

try:
    while True:
        pygame.event.pump()  # Refresh the joystick state

        # Read joystick axis values (left-right, up-down)
        x_axis = joystick.get_axis(0)  # Left/Right Axis
        y_axis = joystick.get_axis(1)  # Up/Down Axis

        # Read button values (if needed, e.g., button 0, 1)
        button_0 = joystick.get_button(0)  # Button 0 press
        button_1 = joystick.get_button(1)  # Button 1 press

        # Print axis movements (values range from -1.0 to 1.0)
        if abs(x_axis) > 0.1 or abs(y_axis) > 0.1:  # Only print if the axis moves
            print(f"Moving left with value {x_axis}")
            print(f"Moving forward with value {y_axis}")

        # Example: Stop if button 0 is pressed
        if button_0:
            print("Button 0 pressed, stopping...")
            break

        time.sleep(0.1)  # Slight delay to prevent overloading the output

except KeyboardInterrupt:
    print("Program terminated by user.")

finally:
    pygame.quit()
