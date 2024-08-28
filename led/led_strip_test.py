import board
import neopixel
import time

# LED strip configuration:
LED_COUNT = 15       # Number of LED pixels.
LED_PIN = board.D23   # GPIO pin connected to the pixels (must support PWM).
ORDER = neopixel.GRB  # Pixel color channel order.

# Create a NeoPixel object:
pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness=0.1, auto_write=False, pixel_order=ORDER)

def set_color(color):
    pixels.fill(color)
    pixels.show()
pixels.fill((0, 0, 0))
# Example usage:
try:
    while True:
        # set_color((255, 0, 0))  # Red
        # time.sleep(1)
        # set_color((0, 255, 0))  # Green
        # time.sleep(1)
        # set_color((0, 0, 255))  # Blue
        # time.sleep(1)
        # Turn off all LEDs initially

        # Set the second LED (index 1) to red
        pixels[1] = (255, 0, 0)  # Red

        # Set the third LED (index 2) to blue
        pixels[2] = (0, 0, 255)  # Blue
        pixels.show()
except KeyboardInterrupt:
    pixels.fill((0, 0, 0))  # Turn off the LEDs
    pixels.show()