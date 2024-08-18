import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

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

# Use a service account.
cred = credentials.Certificate('serviceAccountKey.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

doc_ref = db.collection("inventory")
# example
food_item = create_food_item(label="apple", left=63, top=199, right=205, bottom=376, score=0.67, expiration_date=None)
# auto-generate ID (don't specify document name)
update_time, food_ref = doc_ref.add(food_item)

print(f"Document ID: {food_ref.id}") # access the auto-generated ID 

