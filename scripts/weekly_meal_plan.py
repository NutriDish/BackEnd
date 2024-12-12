import random
import sqlite3
from scripts.data_storage import get_db_connection
from firebase_admin import firestore
from datetime import datetime,timedelta

db = firestore.client()


def get_recipes_not_in_cooldown(user_id, meal_type, selected_tags=None, cooldown_days=7):
    """
    Fetch recipes that are not in cooldown from Firestore.
    """
    try:
        # Query recipes in Firestore
        recipes_ref = db.collection("recipes").where(f"is_{meal_type}", "==", True)
        recipes = [doc.to_dict() for doc in recipes_ref.stream()]

        # Filter recipes not in cooldown
        meal_plan_ref = db.collection("mealPlan").where("userId", "==", user_id).where("mealType", "==", meal_type)
        meal_plan_docs = meal_plan_ref.stream()
        recent_recipes = [doc.to_dict()["recipeTitle"] for doc in meal_plan_docs if doc.to_dict()["dateUsed"] > str(datetime.now() - timedelta(days=cooldown_days))]

        filtered_recipes = [recipe for recipe in recipes if recipe["title"] not in recent_recipes]

        # Apply tag filters
        if selected_tags:
            filtered_recipes = filter_recipes_by_tags(filtered_recipes, selected_tags)

        return filtered_recipes
    except Exception as e:
        return {"error": str(e)}, 500


def filter_recipes_by_tags(recipes, tags):
    """
    Filters recipes by the selected tags.
    :param recipes: The list of recipes (as dictionaries).
    :param tags: The selected tags for filtering.
    :return: A filtered list of recipes based on selected tags.
    """
    filtered_recipes = []
    for recipe in recipes:
        match = True
        for tag, value in tags.items():
            if recipe.get(tag) != value:
                match = False
                break
        if match:
            filtered_recipes.append(recipe)
    return filtered_recipes


def generate_meal_plan(user_id, selected_tags=None):
    """
    Generate a weekly meal plan in Firestore.
    """
    try:
        meal_types = ["breakfast", "lunch", "dinner", "snack", "dessert"]
        meal_plan = {f"Day {day + 1}": {} for day in range(7)}  # Initialize 7-day plan

        for day in range(7):
            daily_meals = {}
            for meal_type in meal_types:
                recipes = get_recipes_not_in_cooldown(user_id, meal_type, selected_tags)

                if not recipes:
                    continue

                selected_recipe = random.choice(recipes)

                # Add meal plan to Firestore
                db.collection("mealPlan").add({
                    "userId": user_id,
                    "recipeTitle": selected_recipe["title"],
                    "mealType": meal_type,
                    "dateUsed": datetime.now().strftime("%Y-%m-%d")
                })

                daily_meals[meal_type] = {
                    "title": selected_recipe["title"],
                    "image_url": selected_recipe.get("image_url"),
                    "dietary": {key: selected_recipe[key] for key in selected_recipe if key.startswith("is_")},
                    "ingredients": {key: selected_recipe[key] for key in selected_recipe if key.startswith("has_")}
                }

            meal_plan[f"Day {day + 1}"] = daily_meals

        return meal_plan
    except Exception as e:
        return {"error": str(e)}, 500
