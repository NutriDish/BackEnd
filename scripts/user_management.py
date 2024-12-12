from scripts.data_storage import get_db_connection
import json
from datetime import datetime
from firebase_admin import firestore

db = firestore.client()


def create_user(user_data):
    """
    Create or update a user in the Firestore 'users' collection.
    """
    try:
        user_id = user_data.get("userId")
        user_ref = db.collection("users").document(user_id)

        # Add or update the user document
        user_data["dateReg"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_ref.set(user_data)

        return {"message": "User information updated successfully"}, 200
    except Exception as e:
        return {"error": str(e)}, 500
    
def calculate_age(dob):
    """
    Calculate age from date of birth.
    """
    if not dob:
        return None
    try:
        today = datetime.today()
        birth_date = datetime.strptime(dob, "%Y-%m-%d")
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    except ValueError:
        return None  # Handle invalid date format


def get_user(user_id):
    """
    Retrieve user details by userId from Firestore.
    """
    try:
        user_ref = db.collection("users").document(user_id)
        user_doc = user_ref.get()

        if not user_doc.exists:
            return {"error": f"User with ID {user_id} not found"}, 404

        return user_doc.to_dict(), 200
    except Exception as e:
        return {"error": str(e)}, 500



