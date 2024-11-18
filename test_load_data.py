import pandas as pd
from data_storage import save_to_sql

# Load the dataset
data = pd.read_csv("Recipes.csv", delimiter=";")

# Save to SQLite
save_to_sql(data, db_path="recipes.db", table_name="recipes")
print("Recipes saved to SQLite!")
