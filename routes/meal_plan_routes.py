from flask import Blueprint, request, jsonify
from scripts.weekly_meal_plan import generate_weekly_menu
from scripts.data_storage import load_from_sql, save_to_json
from pathlib import Path

meal_plan_blueprint = Blueprint("meal_plan", __name__)

@meal_plan_blueprint.route("/", methods=["POST"])
def create_meal_plan():
    user_input = request.json
    cooldown_tracker = request.json.get("cooldown_tracker", {})
    
    db_path = Path(__file__).resolve().parent.parent / "data" / "recipes.db"
    json_path = Path(__file__).resolve().parent.parent / "test_and_output" / "weekly_menu.json"
    
    data = load_from_sql(db_path=db_path, table_name="recipes")
    weekly_menu, cooldown_tracker = generate_weekly_menu(data, user_input, cooldown_tracker)
    
    save_to_json(weekly_menu, json_path=json_path)
    return jsonify({"weekly_menu": weekly_menu, "cooldown_tracker": cooldown_tracker})
