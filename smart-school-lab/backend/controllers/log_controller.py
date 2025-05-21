### `controllers/log_controller.py`

from flask import Blueprint, jsonify, request
from models.log_model import logs

log_bp = Blueprint('logs', __name__)

@log_bp.route('', methods=['GET'])
def get_logs():
    return jsonify(logs), 200

@log_bp.route('/add', methods=['POST'])
def add_log():
    data = request.json
    logs.append(data)
    return jsonify({"message": "Log added"}), 201