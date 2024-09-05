from datetime import datetime, timedelta
from uuid import uuid4
import os

import genai
import database as db
from database import create_food_list
import led
from camera import initialize_camera, close_camera

led.initialize()
cam = initialize_camera()

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

food_list = []

# THRESHOLD
KEYPOINT_DISTANCE_THRESHOLD = 0.75
KEYPOINT_MATCHED_THRESHOLD = 0.7
TEXTURE_THRESHOLD = 0.5

def copy_bounding_box(source, need_copy):
    need_copy.xmin = source.xmin
    need_copy.ymin = source.ymin
    need_copy.xmax = source.xmax
    need_copy.ymax = source.ymax
    return need_copy

def is_keypoints_matched(new, old):
    print("keypoint matched")
    # if len(good_matches) > len(descriptors_old) * 0.7:  # For example, 70% of old keypoints should match
    #     print("Items are considered the same despite deformation.")

def is_texture_matched(new, old):
    print("texture matched")

def is_similar_location(new, old):
    if (abs(old.xmin - new.xmin) < 50 and abs(old.ymin - new.ymin) < 50 and abs(old.xmax - new.xmax) < 50 and abs(old.ymax - new.ymax) < 50):
        return True
    return False

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

		# TODO: when fridge door is just closed, light leds to give light for capturing image
        
        # 1. capture image
        img_name = str(uuid4())
        img_path = f"{img_name}.jpg"
        
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

        food_list = create_food_list(response)

        # 3. get recent db data (know which food already in fridge)
        # TODO: detect which food is the same and which are not and update the corresponding data
        # query in_fridge == True or last_out_fridge_time <= 2 days
        last_in_fridge_food = db.get_food_items([("in_fridge", "==", True)])
        recent_out_fridge_food = db.get_food_items([("in_fridge", "==", False), ("last_out_fridge_time", "<=", datetime.now() - timedelta(days=2))])
        updated_in_fridge_food = []
        # check whether the data is similar, and update the information, or else, add new food item
        for i in range(len(food_list)):
            similar_in_fridge = filter(lambda item: item.name.lower() == food_list[i].name.lower(), last_in_fridge_food)
            for similar in similar_in_fridge:
                if (is_keypoints_matched(food_list[i], similar) and is_texture_matched(food_list[i], similar)):
                    db.update_food_item(copy_bounding_box(food_list[i], similar))
                    break
            



            # (1) check whether there is similar last_in_fridge_food
            # (1.1) if there is, update the coordinates and added to updated_in_fridge_food, remove from food_list and last_in_fridge_food
            # (1.2) if no, food_list remains unchanged

        # last_in_fridge_food remained items should be updated to in_fridge = False and last_out_fridge_time = firestore.SERVER_TIMESTAMP

        # recent_out_fridge_food some food should be updated to in_fridge = True

        # update updated_in_fridge_food info

        # add food_list remained item as new food items



        # 4. upload to firebase
        if (response.strip() != ""):
            db.push_food_list(food_list)

        
        
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