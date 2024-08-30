from uuid import uuid4
import os

import genai
import database as db
import led
from camera import initialize_camera, close_camera

led.initialize()

food_list = db.get_food_list()
unsafe_food_list = filter(lambda item: item.safety != 0, food_list)
for food in unsafe_food_list:
    # light leds
    led.light_area(xmin=food.xmin, xmax=food.xmax, ymin=food.ymin, ymax=food.ymax, danger=food.safety)
    print(food)