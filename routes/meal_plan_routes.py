import sqlite3
from pathlib import Path
from flask import Blueprint, request, jsonify
from scripts.data_storage import get_db_connection
from scripts.weekly_meal_plan import generate_meal_plan #update_meal_plan_with_cooldown
from firebase_admin import firestore

db = firestore.client()
meal_plan_blueprint = Blueprint("meal_plan", __name__)

@meal_plan_blueprint.route("/", methods=["POST"])
def create_meal_plan():
    """
    Generate a weekly meal plan based on user preferences and tags.
    Request body should include: {"userId": "12345", "tags": {"vegetarian": true, "low_carb": true}}
    """
    try:
        # Retrieve data from request body
        data = request.get_json()

        # Validate input
        user_id = data.get("userId")
        if not user_id:
            return jsonify({"error": "Missing 'userId' in request body"}), 400

        selected_tags = data.get("tags", {})

        # Generate the meal plan
        meal_plan = generate_meal_plan(user_id, selected_tags)

        # Save the meal plan to Firestore
        for day, daily_meals in meal_plan.items():
            for meal_type, meal_data in daily_meals.items():
                db.collection("mealPlan").add({
                    "userId": user_id,
                    "recipeTitle": meal_data["title"],
                    "mealType": meal_type,
                    "dateUsed": day  # Optionally include a formatted date
                })

        return jsonify({"message": "Meal plan generated successfully", "meal_plan": meal_plan}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@meal_plan_blueprint.route("/<string:user_id>/", methods=["GET"])
def get_user_meal_plan(user_id):
    """
    Retrieve the meal plan for the given user from Firestore.
    """
    try:
        # Query Firestore for the user's meal plan
        meal_plan_ref = db.collection("mealPlan").where("userId", "==", user_id)
        meal_plan_docs = meal_plan_ref.stream()

        # Convert documents to a structured format
        meal_plan = [doc.to_dict() for doc in meal_plan_docs]

        if not meal_plan:
            return jsonify({"error": "No meal plan found for this user"}), 404

        # Format meal plan data
        formatted_meal_plan = {}
        for meal in meal_plan:
            meal_type = meal.get("mealType")
            if meal_type not in formatted_meal_plan:
                formatted_meal_plan[meal_type] = []
            formatted_meal_plan[meal_type].append({
                "title": meal.get("recipeTitle"),
                "date_used": meal.get("dateUsed")
            })

        return jsonify({"user_id": user_id, "meal_plan": formatted_meal_plan}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500