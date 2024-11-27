from flask import Blueprint, request, jsonify
from scripts.recipe_search import search_recipes
from scripts.recipe_details import get_recipe_details

recipe_blueprint = Blueprint("recipe", __name__)

@recipe_blueprint.route("/", methods=["POST"])
def search():
    user_input = request.get_json()
    return jsonify(search_recipes(user_input))

@recipe_blueprint.route("/<title>/", methods=["GET"])
def details(title):
    return jsonify(get_recipe_details(title))