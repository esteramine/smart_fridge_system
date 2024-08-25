import time
import board
import neopixel

# 假設跟 DEVICE 同 SCALE (cm)
xmin = 20
xmax = 35

# Device Settings (cm)
DV_W = 36
DV_H = 25

# LED Strips Settings
LED_PIN1 = board.D18
LED_PIN2 = board.D21
LED_COUNT = 30
BRIGHTNESS = 0.1
pixels1 = neopixel.NeoPixel(LED_PIN1, LED_COUNT, brightness=BRIGHTNESS)
pixels2 = neopixel.NeoPixel(LED_PIN2, LED_COUNT, brightness=BRIGHTNESS)

def reset_led_color(pixels):
    pixels.fill((0, 0, 0))
    pixels.show()

def determine_area(x):
    # Area 1
    if (0 <= x and x < (DV_W/4)):
        return 1
    # Area 2
    elif ((DV_W/4) <= x and x < (DV_W/2)):
        return 2
    # Area 3
    elif ((DV_W/2) <= x and x < ((3 * DV_W)/4)):
        return 3
    # Area 4
    else:
        return 4

def light_area_leds(area, color):
    if (area == 1):
        pixels1[:15] = [color] * LED_COUNT
    elif (area == 2):
        pixels1[15:30] = [color] * LED_COUNT
    elif (area == 3):
        pixels2[:15] = [color] * LED_COUNT
    else:
        pixels2[15:30] = [color] * LED_COUNT


reset_led_color(pixels1)
reset_led_color(pixels2)

xmin_area = determine_area(xmin)
print(xmin_area)
xmax_area = determine_area(xmax)
print(xmax_area)

for i in range(xmin_area, xmax_area+1):
    light_area_leds(i, (255,0,0))
    

pixels1.show()
pixels2.show()

reset_led_color(pixels1)
reset_led_color(pixels2)


