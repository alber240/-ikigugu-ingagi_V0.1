from flask import Blueprint, jsonify, request
from datetime import datetime
import json
import os

# ✅ Define a Blueprint for log-related routes
log_bp = Blueprint('logs', __name__)

# ✅ Define absolute path for logs.json
LOG_FILE = os.path.join(os.path.dirname(__file__), "../data/logs.json")

# ---------------------------------------------
# 🔹 Load logs safely (Prevent corruption & missing files)
# ---------------------------------------------
def load_logs():
    """ ✅ Reads logs.json safely & prevents file errors """
    try:
        with open(LOG_FILE, "r") as file:
            logs = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []  # ✅ Creates an empty list if file doesn't exist or is corrupt
        with open(LOG_FILE, "w") as file:
            json.dump(logs, file, indent=4)
    
    return logs

# ---------------------------------------------
# 🔹 Save logs safely (Prevent duplicates)
# ---------------------------------------------
def save_log(entry):
    """ ✅ Prevents duplicate logs & writes safely to logs.json """
    logs = load_logs()

    # ✅ Prevent duplicate entries before appending
    if not any(log["timestamp"] == entry["timestamp"] and log["device"] == entry["device"] for log in logs):
        logs.append(entry)

        with open(LOG_FILE, "w") as file:
            json.dump(logs, file, indent=4)

# ---------------------------------------------
# 🔹 API Endpoint: Retrieve all logs (GET /logs)
# ---------------------------------------------
@log_bp.route('/', methods=['GET'])
def get_logs():
    """ ✅ Fetch & return all usage logs dynamically """
    logs = load_logs()
    return jsonify(logs), 200

# ---------------------------------------------
# 🔹 API Endpoint: Add a new log entry (POST /logs)
# ---------------------------------------------
@log_bp.route('/', methods=['POST'])
def add_log():
    """ ✅ Adds a new log entry & improves error handling """
    try:
        data = request.json

        # ✅ Validate required fields before processing
        if not data or "action" not in data or "device_id" not in data or "username" not in data:
            return jsonify({"error": "Missing required fields: action, device_id, username"}), 400

        log_entry = {
            "action": data["action"],
            "device": f"Device {data['device_id']}",
            "username": data["username"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # ✅ Save log entry safely
        save_log(log_entry)

        return jsonify({"message": "Log entry added successfully", "log": log_entry}), 201

    except Exception as e:
        print(f"Error in add_log(): {str(e)}")  # ✅ Logs error for debugging
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500
