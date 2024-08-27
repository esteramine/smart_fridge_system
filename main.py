from uuid import uuid4
import os

import genai
import database as db
from camera import initialize_camera, close_camera

# read from firestore, and light the leds

# capture image
img_name = uuid4()
img_path = f"{img_name}.jpg"
cam = initialize_camera()
cam.capture_file(img_path)

# ask gemini
# file = genai.upload_to_gemini(img_path, img_name, mime_type="image/jpeg")
file = genai.upload_to_gemini("food.jpeg", "fridge_food", mime_type="image/jpeg")
response = ""
if (genai.verify_upload(file.name)):
    response = (genai.send_message(file)).text
    print(response)
    genai.delete_upload(file.name)
os.remove(img_path) # remove local image file

# upload to firebase
if (response.strip() != ""):
    db.push_food_list(response)


# database
# food = create_food_item("egg", 1, 3, 5, 7, "20240827")
# print(db.add_food_item(food))

# genai
# file = genai.upload_to_gemini("food.jpg", "fridge_food", mime_type="image/jpeg")
# if (genai.verify_upload(file.name)):
#   response = genai.send_message(file)
#   print(response.text)
#   genai.delete_upload(file.name)