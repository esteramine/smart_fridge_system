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
  upload_to_gemini("food.jpeg", "food", mime_type="image/jpeg"),
]

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "In the following photo, identify 1. the food items 2. their quantity 3. whether they are safe to eat based on the visual appearance (safe return 0, not safe return 1) 4. the bounding boxes of each of item. Return the information with pure text (without markdown or list): food_item, quantity, 0/1 (safe to eat or not), [ymin xmin ymax xmax] (bounding box)",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Please provide me with the photo so I can analyze it and provide the requested information. \n",
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
        "sauce, 1, 0, [183 94 403 217]\neggs, 6, 0, [312 268 403 548]\njuice, 1, 0, [123 434 319 546]\npickles, 1, 0, [207 548 313 694]\nbutter, 1, 0, [318 562 397 763]\nmilk, 1, 0, [64 699 312 798]\noil, 1, 0, [98 777 395 908]\nmeat, 1, 0, [505 131 581 421]\nmeat patty, 1, 0, [522 469 582 641]\nsausages, 2, 0, [488 670 586 894]\npepper, 1, 0, [605 160 702 310]\npepper, 1, 0, [608 304 706 515]\npepper, 1, 0, [601 523 720 712]\nlettuce, 1, 0, [756 93 950 553]\n",
      ],
    },
  ]
)
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
