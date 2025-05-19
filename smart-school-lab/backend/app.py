from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend access

# Mock data
devices = [
    {"id": 1, "name": "Projector", "status": "off"},
    {"id": 2, "name": "Smart Light", "status": "off"},
    {"id": 3, "name": "Fan", "status": "on"}
]

users = [
    {"id": 1, "username": "teacher1", "password": "pass123", "role": "teacher"},
    {"id": 2, "username": "student1", "password": "pass123", "role": "student"}
]

logs = []

# ----------- Devices -----------
@app.route("/devices", methods=["GET"])
def get_all_devices():
    return jsonify(devices), 200

@app.route("/devices/<int:device_id>", methods=["GET"])
def get_device(device_id):
    device = next((d for d in devices if d["id"] == device_id), None)
    if device:
        return jsonify(device), 200
    return jsonify({"error": "Device not found"}), 404

@app.route("/devices/<int:device_id>/toggle", methods=["POST"])
def toggle_device(device_id):
    data = request.json
    action = data.get("action")

    device = next((d for d in devices if d["id"] == device_id), None)
    if device and action in ["on", "off"]:
        device["status"] = action
        logs.append({"device_id": device_id, "action": action})
        return jsonify({"message": f"Device '{device['name']}' turned {action}"}), 200
    return jsonify({"error": "Invalid request"}), 400

@app.route("/devices/add", methods=["POST"])
def add_device():
    data = request.json
    new_id = max([d["id"] for d in devices]) + 1 if devices else 1
    device = {
        "id": new_id,
        "name": data.get("name", "Unnamed Device"),
        "status": "off"
    }
    devices.append(device)
    return jsonify(device), 201

@app.route("/devices/<int:device_id>/delete", methods=["DELETE"])
def delete_device(device_id):
    global devices
    devices = [d for d in devices if d["id"] != device_id]
    return jsonify({"message": f"Device {device_id} deleted"}), 200

# ----------- Users -----------
@app.route("/users", methods=["GET"])
def list_users():
    return jsonify([{"id": u["id"], "username": u["username"], "role": u["role"]} for u in users]), 200

@app.route("/users/login", methods=["POST"])
def login_user():
    data = request.json
    user = next((u for u in users if u["username"] == data.get("username") and u["password"] == data.get("password")), None)
    if user:
        return jsonify({"message": "Login successful", "user": {"id": user["id"], "role": user["role"]}}), 200
    return jsonify({"error": "Invalid credentials"}), 401

# ----------- Logs -----------
@app.route("/logs", methods=["GET"])
def get_logs():
    return jsonify(logs), 200

@app.route("/logs/add", methods=["POST"])
def add_log():
    data = request.json
    logs.append(data)
    return jsonify({"message": "Log added"}), 201

# ----------- Run -----------
if __name__ == "__main__":
    app.run(debug=True)
