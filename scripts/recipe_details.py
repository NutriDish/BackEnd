import json
from pathlib import Path

def get_recipe_details(title):
    json_path = Path(__file__).resolve().parent.parent / "data" / "Recipe_Details.json"

    with open(json_path, "r") as f:
        recipes = json.load(f)

    recipe = next((r for r in recipes if r["title"].lower() == title.lower()), None)
    if not recipe:
        return {"error": f"Recipe with title '{title}' not found"}, 404

    return recipe
