from flask import Blueprint, request, jsonify
from scripts.user_management import create_user, get_user

user_blueprint = Blueprint("user", __name__)

@user_blueprint.route("/", methods=["POST"])
def create_or_update_user():
    """
    Create or update a user.
    Request body should include: {"user_id": 1, "name": "John", "weight": 70, "dob": "1993-01-15", "tags": {"pork": false, "alcohol": false}}
    """
    try:
        user_data = request.get_json()
        response, status_code = create_user(user_data)
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_blueprint.route("/<int:user_id>/", methods=["GET"])
def fetch_user(user_id):
    """
    Fetch user information by user ID.
    """
    try:
        user_data = get_user(user_id)
        return jsonify(user_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
