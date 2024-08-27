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
  ]
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
