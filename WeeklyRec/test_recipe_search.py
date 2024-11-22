import pandas as pd
from data_storage import load_from_sql
from recipe_search import search_recipes

# Load dataset from SQLite
data = load_from_sql(db_path="WeeklyRec/recipes.db", table_name="recipes")

# User input simulation
user_input = {
    "keywords": "chicken",
    "ingredients": ["chicken", "salt"],
    "nutritional_constraints": {
        "calories": {"min": 100, "max": 500},
        "protein": {"min": 10, "max": 50},
    },
    "tags": {"lunch": True, "low fat": True},
}

# Search recipes
filtered_recipes = search_recipes(data, user_input)
print(filtered_recipes.head())
