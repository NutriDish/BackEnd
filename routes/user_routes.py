from flask import Blueprint, request, jsonify
from scripts.user_management import create_user, get_user

user_blueprint = Blueprint("user", __name__)

@user_blueprint.route("/", methods=["POST"])
def create_or_update_user():
    return jsonify(*create_user(request.get_json()))

@user_blueprint.route("/<int:user_id>/", methods=["GET"])
def fetch_user(user_id):
    return jsonify(*get_user(user_id))
