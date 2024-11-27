import sqlite3
import random
from datetime import datetime, timedelta
from pathlib import Path
import json

def get_recipes_not_in_cooldown(user_id, meal_type, selected_tags=None, cooldown_days=7):
    db_path = Path(__file__).resolve().parent.parent / "data" / "app.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Calculate cooldown period
    cooldown_date = (datetime.now() - timedelta(days=cooldown_days)).strftime("%Y-%m-%d")

    # Query recipes not in cooldown
    cursor.execute("""
        SELECT * FROM recipes
        WHERE id NOT IN (
            SELECT recipe_id
            FROM meal_plan
            WHERE user_id = ? AND meal_type = ? AND date_used > ?
        )
    """, (user_id, meal_type, cooldown_date))

    recipes = cursor.fetchall()
    conn.close()

    # Filter recipes by tags
    if selected_tags:
        recipes = filter_recipes_by_tags(recipes, selected_tags)

    return recipes


def filter_recipes_by_tags(recipes, tags):
    if not tags:
        return recipes  # No filtering needed if no tags are provided

    filtered_recipes = []
    for recipe in recipes:
        recipe_tags = recipe[4]  # Assuming tags are stored as a JSON string in column 4
        recipe_tags_dict = json.loads(recipe_tags)

        if all(recipe_tags_dict.get(tag, False) == value for tag, value in tags.items()):
            filtered_recipes.append(recipe)

    return filtered_recipes


def generate_meal_plan(user_id, selected_tags=None):
    meal_types = ["breakfast", "lunch", "dinner", "snack", "dessert"]
    meal_plan = {meal: [] for meal in meal_types}

    db_path = Path(__file__).resolve().parent.parent / "data" / "app.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for meal_type in meal_types:
        # Fetch recipes that match tags and are not in cooldown
        recipes = get_recipes_not_in_cooldown(user_id, meal_type, selected_tags)

        if not recipes:
            # Fallback: Recommend recipes that match tags but are in cooldown
            cursor.execute("SELECT * FROM recipes WHERE tags LIKE ?", (f"%{meal_type}%",))
            all_recipes = cursor.fetchall()

            # Filter fallback recipes by tags
            recipes = filter_recipes_by_tags(all_recipes, selected_tags)

        # Randomly select 7 recipes for the week (one per day)
        weekly_recipes = random.sample(recipes, min(7, len(recipes)))
        for recipe in weekly_recipes:
            meal_plan[meal_type].append({
                "id": recipe[0],
                "title": recipe[1],
                "ingredients": recipe[2],
                "directions": recipe[3],
                "tags": recipe[4],
            })

            # Log this recipe as used in the meal plan
            cursor.execute("""
                INSERT INTO meal_plan (user_id, recipe_id, meal_type, date_used)
                VALUES (?, ?, ?, ?)
            """, (user_id, recipe[0], meal_type, datetime.now().strftime("%Y-%m-%d")))

    conn.commit()
    conn.close()

    return meal_plan