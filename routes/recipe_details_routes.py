from flask import Blueprint, jsonify
import json
from pathlib import Path

# Define the Blueprint
recipe_details_blueprint = Blueprint("recipe_details_route", __name__)

def get_recipe_details(title):
    """
    Retrieve the details of a specific recipe by title.
    """
    try:
        json_path = Path(__file__).resolve().parent.parent / "data" / "Recipe_Details.json"
        with open(json_path, "r") as f:
            recipes = json.load(f)

        # Find the recipe with the given title (case-insensitive match)
        recipe = next((r for r in recipes if r["title"].lower() == title.lower()), None)

        if not recipe:
            return {"error": f"Recipe with title '{title}' not found"}, 404

        return recipe
    except Exception as e:
        return {"error": str(e)}, 500

@recipe_details_blueprint.route("/<string:title>/", methods=["GET"])
def details(title):
    """
    Fetch the full details of a recipe by title.
    """
    recipe = get_recipe_details(title)
    if "error" in recipe:
        return jsonify(recipe), 404
    return jsonify(recipe)
