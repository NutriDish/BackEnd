# Step 4: Define the data storage and format script

# data_storage.py
import sqlite3
import pandas as pd
import json

def save_to_sql(data, db_path="WeeklyRec/recipes.db", table_name="recipes"):
    """
    Save recipe dataset to an SQLite database.

    Parameters:
    - data (DataFrame): Recipe dataset.
    - db_path (str): Path to SQLite database file.
    - table_name (str): Table name for storing recipes.

    Returns:
    - None
    """
    conn = sqlite3.connect(db_path)
    data.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

def save_to_json(data, json_path="WeeklyRec/weekly_menu.json"):
    """
    Save weekly meal plan to a JSON file.

    Parameters:
    - data (dict): Weekly meal plan or other structured data.
    - json_path (str): Path to save the JSON file.

    Returns:
    - None
    """
    with open(json_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

def load_from_sql(db_path="WeeklyRec/recipes.db", table_name="recipes"):
    """
    Load recipe dataset from an SQLite database.

    Parameters:
    - db_path (str): Path to SQLite database file.
    - table_name (str): Table name for loading recipes.

    Returns:
    - DataFrame: Loaded recipe dataset.
    """
    conn = sqlite3.connect(db_path)
    data = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return data


# Save this script to the file system for modularization
with open("WeeklyRec/data_storage.py", "w") as f:
    f.write(save_to_sql.__code__.co_consts[0])
    f.write("\n")
    f.write(save_to_json.__code__.co_consts[0])
    f.write("\n")
    f.write(load_from_sql.__code__.co_consts[0])