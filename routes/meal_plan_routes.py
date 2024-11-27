from flask import Blueprint, request, jsonify
from scripts.weekly_meal_plan import generate_meal_plan

meal_plan_blueprint = Blueprint("meal_plan", __name__)

@meal_plan_blueprint.route("/", methods=["POST"])
def create_meal_plan():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        selected_tags = data.get("tags", {})

        if not user_id:
            return jsonify({"error": "User ID is required"}), 400

        meal_plan = generate_meal_plan(user_id, selected_tags)
        return jsonify(meal_plan), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
