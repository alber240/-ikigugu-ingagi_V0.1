from flask import Blueprint, jsonify, request
from models.user_model import users

# ✅ Define Blueprint for user-related routes
user_bp = Blueprint('users', __name__)

# ✅ Sample user roles & credentials data (Ideally should be in a database)
users = [
    {"id": 1, "username": "teacher1", "password": "password123", "role": "teacher", "permissions": ["control_devices", "view_logs"]},
    {"id": 2, "username": "student1", "password": "studentpass", "role": "student", "permissions": ["view_logs"]}
]

# ---------------------------------------------
# 🔹 API Endpoint: User Login & Role-Based Authentication
# ---------------------------------------------
@user_bp.route('/login', methods=['POST'])
def login():
    """ ✅ Handles user login with role-based authentication """
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # ✅ Validate input fields before processing
    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    # ✅ Find user by username & password
    user = next((u for u in users if u["username"] == username and u["password"] == password), None)
    
    if user:
        return jsonify({
            "message": "Login successful",
            "user": {"id": user["id"], "role": user["role"], "permissions": user["permissions"]}
        }), 200
    
    return jsonify({"error": "Invalid credentials"}), 401


# ---------------------------------------------
# 🔹 API Endpoint: Fetch All Users
# ---------------------------------------------
@user_bp.route('/users', methods=['GET'])
def list_users():
    """ ✅ Fetches all registered users """
    return jsonify([{"id": u["id"], "username": u["username"], "role": u["role"]} for u in users]), 200
