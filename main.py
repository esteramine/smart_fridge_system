import genai
import database as db

def create_food_item(label, left, top, right, bottom, expiration_date):
    return {
        "label": label,
        "left": left,
        "top": top,
        "right": right,
        "bottom": bottom,
        "expiration_date": expiration_date,
        # "created_at": firestore.SERVER_TIMESTAMP,
    }

food = create_food_item("egg", 1, 3, 5, 7, "20240827")
print(db.add_food_item(food))

# genai
# file = genai.upload_to_gemini("food.jpg", "fridge_food", mime_type="image/jpeg")
# if (genai.verify_upload(file.name)):
#   response = genai.send_message(file)
#   print(response.text)
#   genai.delete_upload(file.name)