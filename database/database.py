from dotenv import load_dotenv
import os
import firebase_admin
from firebase_admin import firestore, credentials

from .data_processing import create_food_list, FoodItem

load_dotenv()

key_path=os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY_PATH")

# Use a service account.
cred = credentials.Certificate(key_path)

app = firebase_admin.initialize_app(cred)

db = firestore.client()

inventory = db.collection("inventory")

def push_food_list(text):
  food_list = create_food_list(text)
  for food_item in food_list:
        food_dict = food_item.to_dict()
        food_dict['created_at'] = firestore.SERVER_TIMESTAMP
        # Add to Firestore collection
        update_time, food_ref = inventory.add(food_dict)
        # access the auto-generated ID
        print(f"Document ID: {food_ref.id}") 


def set_food_item(id, new_data):
  # TODO
  return None

def delete_food_item(id):
  # TODO
  return True

def get_food_list():
  print('Database get food list.')
  docs = inventory.stream()
  food_list = []
  for doc in docs:
      food_list.append(FoodItem.from_dict(doc.to_dict()))
      print(f"{doc.id} => {doc.to_dict()}")
  return food_list



