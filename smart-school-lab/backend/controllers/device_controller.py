from flask import Blueprint, jsonify, request
from flask_cors import CORS
from models.device_model import devices, find_device_by_id, toggle_device_status

# ✅ Create a Blueprint for device-related routes
device_bp = Blueprint('devices', __name__)

# ✅ Enable CORS for device-related requests
CORS(device_bp)

# ---------------------------------------------
# 🔹 Fetch All Devices (GET /devices)
# ---------------------------------------------
@device_bp.route('/', methods=['GET'])
def get_all_devices():
    """ Returns a list of all available devices """
    return jsonify(devices), 200

# ---------------------------------------------
# 🔹 Fetch Single Device by ID (GET /devices/<device_id>)
# ---------------------------------------------
@device_bp.route('/<int:device_id>', methods=['GET'])
def get_device(device_id):
    """ Returns details of a single device based on device ID """
    device = find_device_by_id(device_id)
    if device:
        return jsonify(device), 200
    return jsonify({"error": "Device not found"}), 404

# ---------------------------------------------
# 🔹 Toggle Device Status (ON/OFF) (POST /devices/<device_id>/toggle)
# ---------------------------------------------
@device_bp.route('/<int:device_id>/toggle', methods=['POST'])
def toggle_device(device_id):
    """ Toggles the device status between ON and OFF """
    data = request.json
    action = data.get('action')  # Expected values: 'on' or 'off'

    # Validate action input
    if action not in ['on', 'off']:
        return jsonify({"error": "Invalid action. Use 'on' or 'off'"}), 400

    result = toggle_device_status(device_id, action)
    return jsonify(result), (200 if 'message' in result else 400)

# ---------------------------------------------
# 🔹 Add a New Device (POST /devices/add)
# ---------------------------------------------
@device_bp.route('/add', methods=['POST'])
def add_device():
    """ Adds a new device to the system """
    data = request.json
    new_id = max([d['id'] for d in devices], default=0) + 1

    device = {
        'id': new_id,
        'name': data.get('name', 'Unnamed Device'),
        'status': 'off'  # Default status is OFF
    }
    
    devices.append(device)
    return jsonify(device), 201

# ---------------------------------------------
# 🔹 Delete a Device (DELETE /devices/<device_id>/delete)
# ---------------------------------------------
@device_bp.route('/<int:device_id>/delete', methods=['DELETE'])
def delete_device(device_id):
    """ Deletes a device from the system """
    global devices
    devices = [d for d in devices if d['id'] != device_id]
    return jsonify({"message": f"Device {device_id} deleted"}), 200

# ---------------------------------------------
# 🔹 Save Schedule Settings (POST /devices/<device_id>/schedule)
# ---------------------------------------------
@device_bp.route('/<int:device_id>/schedule', methods=['POST', 'OPTIONS'])
def save_schedule(device_id):
    """
    Saves scheduling settings for a device.
    Expected JSON format: {"on_time": "08:00", "off_time": "12:00"}
    """
    if request.method == "OPTIONS":
        response = jsonify({"message": "CORS preflight handled"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        return response, 200

    data = request.json
    if not data.get("on_time") or not data.get("off_time"):
        return jsonify({"error": "Missing time values"}), 400

    return jsonify({"message": f"Schedule set from {data['on_time']} to {data['off_time']} for device {device_id}"}), 200
