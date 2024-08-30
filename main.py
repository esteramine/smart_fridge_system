from uuid import uuid4
import os

import genai
import database as db
import led
from camera import initialize_camera, close_camera

led.initialize()

# TODO: integrate to hall_sensor package
import RPi.GPIO as GPIO

# gas sensor library
from gpiozero import DigitalInputDevice
import time

# Hall Sensor
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)

# Gas Sensor
mq3 = DigitalInputDevice(17)
mq2 = DigitalInputDevice(27)

near_magnetic = True


while True:
	## GPIO.input(4) == 1 means near magnetic field, 0 means far from magnetic field
	## far from magnetic field (fridge opened), near_magnetic == True means the fridge door before is closed
    if (not GPIO.input(4) and near_magnetic == True):
        # print("Fridge open!")
        print("Fridge open!")
        near_magnetic = False
        # when fridge door is open
        # read from firestore, and light the leds
        food_list = db.get_food_list()
        unsafe_food_list = filter(lambda item: item.safety != 0, food_list)
        for food in unsafe_food_list:
            # light leds
            led.light_area(xmin=food.xmin, xmax=food.xmax, ymin=food.ymin, ymax=food.ymax, danger=food.safety)
            print(food)
	## near magnetic field (fridge closed)
    if (GPIO.input(4) and near_magnetic == False):
        print("Fridge closed!")

		# when fridge door is just closed, light leds to give light for capturing image
        
        # 1. capture image
        img_name = str(uuid4())
        img_path = f"{img_name}.jpg"
        cam = initialize_camera()
        cam.capture_file(img_path)

        # 2. ask gemini
        file = genai.upload_to_gemini(img_path, img_name, mime_type="image/jpeg")
        # file = genai.upload_to_gemini("food.jpeg", "fridge_food", mime_type="image/jpeg")
        response = ""
        if (genai.verify_upload(file.name)):
            print("")
            response = (genai.send_message(file)).text
            print(response)
            # genai.delete_upload(file.name)
        os.remove(img_path) # remove local image file
        file = ""

        # 3. upload to firebase
        if (response.strip() != ""):
            db.push_food_list(response)
        
        # 4. reset the state
        near_magnetic = True

        ## gas sensor
    i = 0
    # print(mq2.is_active)
    if(mq2.is_active==0):
        # print("time stamp ", "f'{i}s" , " Methane Gas detected")
        print(f"time stamp {i}s: Methane Gas detected")
    else:
        print(f"time stamp {i}s: No Methane Gas detected")
    
    if(mq3.is_active==0):
        # print("time stamp ", "f'{i}s" , " Alcohol Gas detected")
        print(f"time stamp {i}s: Alcohol Gas detected")
    else:
        # print("time stamp ", "f'{i}s" , " No Alcohol Gas detected")
        print(f"time stamp {i}s: No Alcohol Gas detected")
    i= i+1
    time.sleep(1)