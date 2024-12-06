from scripts.data_storage import get_db_connection
import json
from datetime import datetime

def create_user(user_data):
    """
    Create a new user or update an existing user.
    :param user_data: Dictionary containing user details (user_id, name, weight, dob, tags).
    :return: A message indicating success or failure.
    """
    try:
        user_id = user_data.get("user_id")  # The user_id is passed from the mobile side
        name = user_data.get("name", "")
        weight = user_data.get("weight", None)
        dob = user_data.get("dob", "")  # Date of birth (DOB)
        tags = json.dumps(user_data.get("tags", {}))  # Convert tags to JSON string

        # Calculate age based on DOB
        age = calculate_age(dob)

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the user exists
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        existing_user = cursor.fetchone()

        if existing_user:
            # Update existing user
            cursor.execute(
                                "UPDATE users SET name = ?, weight = ?, dob = ?, age = ?, tags = ? WHERE user_id = ?",
                (name, weight, dob, age, tags, user_id),
            )
        else:
            # Insert new user
            cursor.execute(
                "INSERT INTO users (user_id, name, weight, dob, age, tags) VALUES (?, ?, ?, ?, ?, ?)",
                (user_id, name, weight, dob, age, tags),
            )

        conn.commit()
        conn.close()
        return {"message": "User information updated successfully"}, 200
    except Exception as e:
        return {"error": str(e)}, 500

def calculate_age(dob):
    today = datetime.today()
    birth_date = datetime.strptime(dob, "%Y-%m-%d")
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def get_user(user_id):
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

