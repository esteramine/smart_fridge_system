import genai

file = genai.upload_to_gemini("fridge_food.jpeg", "fridge_food", mime_type="image/jpeg")
if (genai.verify_upload(file.name)):
  response = genai.send_message(file)
  print(response)
  genai.delete_upload(file.name)