import cv2
from io import BytesIO
from datetime import datetime, timedelta
from uuid import uuid4
import os

import genai
import google_cloud as gcs
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

def upload_cropped_image_to_gcs(img_path, food_list):
    img = cv2.imread(img_path)
    img_h, img_w, img_c = img.shape
    for food in food_list:
        ymin=int((food.ymin * img_h)/1000)
        xmin=int((food.xmin * img_w)/1000)
        ymax=int((food.ymax * img_h)/1000)
        xmax=int((food.xmax * img_w)/1000)
        crop_img=img[ymin:ymax, xmin:xmax]
        is_success, buffer = cv2.imencode(".jpg", crop_img)
        image_bytes = BytesIO(buffer)
        food.image_url = gcs.upload_blob_from_stream(image_bytes, f"{food.name}-{food.doc_id}.jpg")
    return food_list


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

print("Fridge closed!")

# TODO: when fridge door is just closed, light leds to give light for capturing image
led.light_all()
# 1. capture image
img_name = str(uuid4())
img_path = f"{img_name}.jpg"

cam.capture_file(img_path)
led.initialize()
# 2. ask gemini
file = genai.upload_to_gemini(img_path, img_name, mime_type="image/jpeg")
# file = genai.upload_to_gemini("food.jpeg", "fridge_food", mime_type="image/jpeg")
response = ""
if (genai.verify_upload(file.name)):
    print("")
    response = (genai.send_message(file)).text
    print(response)
    # genai.delete_upload(file.name)

food_list = create_food_list(response)

# 3. upload food cropped image to google cloud
food_list_with_img_url = upload_cropped_image_to_gcs(img_path, food_list)

# 4. get recent db data (know which food already in fridge)
# TODO: detect which food is the same and which are not and update the corresponding data

# 5. upload to firebase
if (response.strip() != ""):
    db.push_food_list(food_list_with_img_url)

# 6. remove local image file
os.remove(img_path) 
