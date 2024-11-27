import sqlite3
import pandas as pd
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent 

def save_to_sql(data, db_path=None, table_name="recipes"):
    if db_path is None:
        db_path = PROJECT_ROOT / "data" / "recipes.db"

    conn = sqlite3.connect(db_path)
    data.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

def save_to_json(data, json_path= None):
    if json_path is None:
        json_path = PROJECT_ROOT / "test_and_output" / "weekly_menu.json"

    
    with open(json_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

def load_from_sql(db_path = None, table_name="recipes"):
    if db_path is None:
        db_path = PROJECT_ROOT / "data" / "recipes.db"
    
    conn = sqlite3.connect(db_path)
    data = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return data
