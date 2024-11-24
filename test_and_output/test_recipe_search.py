import pandas as pd
from scripts.data_storage import load_from_sql
from scripts.recipe_search import search_recipes
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
# Load dataset from SQLite
data = load_from_sql(db_path=PROJECT_ROOT / "data" / "recipes.db", table_name="recipes")

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
