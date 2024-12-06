import sqlite3
from pathlib import Path
from flask import Blueprint, request, jsonify
from scripts.weekly_meal_plan import generate_meal_plan, update_meal_plan_with_cooldown

meal_plan_blueprint = Blueprint("meal_plan", __name__)

@meal_plan_blueprint.route("/", methods=["POST"])
def create_meal_plan():
    """
    Generate a weekly meal plan based on user preferences and tags.
    Request body should include: {"user_id": 1, "tags": {"vegetarian": true, "low carb": true}}
    """
    try:
        # Retrieve data from request body
        data = request.get_json()
        user_id = data["user_id"]
        selected_tags = data.get("tags", {})

        # Generate the meal plan
        meal_plan = generate_meal_plan(user_id, selected_tags)

        # Save meal plan with cooldown information
        update_meal_plan_with_cooldown(user_id, meal_plan)

        return jsonify({"message": "Meal plan generated successfully", "meal_plan": meal_plan}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@meal_plan_blueprint.route("/<int:user_id>/", methods=["GET"])
def get_user_meal_plan(user_id):
    """
    Retrieve the meal plan for the given user.
    """
    try:
        db_path = Path(__file__).resolve().parent.parent / "data" / "NutriDish.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM meal_plan WHERE user_id = ?
        """, (user_id,))
        meal_plan = cursor.fetchall()

        conn.close()

        if not meal_plan:
            return jsonify({"error": "No meal plan found for this user"}), 404

        # Format meal plan data
        formatted_meal_plan = {}
        for meal in meal_plan:
            meal_type = meal[2]
            if meal_type not in formatted_meal_plan:
                formatted_meal_plan[meal_type] = []
            formatted_meal_plan[meal_type].append({
                "title": meal[1],  # Recipe title
                "date_used": meal[3]
            })

        return jsonify({"user_id": user_id, "meal_plan": formatted_meal_plan}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
