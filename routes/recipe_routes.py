from flask import Blueprint, request, jsonify
from scripts.recipe_search import search_recipes
from routes.recipe_details_routes import get_recipe_details  # Import the new function

recipe_blueprint = Blueprint("recipe", __name__)

@recipe_blueprint.route("/", methods=["POST"])
def search():
    """
    Search for recipes based on query and filters.
    """
    try:
        user_input = request.get_json()
        results = search_recipes(user_input)
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@recipe_blueprint.route("/<string:title>/", methods=["GET"])
def details(title):
    """
    Fetch details of a single recipe by title.
    """
    try:
        recipe = get_recipe_details(title)
        if "error" in recipe:
            return jsonify(recipe), 404
        return jsonify(recipe)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
