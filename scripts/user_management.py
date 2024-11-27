import sqlite3
import json
from pathlib import Path

def get_db_connection():
    db_path = Path(__file__).resolve().parent.parent / "data" / "app.db"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

def create_user(user_data):
    try:
        user_id = user_data.get("user_id")
        name = user_data.get("name", "")
        weight = user_data.get("weight", None)
        age = user_data.get("age", None)
        tags = json.dumps(user_data.get("tags", {}))  # Convert tags to JSON string

        if not user_id:
            return {"error": "User ID is required"}, 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        existing_user = cursor.fetchone()

        if existing_user:
            cursor.execute(
                "UPDATE users SET name = ?, weight = ?, age = ?, tags = ? WHERE user_id = ?",
                (name, weight, age, tags, user_id),
            )
        else:
            cursor.execute(
                "INSERT INTO users (user_id, name, weight, age, tags) VALUES (?, ?, ?, ?, ?)",
                (user_id, name, weight, age, tags),
            )

        conn.commit()
        conn.close()
        return {"message": "User information updated successfully"}, 200
    except Exception as e:
        return {"error": str(e)}, 500

def get_user(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()

        if not user:
            return {"error": f"User with ID {user_id} not found"}, 404

        user_data = dict(user)
        user_data["tags"] = json.loads(user_data["tags"])  # Convert JSON string to dictionary
        return user_data
    except Exception as e:
        return {"error": str(e)}, 500
