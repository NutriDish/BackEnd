import sqlite3
import pandas as pd
from pathlib import Path

def save_to_sql(data, db_path=None, table_name="recipes"):
    if db_path is None:
        db_path = Path(__file__).resolve().parent.parent / "data" / "recipes.db"

    conn = sqlite3.connect(db_path)
    data.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

def load_from_sql(db_path, table_name="recipes"):
    conn = sqlite3.connect(db_path)
    data = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return data
