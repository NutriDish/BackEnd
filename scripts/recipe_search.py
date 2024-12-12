from scripts.data_storage import get_db_connection
from firebase_admin import firestore
import random

db = firestore.client()


def search_recipes(user_input):
    """
    Search for recipes in Firestore.
    Handles both simple query searches and advanced searches with filters.
    """
    try:
        query = user_input.get("query", "").lower()
        filters = user_input.get("filters", {})

        recipes_ref = db.collection("recipes")
        
        # Apply query if provided
        if query:
            recipes_ref = recipes_ref.where("title", ">=", query).where("title", "<=", query + "\uf8ff")

        # Fetch recipes
        recipes = [doc.to_dict() for doc in recipes_ref.stream()]

        # Apply filters if present
        if filters:
            for key, value in filters.items():
                recipes = [recipe for recipe in recipes if recipe.get(key) == value]

        # Assign thumbnails if needed
        for recipe in recipes:
            if "image_url" not in recipe:
                recipe["image_url"] = random.choice(db.collection("images").stream()).to_dict()["url"]

        return recipes
    except Exception as e:
        return {"error": str(e)}, 500
