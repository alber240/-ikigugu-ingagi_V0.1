from flask import Blueprint, jsonify, request
from flask_cors import CORS
from models.device_model import devices, find_device_by_id
from datetime import datetime
import json
import os

# ✅ Device usage tracking dictionary
device_usage_timestamps = {}

# ✅ Create a Blueprint for device-related routes
device_bp = Blueprint('devices', __name__)

# ✅ Enable CORS globally for this blueprint
CORS(device_bp)

@device_bp.after_request
def add_cors_headers(response):
    """ ✅ Adds CORS headers to ensure API accessibility from frontend """
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

# ✅ Define absolute path for logs.json
LOG_FILE = os.path.join(os.path.dirname(__file__), "../data/logs.json")

def load_logs():
    """ ✅ Loads logs.json safely, creates file if missing """
    try:
        with open(LOG_FILE, "r") as file:
            logs = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []  # ✅ Initializes an empty log list if file doesn't exist or is corrupt
        with open(LOG_FILE, "w") as file:
            json.dump(logs, file, indent=4)
    
    return logs

def save_log(entry):
    """ ✅ Saves a log entry to logs.json """
    logs = load_logs()
    logs.append(entry)

    with open(LOG_FILE, "w") as file:
        json.dump(logs, file, indent=4)

# ---------------------------------------------
# 🔹 Fetch All Devices (GET /devices)
# ---------------------------------------------
@device_bp.route('/', methods=['GET'])
def get_all_devices():
    """ ✅ Returns a list of all available devices """
    return jsonify(devices), 200

# ---------------------------------------------
# 🔹 Fetch Single Device by ID (GET /devices/<device_id>)
# ---------------------------------------------
@device_bp.route('/<int:device_id>', methods=['GET'])
def get_device(device_id):
    """ ✅ Returns details of a specific device by ID """
    device = find_device_by_id(device_id)
    if device:
        return jsonify(device), 200
    return jsonify({"error": "Device not found"}), 404

# ---------------------------------------------
# 🔹 Toggle Device Status (ON/OFF) (POST /devices/<device_id>/toggle)
# ---------------------------------------------
@device_bp.route('/<int:device_id>/toggle', methods=['POST'])
def toggle_device(device_id):
    """ ✅ Toggles device status and logs the action """
    data = request.json
    action = data.get('action')
    username = data.get("username", "Unknown")

    device = find_device_by_id(device_id)
    if not device:
        print(f"Error: Device ID {device_id} not found!")  # ✅ Debugging message
        return jsonify({"error": "Device not found"}), 404

    # ✅ Update device status
    device["status"] = action

    # ✅ Track device usage
    if action == "on":
        device_usage_timestamps[device_id] = datetime.now()
    elif action == "off" and device_id in device_usage_timestamps:
        on_time = device_usage_timestamps.pop(device_id)
        duration = (datetime.now() - on_time).seconds / 3600  
        device["total_usage_hours"] = device.get("total_usage_hours", 0) + duration  

    # ✅ Log device action
    log_entry = {
        "action": action,
        "device": device["name"],
        "username": username,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_log(log_entry)

    return jsonify({"message": f"Device {action} successfully!", "device": device}), 200


@device_bp.route('/analytics', methods=['GET'])
def get_device_analytics():
    """ ✅ Returns device analytics including usage hours """
    analytics_data = [{"name": device["name"], "status": device["status"], "total_usage_hours": device.get("total_usage_hours", 0)} for device in devices]
    return jsonify(analytics_data), 200

# ---------------------------------------------
# 🔹 Save Schedule Settings (POST /devices/<device_id>/schedule)
# ---------------------------------------------
@device_bp.route('/<int:device_id>/schedule', methods=['POST', 'OPTIONS'])
def save_schedule(device_id):
    """ ✅ Saves scheduling settings and logs the update """
    if request.method == "OPTIONS":
        response = jsonify({"message": "CORS preflight handled"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        return response, 200  # ✅ Handle CORS preflight request

    try:
        data = request.json
        username = data.get("username", "Unknown")
        on_time = data.get("on_time")
        off_time = data.get("off_time")

        if not on_time or not off_time:
            return jsonify({"error": "Missing start or end time"}), 400

        device = find_device_by_id(device_id)
        if not device:
            print(f"Error: Device ID {device_id} not found!")  # ✅ Debugging message
            return jsonify({"error": "Device not found"}), 404

        # ✅ Log scheduling action
        log_entry = {
            "action": "schedule_set",
            "device": device["name"],
            "username": username,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "schedule": {
                "start_time": on_time,
                "end_time": off_time
            }
        }
        save_log(log_entry)

        return jsonify({"message": f"Schedule set from {on_time} to {off_time} for {device['name']}"}), 200

    except Exception as e:
        print(f"Error in save_schedule: {str(e)}")  # ✅ Debugging message
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
        print(f"Error: Device ID {device_id} not found!")  # ✅ Debugging message
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
