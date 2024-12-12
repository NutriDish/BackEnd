from flask import Blueprint, request, jsonify
from firebase_admin import firestore
from scripts.assign_thumbnails import get_random_image_url, load_image_data

# Load image data for thumbnails
IMAGE_DATA = load_image_data("data/image_path_url.csv")

db = firestore.client()

recipe_blueprint = Blueprint("recipe", __name__)

@recipe_blueprint.route("/", methods=["POST"])
def search():
    """
    Search for recipes based on query and filters.

    {
        "query": "avocado toast",
        "filters": {
            "vegetarian": true,
            "low_carb": true
        }
    }
    """
    try:
        user_input = request.get_json()
        query = user_input.get("query", "").lower()
        filters = user_input.get("filters", {})

        # Query Firestore for recipes
        recipes_ref = db.collection("recipes")
        if query:
            recipes_ref = recipes_ref.where("title", ">=", query).where("title", "<=", query + "\uf8ff")
        recipes = [doc.to_dict() for doc in recipes_ref.stream()]

        # Apply filters
        for key, value in filters.items():
            recipes = [recipe for recipe in recipes if recipe.get(key) == value]

        # Assign thumbnails if not present
        for recipe in recipes:
            if "image_url" not in recipe or not recipe["image_url"]:
                recipe["image_url"] = get_random_image_url(IMAGE_DATA)

        return jsonify(recipes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@recipe_blueprint.route("/search", methods=["GET"])
def search_get():
    """
    Search for recipes based on a query passed as a URL parameter.
    """
    try:
        query = request.args.get("query", "").lower()
        if not query:
            return jsonify({"error": "Query parameter is required"}), 400

        # Query Firestore for recipes matching the query
        recipes_ref = db.collection("recipes").where("title", ">=", query).where("title", "<=", query + "\uf8ff")
        recipes = [doc.to_dict() for doc in recipes_ref.stream()]

        # Assign thumbnails if not present
        for recipe in recipes:
            if "image_url" not in recipe or not recipe["image_url"]:
                recipe["image_url"] = get_random_image_url(IMAGE_DATA)

        return jsonify(recipes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
