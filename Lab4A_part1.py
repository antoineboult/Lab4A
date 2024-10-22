from machine import Pin
import time

# They all have different purposes and functions
DS = Pin(20, Pin.OUT)
SHCP = Pin(18, Pin.OUT)
STCP = Pin(19, Pin.OUT)
OE = Pin(21, Pin.OUT)

# The off state, all lights are off (all values are 0)
off = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

# The "lights" matrix contains 16 bits for each light (4 directions with 4 lights each)
lights = [
    [1, 0, 0, 0],  # Light 1: Direction 1 (Green)
    [0, 1, 0, 0],  # Light 2: Direction 1 (Yellow)
    [0, 0, 1, 0],  # Light 3: Direction 1 (Red)
    [0, 0, 0, 1],  # Light 4: Direction 1 (White)

    [1, 0, 0, 0],  # Light 5: Direction 2 (Green)
    [0, 1, 0, 0],  # Light 6: Direction 2 (Yellow)
    [0, 0, 1, 0],  # Light 7: Direction 2 (Red)
    [0, 0, 0, 1],  # Light 8: Direction 2 (White)

    [1, 0, 0, 0],  # Light 9: Direction 3 (Green)
    [0, 1, 0, 0],  # Light 10: Direction 3 (Yellow)
    [0, 0, 1, 0],  # Light 11: Direction 3 (Red)
    [0, 0, 0, 1],  # Light 12: Direction 3 (White)

    [1, 0, 0, 0],  # Light 13: Direction 4 (Green)
    [0, 1, 0, 0],  # Light 14: Direction 4 (Yellow)
    [0, 0, 1, 0],  # Light 15: Direction 4 (Red)
    [0, 0, 0, 1]   # Light 16: Direction 4 (White)
]

# Function to output the light settings to the shift register
def shift_register_output(light_settings):
    # Shift out 16 bits to the shift register (1 by 1)
    for direction in light_settings:  # Iterate through the 4 directions
        for bit in direction:  # For each direction, there are 4 bits
            # Shift in all of the traffic light control bit values
            DS.value(bit)
            # Clock line
            SHCP.value(1)
            SHCP.value(0)
    # Latch the 16-bit value (stored into memory)
    STCP.value(1)
    STCP.value(0)
    OE.off()

# Function to sequentially turn on each light for 5 seconds
def sequential_lights(lights, delay=5):
    # lights is a list of 16 light states, we need to map each light back into the 4x4 matrix
    for i in range(16):  # Iterate over all 16 lights
        current_light = [[0, 0, 0, 0] for _ in range(4)]  # Start with all lights off
        direction = i // 4  # Determine which of the 4 directions (0 to 3)
        light_in_direction = i % 4  # Determine which light in the direction (0 to 3)
        current_light[direction][light_in_direction] = 1  # Turn on the appropriate light
        
        # Print which light is on
        print(f"Light {i+1} is on")
        
        shift_register_output(current_light)  # Output the current light state
        time.sleep(delay)  # Keep the light on for the specified delay
        shift_register_output(off)  # Turn all lights off before moving to the next
        time.sleep(0.5)  # Small delay before switching to the next light

# Call the sequential lights function
print("The light program is running...")
sequential_lights(lights)
print("Done! All of the lights were turned on.")
