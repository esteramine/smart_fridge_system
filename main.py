from uuid import uuid4
import os

import genai
import database as db
import led
from camera import initialize_camera, close_camera

led.initialize()

# when fridge door is open
# read from firestore, and light the leds
food_list = db.get_food_list()
unsafe_food_list = filter(lambda item: item.safety == 1, food_list)
for food in unsafe_food_list:
  # light leds
  led.light_area(xmin=food.xmin, xmax=food.xmax, ymin=food.ymin, ymax=food.ymax)
  print(food)

# when fridge door is just closed
# light leds to give light for capturing image
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