import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
cred = credentials.Certificate('serviceAccountKey.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

inventory = db.collection("inventory")

def add_food_item(food):
  update_time, food_ref = inventory.add(food)
   # access the auto-generated ID
  print(f"Document ID: {food_ref.id}") 
  return food_ref.id

def set_food_item(id, new_data):
  # TODO
  return None

def delete_food_item(id):
  # TODO
  return True

def list_food_items():
  # TODO
  return []



