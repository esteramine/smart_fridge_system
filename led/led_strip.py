import time
import board
import neopixel

# 假設跟 DEVICE 同 SCALE (cm)
# xmin = 18
# xmax = 36
# ymin = 3.5
# ymax = 8.3

# Device Settings (cm)
DV_W = 44
DV_H = 25

# LED Strips Settings
LED_PIN1 = board.D18
LED_PIN2 = board.D21
STRIP_LED_COUNT = 15 # 一條燈條有幾顆 LED
STRIP_COUNT = 2 # 幾條燈條串連成統一控制
LED_COUNT = STRIP_LED_COUNT * STRIP_COUNT # 串聯後 LED 總數
BRIGHTNESS = 0.5
pixels1 = neopixel.NeoPixel(LED_PIN1, LED_COUNT, brightness=BRIGHTNESS)
pixels2 = neopixel.NeoPixel(LED_PIN2, LED_COUNT, brightness=BRIGHTNESS)
LED_INTVL = DV_H / (STRIP_LED_COUNT) # LED INTERVAL

# Color Settings
NO_COLOR = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

def __reset_led_color(pixels):
    pixels.fill((0, 0, 0))
    pixels.show()

def initialize():
    __reset_led_color(pixels1)
    __reset_led_color(pixels2)

def light_all():
    pixels1.fill((255, 255, 255))
    pixels2.fill((255, 255, 255))
    pixels1.show()
    pixels2.show()
    
def __determine_col(x):
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

def __determine_row(y):
    for i in range(STRIP_LED_COUNT):
        if ((i * LED_INTVL) <= y and y < ((i+1)*LED_INTVL)):
            return i
    # if can't find, then might hit the boundary of DV_H, return the last led index
    return STRIP_LED_COUNT - 1 

def __light_area_leds(c_min, c_max, r_min, r_max, color):
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

def __convert_to_device_scale(ymin, xmin, ymax, xmax):
    xmin = (xmin/1000) * DV_W
    xmax = (xmax/1000) * DV_W
    ymin = (ymin/1000) * DV_H
    ymax = (ymax/1000) * DV_H
    return ymin, xmin, ymax, xmax


def light_area(ymin, xmin, ymax, xmax, danger):
  ymin, xmin, ymax, xmax = __convert_to_device_scale(ymin, xmin, ymax, xmax)
  col_min = __determine_col(xmin)
  print("LED col min: ", col_min)
  col_max = __determine_col(xmax)
  print("LED col max: ", col_max)
  row_min = __determine_row(ymin)
  print("LED row min: ", row_min)
  row_max = __determine_row(ymax)
  print("LED row max: ", row_max)

  color = NO_COLOR
  if danger == 1:
    color = YELLOW
  if danger == 2:
    color = RED
  __light_area_leds(col_min, col_max, row_min, row_max, color)   

  pixels1.show()
  pixels2.show()

if __name__ == "__main__":
    initialize()
    light_all()
    time.sleep(2)
    initialize()
    
    pixels1[16] = (0, 0, 255)
    pixels1[28] = (255, 0, 0)
    pixels2[16] = (0, 0, 255)
    pixels2[28] = (255, 0, 0)
    pixels1.show()
    pixels2.show()

    time.sleep(5)
    initialize()
    

