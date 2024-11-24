import pandas as pd
from scripts.data_storage import save_to_sql
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
# Load the dataset
data = pd.read_csv(PROJECT_ROOT / "data" / "Recipes.csv", delimiter=";")

# Save to SQLite
save_to_sql(data, db_path= PROJECT_ROOT / "data" / "recipes.db", table_name="recipes")
print("Recipes saved to SQLite!")