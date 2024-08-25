import time
import board
import neopixel

def reset_led_color(pixels):
    pixels.fill((0, 0, 0))
    pixels.show()

LED_PIN1 = board.D18
LED_PIN2 = board.D21
LED_COUNT = 30
BRIGHTNESS = 0.1

pixels1 = neopixel.NeoPixel(LED_PIN1, LED_COUNT, brightness=BRIGHTNESS)
pixels2 = neopixel.NeoPixel(LED_PIN2, LED_COUNT, brightness=BRIGHTNESS)

reset_led_color(pixels1)
reset_led_color(pixels2)


pixels1.fill((0, 255, 0))
pixels2.fill((0, 0, 255))
pixels1.show()
pixels2.show()
time.sleep(4)

pixels1.fill((0, 0, 0))
pixels2.fill((0, 0, 0))

pixels1[15] = (255, 0, 0)
pixels2[15] = (255, 0, 0)
pixels1.show()
pixels2.show()

time.sleep(4)

pixels1.fill((0, 0, 0))
pixels2.fill((0, 0, 0))


