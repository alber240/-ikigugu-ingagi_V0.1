from flask import Blueprint, jsonify, request
from flask_cors import CORS
from models.device_model import devices, find_device_by_id
from datetime import datetime
import json
import os
from datetime import datetime, timedelta  # ✅ Add timedelta here


# ---------------------------------------------
# 🔹 Global Variables & Setup
# ---------------------------------------------
device_bp = Blueprint('devices', __name__)  # ✅ Blueprint for device-related routes
CORS(device_bp)  # ✅ Enable CORS globally for API access
device_usage_timestamps = {}  # ✅ Dictionary to track device usage duration

# ✅ Log file path for tracking device actions
LOG_FILE = os.path.join(os.path.dirname(__file__), "../data/logs.json")

# ---------------------------------------------
# 🔹 Utility Functions for Logging
# ---------------------------------------------
def load_logs():
    """ ✅ Loads logs.json safely, creates file if missing """
    try:
        with open(LOG_FILE, "r") as file:
            logs = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []  # ✅ Initializes empty list if file is missing or corrupted
        with open(LOG_FILE, "w") as file:
            json.dump(logs, file, indent=4)
    return logs

def save_log(entry):
    """ ✅ Saves an action log entry to logs.json """
    logs = load_logs()
    logs.append(entry)
    with open(LOG_FILE, "w") as file:
        json.dump(logs, file, indent=4)

# ---------------------------------------------
# 🔹 API Routes for Device Control
# ---------------------------------------------

@device_bp.after_request
def add_cors_headers(response):
    """ ✅ Adds CORS headers for API accessibility from the frontend """
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

# ---------------------------------------------
# 🔹 Fetch All Devices (GET /devices)
# ---------------------------------------------
@device_bp.route('/', methods=['GET'])
def get_all_devices():
    """ ✅ Returns a list of all available devices """
    return jsonify(devices), 200

# ---------------------------------------------
# 🔹 Fetch Device Status (GET /devices/status)
# ---------------------------------------------
@device_bp.route('/status', methods=['GET'])
def get_device_status():
    """ ✅ Returns current real-time status of all devices """
    return jsonify(devices), 200

# ---------------------------------------------
# 🔹 Toggle Device Status (ON/OFF) (POST /devices/<device_id>/toggle)
# ---------------------------------------------
@device_bp.route('/<int:device_id>/toggle', methods=['POST'])
def toggle_device(device_id):
    """ ✅ Toggles device ON/OFF and logs action with correct username """
    data = request.json
    username = data.get("username", "Unknown")

    # ✅ Ensure username is valid before saving log
    if username.strip() == "" or username.lower() == "unknown":
        username = "System User"  # 🔹 Replace "Unknown" with a default system user

    device = find_device_by_id(device_id)
    if not device:
        return jsonify({"error": "Device not found"}), 404

    device["status"] = "on" if device["status"] == "off" else "off"

    log_entry = {
        "action": device["status"],
        "device": device["name"],
        "username": username,  # ✅ Now ensures proper username
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_log(log_entry)

    return jsonify({"message": f"{device['name']} turned {device['status'].upper()}!", "device": device}), 200


# ---------------------------------------------
# 🔹 Fetch Device Analytics (GET /devices/analytics)
# ---------------------------------------------
@device_bp.route('/analytics', methods=['GET'])
def get_device_analytics():
    """ ✅ Returns device analytics including usage hours """
    analytics_data = [
        {"name": device["name"], "status": device["status"], "total_usage_hours": device.get("total_usage_hours", 0)}
        for device in devices
    ]
    return jsonify(analytics_data), 200


# ---------------------------------------------
# 🔹 Save Device Schedule (POST /devices/<device_id>/schedule)
# ---------------------------------------------
@device_bp.route('/<int:device_id>/schedule', methods=['POST', 'OPTIONS'])
def save_schedule(device_id):
    """ ✅ Saves scheduling settings and logs the update """
    if request.method == "OPTIONS":  # ✅ Handle CORS preflight request
        response = jsonify({"message": "CORS preflight handled"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        return response, 200

    try:
        data = request.json
        username = data.get("username", "Unknown")
        on_time = data.get("on_time")
        off_time = data.get("off_time")

        if not on_time or not off_time:
            return jsonify({"error": "Missing start or end time"}), 400

        device = find_device_by_id(device_id)
        if not device:
            return jsonify({"error": "Device not found"}), 404

        # ✅ Log scheduling action
        log_entry = {
            "action": "schedule_set",
            "device": device["name"],
            "username": username,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "schedule": {"start_time": on_time, "end_time": off_time}
        }
        save_log(log_entry)

        return jsonify({"message": f"Schedule set from {on_time} to {off_time} for {device['name']}"}), 200

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

# ---------------------------------------------
# 🔹 Request Access to a Device (POST /devices/<device_id>/request-access)
# ---------------------------------------------
@device_bp.route('/<int:device_id>/request-access', methods=['POST'])
def request_device_access(device_id):
    """ ✅ Allows students to request access to a device and logs it """
    data = request.json
    username = data.get("username", "Unknown")

    device = find_device_by_id(device_id)
    if not device:
        return jsonify({"error": "Device not found"}), 404

    # ✅ Log request action
    log_entry = {
        "action": "request",
        "device": device["name"],
        "username": username,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_log(log_entry)

    return jsonify({"message": f"Access requested for {device['name']} by {username}"}), 200

@device_bp.route('/delete-logs', methods=['POST'])
def delete_old_logs():
    """ ✅ Debugging log deletion to identify issues """
    try:
        logs = load_logs()
        print(f"🔹 Debug: Loaded {len(logs)} logs from logs.json")  # ✅ Print total logs loaded

        cutoff_date = datetime.now() - timedelta(days=1)  # 🔹 Change from 90 days to 1 for testing

        filtered_logs = []  # ✅ Initialize empty list for cleaned logs

        for log in logs:
            try:
                log_timestamp = datetime.strptime(log.get("timestamp", "1900-01-01"), "%Y-%m-%d %H:%M:%S")
                if log_timestamp > cutoff_date:
                    filtered_logs.append(log)  # ✅ Keep valid logs
            except ValueError as e:
                print(f"❌ Error parsing timestamp: {log.get('timestamp')} → {e}")  # ✅ Identify bad timestamps

        print(f"✅ Debug: {len(filtered_logs)} logs remain after filtering")  # ✅ Print logs remaining

        save_logs(filtered_logs)  # ✅ Overwrite logs.json with cleaned logs

        return jsonify({"message": "✅ Logs older than 1 day deleted successfully!"}), 200

    except Exception as e:
        print(f"❌ Internal Server Error: {str(e)}")  # ✅ Log unexpected errors
        return jsonify({"error": f"❌ Failed to delete logs: {str(e)}"}), 500


# ---------------------------------------------
# 🔹 Utility Functions for Logging
# ---------------------------------------------
def load_logs():
    """ ✅ Loads logs.json safely, creates file if missing """
    try:
        with open(LOG_FILE, "r") as file:
            logs = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []  # ✅ Initializes empty list if file is missing or corrupted
        with open(LOG_FILE, "w") as file:
            json.dump(logs, file, indent=4)
    return logs

def save_logs(logs):
    """ ✅ Saves the full list of logs to logs.json (Overwrites existing logs) """
    with open(LOG_FILE, "w") as file:
        json.dump(logs, file, indent=4)
