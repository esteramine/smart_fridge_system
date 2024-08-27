from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

gemini_key=os.getenv("GEMINI_API_KEY")

genai.configure(api_key=gemini_key)

def upload_to_gemini(path, display_name, mime_type=None):
  # Uploads the given file to Gemini.
  file = genai.upload_file(path, display_name=display_name, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

def verify_upload(name):
  try:
    file = genai.get_file(name=name)
    print(f"Retrieved file '{file.display_name}' as: {file.uri}")
    return True
  except:
    print(f"File '{name}' upload unsuccessfully.")
    return False

def delete_upload(name):
  try:
    file = genai.get_file(name=name)
    file.delete()
    print(f"Deleted file '{file.display_name}' as: {file.uri}")
  except:
    print(f"File '{name}' does not exist in Gemini.")

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
)

# TODO Make these files available on the local file system
# You may need to update the file paths
# files = [
#   upload_to_gemini("article_291139_the-top-10-healthiest-foods-for-kids_-02-4b745e57928c4786a61b47d8ba920058.jpg", mime_type="image/jpeg"),
#   upload_to_gemini("1371602904324.jpeg", mime_type="image/jpeg"),
# ]

# file = upload_to_gemini("fridge_food.jpeg", "fridge_food", mime_type="image/jpeg")
# verify_upload(file.name)
# delete_upload("zbwjb7yetibs")
print(verify_upload("zbwjb7yetibs"))

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "Identify the food items and its quantity in the following uploaded photos and return the bounding boxes of each of the item and whether they are safe to eat based on the visual appearance in the following format: food_item: [xmin, xmax, ymin, ymax], quantity, safe/not safe to eat",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Please provide the photos you are referring to. I need to see the images to identify the food items, their quantities, and their safety status. \n\nOnce you provide the images, I will be able to analyze them and provide the information in the requested format. \n",
      ],
    },
    # {
    #   "role": "user",
    #   "parts": [
    #     files[0],
    #   ],
    # },
    # {
    #   "role": "model",
    #   "parts": [
    #     "- carrots: [1, 347, 0, 394], 6, safe to eat\n- carrots: [13, 218, 285, 297], 1, safe to eat\n- carrots: [5, 263, 245, 346], 1, safe to eat\n- carrots: [1, 302, 201, 395], 1, safe to eat\n- carrots: [0, 327, 155, 405], 1, safe to eat\n- beans: [299, 0, 571, 133], many, safe to eat\n- walnuts: [385, 192, 623, 345], many, safe to eat\n- raspberries: [310, 358, 564, 549], many, safe to eat\n- blueberries: [420, 441, 552, 538], many, safe to eat\n- avocado: [187, 506, 365, 635], 1, safe to eat\n- avocado: [334, 621, 512, 759], 1, safe to eat\n- sweet potato: [497, 532, 886, 766], many, safe to eat\n- strawberries: [813, 625, 976, 799], many, safe to eat\n- yogurt: [629, 685, 852, 826], 1, safe to eat\n- spinach: [0, 594, 360, 998], many, safe to eat\n- cherry tomatoes: [355, 822, 649, 998], many, safe to eat\n- quinoa: [673, 866, 925, 998], many, safe to eat\n- eggs: [572, 17, 713, 161], 1, safe to eat\n- eggs: [658, 45, 808, 139], 1, safe to eat\n- eggs: [748, 72, 898, 174], 1, safe to eat\n- eggs: [581, 117, 735, 214], 1, safe to eat\n- eggs: [674, 168, 829, 261], 1, safe to eat\n- brown rice: [639, 294, 938, 502], many, safe to eat\n- milk: [34, 0, 206, 102], 1, safe to eat\n",
    #   ],
    # },
    # {
    #   "role": "user",
    #   "parts": [
    #     files[1],
    #   ],
    # },
    # {
    #   "role": "model",
    #   "parts": [
    #     "- ketchup: [177, 92, 397, 214], 1, safe to eat\n- juice: [123, 441, 319, 538], 1, safe to eat\n- milk: [79, 726, 371, 801], 1, safe to eat\n- oil: [90, 787, 376, 916], 1, safe to eat\n- eggs: [319, 269, 396, 540], 6, safe to eat\n- pickles: [203, 565, 317, 700], 1, safe to eat\n- meat: [505, 137, 585, 402], 1, safe to eat\n- patty: [522, 481, 585, 639], 1, safe to eat\n- sausage: [498, 677, 592, 899], 1, safe to eat\n- red pepper: [617, 142, 701, 311], 1, safe to eat\n- green pepper: [614, 308, 704, 515], 1, safe to eat\n- yellow pepper: [610, 512, 703, 721], 1, safe to eat\n- lettuce: [754, 93, 958, 549], 1, safe to eat \n",
    #   ],
    # },
  ]
)

# response = chat_session.send_message(file)

# print(response.text)