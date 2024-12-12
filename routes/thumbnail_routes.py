from flask import Blueprint, jsonify
from firebase_admin import firestore
import random

# Create a Flask Blueprint for thumbnail routes
thumbnail_routes = Blueprint('thumbnail_routes', __name__)

db = firestore.client()

# Load image URLs into memory (load this once during server startup)
# Assuming a predefined function to load image data exists
from scripts.assign_thumbnails import load_image_data
IMAGE_DATA = load_image_data("data/image_path_url.csv")

# Route to assign and fetch recipes with thumbnails
@thumbnail_routes.route('/api/recipes-with-thumbnails', methods=['GET'])
def get_recipes_with_thumbnails():
    try:
        # Fetch recipes from Firestore
        recipes_ref = db.collection("recipes")
        recipes = [doc.to_dict() for doc in recipes_ref.stream()]

        # Assign random thumbnails if not already present
        for recipe in recipes:
            if "image_url" not in recipe or not recipe["image_url"]:
                recipe["image_url"] = random.choice(IMAGE_DATA)["url"]

        return jsonify({"recipes": recipes}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Optional: Route to refresh thumbnails (assign random thumbnails again)
@thumbnail_routes.route('/api/refresh-thumbnails', methods=['POST'])
def refresh_thumbnails():
    try:
        recipes_ref = db.collection("recipes")
        recipes = recipes_ref.stream()

        # Update each recipe with a new random thumbnail
        for recipe_doc in recipes:
            recipe_data = recipe_doc.to_dict()
            recipe_data["image_url"] = random.choice(IMAGE_DATA)["url"]
            recipes_ref.document(recipe_doc.id).set(recipe_data)

        return jsonify({"message": "Thumbnails refreshed successfully."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
