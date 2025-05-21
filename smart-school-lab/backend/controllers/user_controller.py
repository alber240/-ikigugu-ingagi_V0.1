### `controllers/user_controller.py`

from flask import Blueprint, jsonify, request
from models.user_model import users

user_bp = Blueprint('users', __name__)

@user_bp.route('', methods=['GET'])
def list_users():
    return jsonify([{"id": u["id"], "username": u["username"], "role": u["role"]} for u in users]), 200

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = next((u for u in users if u['username'] == data.get('username') and u['password'] == data.get('password')), None)
    if user:
        return jsonify({"message": "Login successful", "user": {"id": user["id"], "role": user["role"]}}), 200
    return jsonify({"error": "Invalid credentials"}), 401