# Step 4: Define the data storage and format script

# data_storage.py
import sqlite3
import pandas as pd
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent  # Adjust this as per your folder structure

def save_to_sql(data, db_path=None, table_name="recipes"):
    """
    Save recipe dataset to an SQLite database.

    Parameters:
    - data (DataFrame): Recipe dataset.
    - db_path (str): Path to SQLite database file.
    - table_name (str): Table name for storing recipes.

    Returns:
    - None
    """

    if db_path is None:
        db_path = PROJECT_ROOT / "data" / "recipes.db"

    conn = sqlite3.connect(db_path)
    data.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

def save_to_json(data, json_path= None):
    """
    Save weekly meal plan to a JSON file.

    Parameters:
    - data (dict): Weekly meal plan or other structured data.
    - json_path (str): Path to save the JSON file.

    Returns:
    - None
    """

    if json_path is None:
        json_path = PROJECT_ROOT / "test_and_output" / "weekly_menu.json"

    
    with open(json_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

def load_from_sql(db_path = None, table_name="recipes"):
    """
    Load recipe dataset from an SQLite database.

    Parameters:
    - db_path (str): Path to SQLite database file.
    - table_name (str): Table name for loading recipes.

    Returns:
    - DataFrame: Loaded recipe dataset.
    """

    if db_path is None:
        db_path = PROJECT_ROOT / "data" / "recipes.db"
    
    conn = sqlite3.connect(db_path)
    data = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return data


# Save this script to the file system for modularization

"""
with open("WeeklyRec/data_storage.py", "w") as f:
    f.write(save_to_sql.__code__.co_consts[0])
    f.write("\n")
    f.write(save_to_json.__code__.co_consts[0])
    f.write("\n")
    f.write(load_from_sql.__code__.co_consts[0])
"""