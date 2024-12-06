import random
from scripts.data_storage import get_db_connection

def get_recipes_not_in_cooldown(user_id, meal_type, selected_tags=None, cooldown_days=7):
    """
    Fetch recipes that are not in cooldown and match selected tags for a specific user and meal type.
    :param user_id: The ID of the user requesting the meal plan.
    :param meal_type: The type of meal (e.g., breakfast, lunch, dinner).
    :param selected_tags: Filters for tags such as dietary preferences.
    :param cooldown_days: Number of days for which recipes should not be reused.
    :return: A list of recipes that match the meal type, tags, and cooldown conditions.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Calculate cooldown period
    cursor.execute("""
        SELECT * FROM recipes
        WHERE id NOT IN (
            SELECT recipe_id
            FROM meal_plan
            WHERE user_id = ? AND meal_type = ? AND date_used > DATE('now', ?)
        )
    """, (user_id, meal_type, f"-{cooldown_days} days"))

    recipes = cursor.fetchall()
    conn.close()

    # Filter recipes by selected tags if any
    if selected_tags:
        recipes = filter_recipes_by_tags(recipes, selected_tags)

    return recipes


def filter_recipes_by_tags(recipes, tags):
    """
    Filters recipes by the selected tags.
    :param recipes: The list of recipes.
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
    Generate a weekly meal plan for a user, respecting cooldowns and filtering by tags.
    :param user_id: The ID of the user requesting the meal plan.
    :param selected_tags: Filters for dietary preferences and other tags.
    :return: A dictionary representing a 7-day meal plan with meals for each day.
    """
    meal_types = ["breakfast", "lunch", "dinner", "snack", "dessert"]
    meal_plan = {meal: [] for meal in meal_types}

    conn = get_db_connection()
    cursor = conn.cursor()

    # Generate meals for 7 days
    for day in range(7):
        daily_meals = {}
        for meal_type in meal_types:
            # Get recipes that are not in cooldown and match the tags
            recipes = get_recipes_not_in_cooldown(user_id, meal_type, selected_tags)

            if not recipes:
                continue  # If no recipes are available, skip to the next meal type

            # Randomly select a recipe for the meal type
            selected_recipe = random.choice(recipes)

            dietary = {key: selected_recipe[val] for key, val in {
                "vegetarian": "is_vegetarian",
                "vegan": "is_vegan",
                "pescatarian": "is_pescatarian",
                "paleo": "is_paleo",
                "dairy free": "is_dairy_free",
                "fat free": "is_fat_free",
                "peanut free": "is_peanut_free",
                "soy free": "is_soy_free",
                "wheat free": "is_wheat_free",
                "low carb": "is_low_carb",
                "low cal": "is_low_cal",
                "low fat": "is_low_fat",
                "low sodium": "is_low_sodium",
                "low sugar": "is_low_sugar",
                "low cholesterol": "is_low_cholesterol"
            }.items() if selected_recipe[val] == 1}

            ingredients = {ingredient: selected_recipe[f'has_{ingredient}'] for ingredient in [
                'pork', 'alcohol', 'beef', 'bread', 'butter', 'cabbage', 'carrot', 'cheese', 
                'chicken', 'egg', 'eggplant', 'fish', 'onion', 'pasta', 'peanut', 'potato', 
                'rice', 'shrimp', 'tofu', 'tomato', 'zucchini'
            ] if selected_recipe[f'has_{ingredient}'] == 1}

            # Limit dietary preferences to 2 and ingredients to 3
            dietary = dict(list(dietary.items())[:2])
            ingredients = dict(list(ingredients.items())[:3])

            daily_meals[meal_type] = {
                "title": selected_recipe["title"],
                "meal_type": meal_type,
                "dietary": dietary,
                "ingredients": ingredients
            }
        
        meal_plan[f"Day {day + 1}"] = daily_meals

    conn.close()
    return meal_plan
