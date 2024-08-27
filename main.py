import genai

def create_food_item(label, left, top, right, bottom, score, expiration_date):
    return {
        "label": label,
        "left": left,
        "top": top,
        "right": right,
        "bottom": bottom,
        "score": score,
        "expiration_date": expiration_date,
        "created_at": firestore.SERVER_TIMESTAMP,
    }


file = genai.upload_to_gemini("food.jpg", "fridge_food", mime_type="image/jpeg")
if (genai.verify_upload(file.name)):
  response = genai.send_message(file)
  print(response)
  genai.delete_upload(file.name)