from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

gemini_key=os.getenv("GEMINI_API_KEY")

genai.configure(api_key=gemini_key)

# Create Gemini model
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

def upload_to_gemini(path, display_name, mime_type=None):
  """
  Uploads the given file to Gemini.

  :param path: Path of the file you want to upload.
  :param display_name: An easy to read name of the file to stored in Gemini.
  :param mime_type: Type of the file (ex. jpg/jpeg/png).
  :return: Information of the file uploaded.
  """
  file = genai.upload_file(path, display_name=display_name, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

files = [
  upload_to_gemini("test_food_1.jpeg", "test_food_1", mime_type="image/jpeg"),
  upload_to_gemini("test_food_2.jpeg", "test_food_2", mime_type="image/jpeg"),
]

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "In the following photo, identify \n1. the \"food\" items (exclude those which cannot be consumed by humans) \n2. their quantity \n3. whether they are safe to eat based on the visual appearance (safe return 0, not sure return 1, not safe to eat return 2) 4. which category the food belongs to (pick one of the following categories: \"leafy_greens\", \"broccoli_and_cauliflower\", \"root_vegetables\", \"berries\", \"citrus_fruits\", \"milk\", \"soft_cheese\", \"hard_cheese\", \"yogurt\",\n\"raw_chicken\", \"raw_beef_pork_lamb\", \"cooked_meat_and_poultry\", \"deli_meats\",\n\"fresh_fish\", \"shellfish\", \"smoked_fish\", \"whole_eggs\", \"hard_boiled_eggs\",\n\"bread\", \"baked_goods\", \"cooked_rice_and_pasta\", \"soups_and_stews\",\n\"canned_goods_unopened\", \"nuts\", \"bell_peppers\", \"zucchini_and_summer_squash\", \"cucumbers\", \"green_beans\",\n\"asparagus\", \"mushrooms\", \"cabbage\", \"celery\", \"tomatoes\", \"apples\",\n\"bananas\", \"grapes\", \"whole_pineapple\", \"cut_pineapple\", \"whole_melons\", \"cut_melons\", \"peaches_plums_and_nectarines\",\n\"pears\", \"kiwifruit\", \"avocados\", \"others\")\n4. the bounding boxes of each of item. Return the information with pure text (without markdown or list): food_item, quantity, 0/1/2 (safe to eat or not), category of the food, [ymin xmin ymax xmax] (bounding box)\nAn example: spinach, 1, 2, leafy_greens, [10 12 564 756]",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Please provide me with the photo so I can analyze it and provide you with the requested information. I need the image to identify the food items, their quantity, safety, category, and bounding boxes. \n",
      ],
    },
    {
      "role": "user",
      "parts": [
        files[0],
      ],
    },
    {
      "role": "model",
      "parts": [
        "eggs, 6, 0, whole_eggs, [314 271 394 530]\npickles, 1, 0, others, [212 553 324 704]\nlettuce, 1, 0, leafy_greens, [755 111 925 569]\nred bell pepper, 1, 0, bell_peppers, [616 164 708 307]\ngreen bell pepper, 1, 0, bell_peppers, [614 317 701 507]\nyellow bell pepper, 1, 0, bell_peppers, [607 520 710 718]\nraw beef_pork_lamb, 1, 0, raw_beef_pork_lamb, [511 151 585 411]\nsausages, 1, 0, deli_meats, [501 666 588 893]\nmeat patties, 1, 0, cooked_meat_and_poultry, [512 477 587 638]\nmilk, 1, 0, milk, [84 714 327 796]\nvegetable oil, 1, 0, others, [85 788 388 904]\nketchup, 1, 0, others, [220 97 404 220]\njuice, 1, 0, others, [118 434 314 541]\npasta, 1, 0, cooked_rice_and_pasta, [329 572 397 756]",
      ],
    },
    {
      "role": "user",
      "parts": [
        files[1],
      ],
    },
    {
      "role": "model",
      "parts": [
        "pineapple, 15, 0, cut_pineapple, [319 6 813 986]\nchillies, 3, 0, others, [212 2 312 138]\npineapple, 1, 0, whole_pineapple, [0 704 359 999]\npineapple, 1, 0, cut_pineapple, [762 675 848 816] \npaprika, 1, 0, others, [764 675 845 816] \n",
      ],
    },
  ]
)

# chat_session = model.start_chat(
#   history=[
#     {
#       "role": "user",
#       "parts": [
#         "In the following photo, identify 1. the food items 2. their quantity 3. whether they are safe to eat based on the visual appearance (safe return 0, not safe return 1) 4. the bounding boxes of each of item. Return the information with pure text (without markdown or list): food_item, quantity, 0/1 (safe to eat or not), [ymin xmin ymax xmax] (bounding box)",
#       ],
#     },
#     {
#       "role": "model",
#       "parts": [
#         "Please provide me with the photo so I can analyze it and provide the requested information. \n",
#       ],
#     },
#     {
#       "role": "user",
#       "parts": [
#         files[0],
#       ],
#     },
#     {
#       "role": "model",
#       "parts": [
#         "sauce, 1, 0, [183 94 403 217]\neggs, 6, 0, [312 268 403 548]\njuice, 1, 0, [123 434 319 546]\npickles, 1, 0, [207 548 313 694]\nbutter, 1, 0, [318 562 397 763]\nmilk, 1, 0, [64 699 312 798]\noil, 1, 0, [98 777 395 908]\nmeat, 1, 0, [505 131 581 421]\nmeat patty, 1, 0, [522 469 582 641]\nsausages, 2, 0, [488 670 586 894]\npepper, 1, 0, [605 160 702 310]\npepper, 1, 0, [608 304 706 515]\npepper, 1, 0, [601 523 720 712]\nlettuce, 1, 0, [756 93 950 553]\n",
#       ],
#     },
#   ]
# )

# chat_session = model.start_chat(
#   history=[
#     {
#       "role": "user",
#       "parts": [
#         "Identify the food items and its quantity in the following uploaded photos and return the bounding boxes of each of the item and whether they are safe to eat based on the visual appearance in the following format: food_item: [xmin, xmax, ymin, ymax], quantity, safe/not safe to eat",
#       ],
#     },
#     {
#       "role": "model",
#       "parts": [
#         "Please provide the photos you are referring to. I need to see the images to identify the food items, their quantities, and their safety status. \n\nOnce you provide the images, I will be able to analyze them and provide the information in the requested format. \n",
#       ],
#     },
#   ]
# )

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

def send_message(message):
  """
  Send message to Gemini model.

  :param message(string/Part): Message sent to Gemini model.
  :return: Response of the message.
  """
  response = chat_session.send_message(message)
  return response
