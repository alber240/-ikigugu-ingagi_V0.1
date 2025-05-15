from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow requests from frontend

device_state = {"status": "off"}

@app.route("/device/toggle", methods=["POST"])
def toggle_device():
    action = request.json.get("action")
    if action in ["on", "off"]:
        device_state["status"] = action
        return jsonify({"message": f"Device turned {action}"}), 200
    return jsonify({"error": "Invalid action"}), 400

@app.route("/device/status", methods=["GET"])
def device_status():
    return jsonify(device_state), 200

@app.route("/")
def home():
    return "Welcome to the Smart School Lab API"

if __name__ == "__main__":
    app.run(debug=True)
