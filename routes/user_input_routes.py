from flask import Blueprint, request, jsonify
from scripts.user_input_handler import handle_user_input

user_input_blueprint = Blueprint("user_input", __name__)

@user_input_blueprint.route("/", methods=["POST"])
def handle_input():
    user_request = request.json
    processed_input = handle_user_input(user_request)
    return jsonify(processed_input)
