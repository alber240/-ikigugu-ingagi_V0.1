from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

# ✅ Define Blueprint for user-related routes
user_bp = Blueprint('users', __name__)

# ✅ Sample user database (Replace with a real database)
users = {}  # 🔹 Temporary in-memory storage (Resets after restart)

# ---------------------------------------------
# 🔹 API Endpoint: User Signup (Registration)
# ---------------------------------------------
@user_bp.route('/signup', methods=['POST'])
def signup():
    """ ✅ Handles new user signup with secure password hashing """
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role").lower()  # 🔹 Normalize role to lowercase

    # ✅ Validate required fields
    if not username or not email or not password or not role:
        return jsonify({"error": "Missing required fields"}), 400

    if email in users:
        return jsonify({"error": "User already exists"}), 400

    # ✅ Store user with hashed password for security
    users[email] = {
        "id": len(users) + 1,  # Assign a unique ID
        "username": username,
        "email": email,
        "password": generate_password_hash(password),
        "role": role,
        "permissions": get_permissions_by_role(role)
    }
    return jsonify({"message": "User registered successfully", "role": role}), 201

# ---------------------------------------------
# 🔹 API Endpoint: User Login & Role-Based Authentication
# ---------------------------------------------
@user_bp.route('/login', methods=['POST'])
def login():
    """ ✅ Handles user login and verifies credentials """
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = users.get(email)

    if not user or not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    role = user["role"].lower()  # ✅ Normalize role

    print(f"DEBUG: Logging in user {user['username']} with role: {role}")  # ✅ Print role in Flask terminal

    return jsonify({
        "message": f"Welcome {user['username']}, Role: {role}",
        "user": {
            "id": user["id"],
            "username": user["username"],
            "role": role,  # ✅ Ensure role is correctly sent
            "permissions": user["permissions"]
        }
    }), 200

# ---------------------------------------------
# 🔹 API Endpoint: Fetch All Users (GET /users)
# ---------------------------------------------
@user_bp.route('/users', methods=['GET'])
def list_users():
    """ ✅ Fetches all registered users """
    return jsonify([
        {"id": u["id"], "username": u["username"], "role": u["role"], "email": u["email"]}
        for u in users.values()
    ]), 200

# ---------------------------------------------
# 🔹 Helper Function: Get Role-Based Permissions
# ---------------------------------------------
def get_permissions_by_role(role):
    """ ✅ Defines user permissions based on their role """
    role_permissions = {
        "teacher": ["manage_devices", "view_logs"],
        "student": ["view_devices"],
        "admin": ["manage_users", "manage_devices", "view_logs"]
    }
    return role_permissions.get(role, [])
