import time
import board
import neopixel

# 假設跟 DEVICE 同 SCALE (cm)
xmin = 18
xmax = 36
ymin = 3.5
ymax = 8.3

# Device Settings (cm)
DV_W = 36
DV_H = 25

# LED Strips Settings
LED_PIN1 = board.D18
LED_PIN2 = board.D21
STRIP_LED_COUNT = 15 # 一條燈條有幾顆 LED
STRIP_COUNT = 2 # 幾條燈條串連成統一控制
LED_COUNT = STRIP_LED_COUNT * STRIP_COUNT # 串聯後 LED 總數
BRIGHTNESS = 0.1
pixels1 = neopixel.NeoPixel(LED_PIN1, LED_COUNT, brightness=BRIGHTNESS)
pixels2 = neopixel.NeoPixel(LED_PIN2, LED_COUNT, brightness=BRIGHTNESS)
LED_INTVL = DV_H / (STRIP_LED_COUNT) # LED INTERVAL

def reset_led_color(pixels):
    pixels.fill((0, 0, 0))
    pixels.show()

def determine_col(x):
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

def determine_row(y):
    for i in range(STRIP_LED_COUNT):
        if ((i * LED_INTVL) <= y and y < ((i+1)*LED_INTVL)):
            return i
    # if can't find, then might hit the boundary of DV_H, return the last led index
    return STRIP_LED_COUNT - 1 

def light_area_leds(c_min, c_max, r_min, r_max, color):
    r_max += 1 # for calculating the diff and array indexing convenience
    r_diff = r_max - r_min
    for col in range(c_min, c_max+1):
        if (col == 1):
            pixels1[r_min:r_max] = [color] * r_diff
        elif (col == 2):
            pixels1[(STRIP_LED_COUNT+r_min):(STRIP_LED_COUNT+r_max)] = [color] * r_diff
        elif (col == 3):
            pixels2[r_min:r_max] = [color] * r_diff
        else:
            pixels2[(STRIP_LED_COUNT+r_min):(STRIP_LED_COUNT+r_max)] = [color] * r_diff


reset_led_color(pixels1)
reset_led_color(pixels2)

col_min = determine_col(xmin)
print(col_min)
col_max = determine_col(xmax)
print(col_max)
row_min = determine_row(ymin)
print(row_min)
row_max = determine_row(ymax)
print(row_max)


light_area_leds(col_min, col_max, row_min, row_max, (255,0,0))
    

pixels1.show()
pixels2.show()

reset_led_color(pixels1)
reset_led_color(pixels2)


