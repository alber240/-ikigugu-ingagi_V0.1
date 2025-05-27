import jwt
import datetime
from flask import Blueprint, request, jsonify

auth_bp = Blueprint("auth", __name__)

SECRET_KEY = "your_secret_key"  # 🔒 Use a strong secret key
TOKEN_EXPIRATION_MINUTES = 30  # ✅ Access token expires in 30 minutes
REFRESH_TOKEN_EXPIRATION_DAYS = 7  # ✅ Refresh token lasts 7 days

@auth_bp.route('/login', methods=['POST'])
def login():
    """ ✅ Handles user login authentication and generates JWT tokens """
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # ✅ Mock authentication logic (Replace with actual database validation)
    if username == "admin" and password == "securepassword":
        access_token_payload = {
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=TOKEN_EXPIRATION_MINUTES)
        }
        refresh_token_payload = {
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=REFRESH_TOKEN_EXPIRATION_DAYS)
        }

        access_token = jwt.encode(access_token_payload, SECRET_KEY, algorithm="HS256")
        refresh_token = jwt.encode(refresh_token_payload, SECRET_KEY, algorithm="HS256")

        return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

@auth_bp.route('/refresh', methods=['POST'])
def refresh_token():
    """ 🔄 Automatically refresh JWT token before expiration """
    refresh_header = request.headers.get("Authorization")

    if not refresh_header or not refresh_header.startswith("Bearer "):
        return jsonify({"error": "Refresh token missing"}), 401

    refresh_token = refresh_header.split(" ")[1]  # ✅ Extract actual token

    try:
        decoded_refresh = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
        new_access_token_payload = {
            "username": decoded_refresh["username"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=TOKEN_EXPIRATION_MINUTES)
        }
        new_refresh_token_payload = {
            "username": decoded_refresh["username"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=REFRESH_TOKEN_EXPIRATION_DAYS)
        }

        new_access_token = jwt.encode(new_access_token_payload, SECRET_KEY, algorithm="HS256")
        new_refresh_token = jwt.encode(new_refresh_token_payload, SECRET_KEY, algorithm="HS256")

        return jsonify({"access_token": new_access_token, "refresh_token": new_refresh_token}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Refresh token expired, please log in again"}), 403
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid refresh token"}), 403
