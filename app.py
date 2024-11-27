import json
from flask import Flask, jsonify, request
from pathlib import Path
from scripts.data_storage import load_from_sql
from scripts.recipe_search import search_recipes

app = Flask(__name__)

# Home endpoint to test API availability
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to NutriDish API"})

# Recipe search endpoint
@app.route("/recipes/", methods=["POST"])
def recipes():
    try:
        # Get JSON data from the request
        user_input = request.get_json() or {}

        # Load recipes from SQLite database
        db_path = Path(__file__).resolve().parent / "data" / "recipes.db"
        data = load_from_sql(db_path=db_path, table_name="recipes")

        # Perform the recipe search
        filtered_recipes = search_recipes(data, user_input)

        # Return filtered recipes as JSON
        return jsonify(filtered_recipes.to_dict(orient="records"))
    except Exception as e:
        # Handle errors
        return jsonify({"error": str(e)}), 400

# Recipe details endpoint
@app.route("/recipe/<title>/", methods=["GET"])
def recipe_details(title):
    try:
        # Load the JSON file containing recipe details
        json_path = Path(__file__).resolve().parent / "data" / "Recipe_Details.json"
        with open(json_path, "r") as f:
            recipe_details = json.load(f)

        # Search for the recipe by title (case-insensitive)
        recipe = next(
            (r for r in recipe_details if r["title"].strip().lower() == title.strip().lower()), None
        )

        # If not found, return a 404 error
        if not recipe:
            return jsonify({"error": f"Recipe with title '{title}' not found"}), 404

        # Return the detailed recipe as JSON
        return jsonify(recipe)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
