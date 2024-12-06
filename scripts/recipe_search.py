from scripts.data_storage import get_db_connection

def search_recipes(user_input):
    """
    Search for recipes based on a query and user-defined filters.
    :param user_input: Dictionary containing the search query and filter criteria.
    :return: A list of recipes matching the search query and filters.
    """
    query = user_input.get("query", "").lower()
    filters = user_input.get("filters", {})

    conn = get_db_connection()
    cursor = conn.cursor()

    # Build the search query with user-defined filters
    query_conditions = ["title LIKE ?", "ingredients LIKE ?"]
    params = [f"%{query}%", f"%{query}%"]

    for tag, value in filters.items():
        if value:
            query_conditions.append(f"{tag} = 1")
    
    where_clause = " AND ".join(query_conditions)
    cursor.execute(f"SELECT * FROM recipes WHERE {where_clause}", params)
    recipes = cursor.fetchall()

    conn.close()

    # Format and return the results with meal type, dietary preferences, and ingredients
    formatted_recipes = []
    for recipe in recipes:
        dietary = {key: recipe[val] for key, val in {
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
        }.items() if recipe[val] == 1}

        ingredients = {ingredient: recipe[f'has_{ingredient}'] for ingredient in [
            'pork', 'alcohol', 'beef', 'bread', 'butter', 'cabbage', 'carrot', 'cheese', 
            'chicken', 'egg', 'eggplant', 'fish', 'onion', 'pasta', 'peanut', 'potato', 
            'rice', 'shrimp', 'tofu', 'tomato', 'zucchini'
        ] if recipe[f'has_{ingredient}'] == 1}

        # Limit dietary preferences to 2 and ingredients to 3
        dietary = dict(list(dietary.items())[:2])
        ingredients = dict(list(ingredients.items())[:3])

        formatted_recipes.append({
            "title": recipe["title"],
            "meal_type": {
                "breakfast": recipe["is_breakfast"],
                "lunch": recipe["is_lunch"],
                "dinner": recipe["is_dinner"],
                "snack": recipe["is_snack"],
                "dessert": recipe["is_dessert"]
            },
            "dietary": dietary,
            "ingredients": ingredients
        })

    return formatted_recipes
