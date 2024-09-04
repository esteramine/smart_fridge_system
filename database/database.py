from dotenv import load_dotenv
import os
import firebase_admin
from firebase_admin import firestore, credentials
from datetime import datetime, timedelta

from .data_processing import create_food_list, FoodItem

load_dotenv()

key_path=os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY_PATH")

# Use a service account.
cred = credentials.Certificate(key_path)

app = firebase_admin.initialize_app(cred)

db = firestore.client()

inventory = db.collection("inventory")

def push_food_list(food_list):
  # food_list = create_food_list(text)
  for food_item in food_list:
        food_dict = food_item.to_dict()
        food_dict['created_at'] = firestore.SERVER_TIMESTAMP
        # Add to Firestore collection
        update_time, food_ref = inventory.add(food_dict)
        # access the auto-generated ID
        print(f"Document ID: {food_ref.id}") 

def update_in_fridge_status(document_ids):
    # Create a batch object
    batch = db.batch()
    
    # Loop over each document ID
    for doc_id in document_ids:
        # Get a reference to the document
        doc_ref = inventory.document(doc_id)
        
        # Update the "in_fridge" field to False in the batch
        batch.update(doc_ref, {"in_fridge": False})
    
    # Commit the batch
    batch.commit()

def update_food_item(food_item):
    doc_ref = inventory.document(food_item.doc_id)
    doc_ref.update(food_item.to_dict())

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
      data = doc.to_dict()
      food_item = FoodItem.from_dict(data, doc_id=doc.id)
      food_list.append(food_item)
      print(f"{doc.id} => {doc.to_dict()}")
  return food_list


def get_food_items(conditions=None):
    """
    Query Firestore for food items with optional conditions.
    
    :param conditions: A list of tuples representing conditions. 
                       Each tuple should be in the form (field_name, operator, value).
                       Example: [("created_at", ">=", datetime.now() - timedelta(days=2))]
    :return: A list of FoodItem objects matching the query.
    """
    print('Database get food list. Query conditions: ', conditions)
    # Apply conditions if provided
    query = inventory
    if conditions:
        for condition in conditions:
            field_name, operator, value = condition
            query = query.where(field_name, operator, value)

    # Execute the query
    docs = query.stream()
    food_items = []

    for doc in docs:
        data = doc.to_dict()
        food_item = FoodItem.from_dict(data, doc_id=doc.id)
        food_items.append(food_item)

    return food_items


def query_recent_food():
    # Query for documents where in_fridge is True
    query_in_fridge = inventory.where("in_fridge", "==", True)
    
    # Query for documents where created_at is within the last two days
    two_days_ago = datetime.now() - timedelta(days=2)
    query_recent = inventory.where("last_out_fridge_time", "<=", two_days_ago)
    
    # Execute both queries
    docs_in_fridge = query_in_fridge.stream()
    docs_recent = query_recent.stream()

    food_items = {}
    
    # Collect results from the first query
    for doc in docs_in_fridge:
        data = doc.to_dict()
        food_item = FoodItem.from_dict(data, doc_id=doc.id)
        food_items[doc.id] = food_item

    # Collect results from the second query
    for doc in docs_recent:
        if doc.id not in food_items:  # Avoid duplicates
            data = doc.to_dict()
            food_item = FoodItem.from_dict(data, doc_id=doc.id)
            food_items[doc.id] = food_item

    # Return the list of FoodItem objects
    return list(food_items.values())

