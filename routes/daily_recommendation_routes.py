from flask import Blueprint, jsonify, request
from datetime import datetime
import random
from scripts.data_storage import get_db_connection
from firebase_admin import firestore
import random

db = firestore.client()
daily_recommendations_blueprint = Blueprint("daily_recommendations", __name__)

def get_recommendations(meal_type, user_restrictions, num_recommendations=10):
    """
    Fetch recommendations for the given meal type and user restrictions from Firestore.
    :param meal_type: The type of meal (e.g., breakfast, lunch, etc.).
    :param user_restrictions: User's restrictions like cons_pork and cons_alcohol.
    :param num_recommendations: Number of recipes to recommend.
    :return: A list of recommended recipes.
    """
    try:
        # Start Firestore query for recipes matching the meal type
        recipes_ref = db.collection("recipes").where(f"is_{meal_type}", "==", True)

        # Apply user restrictions
        if user_restrictions.get("cons_pork") == 0:  # User doesn't allow pork
            recipes_ref = recipes_ref.where("has_pork", "==", False)
        if user_restrictions.get("cons_alcohol") == 0:  # User doesn't allow alcohol
            recipes_ref = recipes_ref.where("has_alcohol", "==", False)

        # Execute query and fetch results
        recipes = [doc.to_dict() for doc in recipes_ref.stream()]

        if not recipes:
            return []

        # Randomly select the required number of recipes
        return random.sample(recipes, min(len(recipes), num_recommendations))
    except Exception as e:
        raise RuntimeError(f"Error fetching recommendations: {e}")

@daily_recommendations_blueprint.route("/", methods=["POST"])
def recommend():
    """
    Recommend recipes based on the current time and user restrictions.
    """
    try:
        user_data = request.get_json()
        if not user_data or "userId" not in user_data:
            return jsonify({"error": "Missing userId in the request body"}), 400

        user_id = user_data["userId"]

        # Fetch user restrictions from Firestore
        user_ref = db.collection("users").document(user_id)
        user_doc = user_ref.get()

        if not user_doc.exists:
            return jsonify({"error": "User not found"}), 404

        user_restrictions = user_doc.to_dict()

        # Determine the current time and meal type
        current_hour = datetime.now().hour
        if 5 <= current_hour < 12:
            meal_type = "breakfast"
        elif 12 <= current_hour < 17:
            meal_type = "lunch"
        elif 17 <= current_hour < 21:
            meal_type = "dinner"
        else:
            meal_type = random.choice(["snack", "dessert"])  # Nighttime can be snack or dessert

        # Get recommendations
        recommendations = get_recommendations(meal_type, user_restrictions)

        if not recommendations:
            return jsonify({"message": f"No {meal_type} recipes found"}), 404

        return jsonify({
            "meal_type": meal_type,
            "recommendations": recommendations
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
