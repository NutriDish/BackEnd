from flask import Blueprint, jsonify
from firebase_admin import firestore

# Define the Blueprint
recipe_details_blueprint = Blueprint("recipe_details_route", __name__)
db = firestore.client()

def get_recipe_details(title):
    """
    Retrieve the details of a specific recipe by title from Firestore.
    """
    try:
        # Query Firestore for the recipe with the given title (case-insensitive)
        recipes_ref = db.collection("recipes").where("title", "==", title.strip())
        recipe_docs = recipes_ref.stream()
        recipe = next((doc.to_dict() for doc in recipe_docs), None)

        if not recipe:
            return {"error": f"Recipe with title '{title}' not found"}, 404

        # Format the response to exclude unnecessary keys (if needed)
        formatted_recipe = {
            "title": recipe.get("title"),
            "description": recipe.get("desc"),
            "calories": recipe.get("calories"),
            "protein": recipe.get("protein"),
            "fat": recipe.get("fat"),
            "sodium": recipe.get("sodium"),
            "ingredients": recipe.get("ingredients"),
            "directions": recipe.get("directions"),
            "categories": recipe.get("categories"),
            "date": recipe.get("date"),
            "image_url": recipe.get("image_url")  # Include thumbnail if available
        }

        return formatted_recipe
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
