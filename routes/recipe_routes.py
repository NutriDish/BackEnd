from flask import Blueprint, request, jsonify
from scripts.recipe_search import search_recipes
from scripts.data_storage import load_from_sql
from pathlib import Path

recipe_blueprint = Blueprint("recipes", __name__)

@recipe_blueprint.route("/", methods=["POST"])
def search():
    try:
        # Get user input JSON from the request body
        user_input = request.get_json() or {}

        # Load the recipes database
        db_path = Path(__file__).resolve().parent.parent / "data" / "recipes.db"
        data = load_from_sql(db_path=db_path, table_name="recipes")

        # Filter recipes based on user input
        filtered_recipes = search_recipes(data, user_input)

        # Return the filtered recipes as JSON
        return jsonify(filtered_recipes.to_dict(orient="records"))
    except Exception as e:
        # Handle any errors and return an error message
        return jsonify({"error": str(e)}), 400