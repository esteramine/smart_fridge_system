
from uuid import uuid4
import os

import genai
import database as db
import led
from camera import initialize_camera, close_camera

led.initialize()

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
    response = (genai.send_message(file)).text
    print(response)
    genai.delete_upload(file.name)
# os.remove(img_path) # remove local image file

# 3. upload to firebase
if (response.strip() != ""):
    db.push_food_list(response)
        